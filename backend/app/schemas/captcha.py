from pydantic import BaseModel, Field
from typing import Optional


class CaptchaRequest(BaseModel):
    """获取验证码请求"""
    captcha_id: Optional[str] = Field(None, description="验证码ID（刷新时传入）")
    
    class Config:
        json_schema_extra = {
            "example": {
                "captcha_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }


class CaptchaResponse(BaseModel):
    """验证码响应"""
    captcha_id: str = Field(..., description="验证码ID（用于验证）")
    image_base64: str = Field(..., description="Base64编码的图片")
    expire_seconds: int = Field(..., description="过期时间（秒）")
    
    class Config:
        json_schema_extra = {
            "example": {
                "captcha_id": "550e8400-e29b-41d4-a716-446655440000",
                "image_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
                "expire_seconds": 300
            }
        }


class CaptchaVerifyRequest(BaseModel):
    """验证验证码请求"""
    captcha_id: str = Field(..., description="验证码ID")
    code: str = Field(..., min_length=4, max_length=6, description="验证码")
    
    class Config:
        json_schema_extra = {
            "example": {
                "captcha_id": "550e8400-e29b-41d4-a716-446655440000",
                "code": "AB3D"
            }
        }

