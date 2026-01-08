from pydantic import BaseModel
from typing import Optional

class RecognizeByUrlRequest(BaseModel):
    """通过URL识别车牌请求"""
    image_url: str

class ImageUploadResponse(BaseModel):
    """图片上传响应"""
    url: str
    filename: str
    size: int
    content_type: str
    
    class Config:
        from_attributes = True
