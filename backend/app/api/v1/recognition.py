from fastapi import APIRouter, Depends, UploadFile, File, Body
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.response import success, error, UnifiedResponse
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.services.recognition import recognition_service
from app.schemas.recognition import RecognitionResultResponse
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

