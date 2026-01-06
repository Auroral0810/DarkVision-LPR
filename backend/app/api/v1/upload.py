from fastapi import APIRouter, UploadFile, File
from app.core.response import success, error, UnifiedResponse
from app.utils.oss import oss_uploader
from app.schemas.upload import ImageUploadResponse
import os

router = APIRouter()

@router.post("/image", response_model=UnifiedResponse[ImageUploadResponse], summary="上传图片到OSS")
async def upload_image(file: UploadFile = File(...)):
    """
    上传图片到阿里云OSS
    
    - 接收前端上传的图片文件
    - 将图片上传到OSS
    - 返回OSS的URL和文件信息
    - 此接口仅负责上传，不做车牌识别
    """
    # 验证文件类型
    if not file.content_type.startswith("image/"):
        return error(message="请上传图片文件")
    
    # 验证文件大小 (5MB)
    file_content = await file.read()
    file_size = len(file_content)
    
    if file_size > 5 * 1024 * 1024:  # 5MB
        return error(message="文件大小不能超过5MB")
    
    # 生成文件名
    import uuid
    file_ext = os.path.splitext(file.filename)[1]
    filename = f"lpr/upload/{uuid.uuid4()}{file_ext}"
    
    try:
        # 上传到OSS
        oss_url = oss_uploader.upload_file(file_content, filename)
        
        # 构造响应数据（转换为字典）
        response_data = {
            "url": oss_url,
            "filename": file.filename,
            "size": file_size,
            "content_type": file.content_type
        }
        
        return success(data=response_data, message="上传成功")
        
    except Exception as e:
        print(f"Upload error: {e}")
        return error(message=f"上传失败: {str(e)}")

