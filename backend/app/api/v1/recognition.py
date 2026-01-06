from fastapi import APIRouter, Depends, UploadFile, File, Body, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.response import success, error, UnifiedResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.recognition import recognition_service
from app.schemas.recognition import RecognitionResultResponse, BatchRecognitionRequest
from app.schemas.upload import RecognizeByUrlRequest

router = APIRouter()

@router.post("/single", response_model=UnifiedResponse[RecognitionResultResponse], summary="单张图片识别（上传文件）")
async def recognize_single_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    上传单张图片进行车牌识别
    直接上传文件，后端自动上传到OSS并识别
    """
    if not file.content_type.startswith("image/"):
        return error(message="请上传图片文件")
        
    try:
        result = await recognition_service.process_image(file, current_user.id, db)
        
        if not result:
            return error(message="未检测到车牌或识别失败")
            
        return success(data=result)
    except Exception as e:
        print(f"Recognition error: {e}")
        return error(message="服务器内部错误，请检查日志")

@router.post("/by-url", response_model=UnifiedResponse[RecognitionResultResponse], summary="通过OSS URL识别车牌")
async def recognize_by_url(
    request: RecognizeByUrlRequest = Body(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    通过已上传到OSS的图片URL进行车牌识别
    前端流程：
    1. 先调用 /upload/image 上传图片到OSS，获取URL
    2. 再调用此接口，传入OSS URL进行识别
    """
    try:
        # 下载OSS图片并处理
        result = await recognition_service.process_image_from_url(request.image_url, current_user.id, db)
        
        if not result:
            return error(message="未检测到车牌或识别失败")
            
        return success(data=result)
    except Exception as e:
        print(f"Recognition error: {e}")
        return error(message="服务器内部错误，请检查日志")


@router.post("/start-single", summary="开始单张图片识别任务（WebSocket）")
async def start_recognition_task(
    background_tasks: BackgroundTasks,
    request: RecognizeByUrlRequest = Body(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    开始识别任务（支持WebSocket进度）
    1. 检查额度
    2. 扣除额度
    3. 创建任务
    4. 后台异步执行识别（通过WebSocket推送进度）
    """
    # 1. 检查额度
    if not recognition_service.check_quota(current_user.id, db):
        return error(message="今日识别额度已用尽")
        
    # 2. 扣除额度
    recognition_service.deduct_quota(current_user.id, db)
    
    # 3. 创建任务
    task = recognition_service.create_task(current_user.id, "single", db)
    
    # 4. 后台执行
    background_tasks.add_task(
        recognition_service.process_task_async, 
        task.task_uuid, 
        request.image_url, 
        current_user.id
    )
    
    return success(data={"task_uuid": task.task_uuid})

@router.post("/batch", summary="开始批量图片识别任务")
async def start_batch_recognition(
    background_tasks: BackgroundTasks,
    request: BatchRecognitionRequest = Body(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    批量识别任务
    1. 验证数量限制
    2. 创建批量任务
    3. 后台异步处理
    """
    if len(request.image_urls) > 50:
        return error(message="单次批量识别最多支持 50 张图片")
        
    if not request.image_urls:
        return error(message="请至少提供一张图片URL")

    # 1. Start Task
    task = recognition_service.create_task(current_user.id, "batch", db)
    
    # 2. Async Process
    background_tasks.add_task(
        recognition_service.process_batch_task_async,
        task.task_uuid,
        request.image_urls,
        current_user.id
    )
    
    return success(data={"task_uuid": task.task_uuid})

