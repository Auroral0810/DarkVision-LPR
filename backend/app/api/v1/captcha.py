"""
图形验证码API
"""
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import uuid
import base64
import io
from app.core.response import success, UnifiedResponse
from app.schemas.captcha import CaptchaRequest, CaptchaResponse, CaptchaVerifyRequest
from app.services.captcha import captcha_service, CaptchaService
from app.core.exceptions import ParameterException

router = APIRouter()


@router.post("/captcha/generate", response_model=UnifiedResponse, summary="获取图形验证码", tags=["验证码"])
def generate_captcha(request: CaptchaRequest = CaptchaRequest()):
    """
    获取图形验证码
    
    **功能说明**:
    - 生成图形验证码并返回Base64编码的图片
    - 验证码在Redis中存储5分钟
    - 验证码为4位字符（数字+大写字母，排除易混淆字符）
    - 返回唯一的 captcha_id 用于后续验证
    
    **使用场景**:
    - 用户注册时
    - 用户登录时（可选）
    - 敏感操作验证
    
    **刷新验证码**:
    - 传入之前的 captcha_id 可清理旧验证码
    - 不传则生成新的 captcha_id
    
    **示例请求**:
    ```json
    {
      "captcha_id": "550e8400-e29b-41d4-a716-446655440000"  // 可选，刷新时传入
    }
    ```
    
    **示例响应**:
    ```json
    {
      "code": 20000,
      "message": "验证码生成成功",
      "data": {
        "captcha_id": "550e8400-e29b-41d4-a716-446655440000",
        "image_base64": "data:image/png;base64,iVBORw0KGgo...",
        "expire_seconds": 300
      }
    }
    ```
    """
    # 如果提供了旧的captcha_id，先删除旧验证码
    if request.captcha_id:
        captcha_service.delete_captcha(request.captcha_id)
    
    # 生成新的UUID作为验证码ID
    captcha_id = str(uuid.uuid4())
    
    # 生成验证码图片
    img_bytes, code = captcha_service.generate_captcha(captcha_id)
    
    # 将图片转换为Base64
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    image_data_url = f"data:image/png;base64,{img_base64}"
    
    return success(
        data={
            "captcha_id": captcha_id,
            "image_base64": image_data_url,
            "expire_seconds": CaptchaService.CAPTCHA_EXPIRE_TIME
        },
        message="验证码生成成功"
    )


@router.get("/captcha/image/{captcha_id}", summary="获取验证码图片（直接返回图片）", tags=["验证码"])
def get_captcha_image(captcha_id: str):
    """
    获取验证码图片（直接返回PNG图片）
    
    **说明**:
    - 直接返回PNG图片，可用于 <img> 标签的 src
    - 相比Base64方式，这个接口返回的是原始图片
    - 验证码ID在生成时获得
    
    **使用方式**:
    ```html
    <img src="http://localhost:8000/api/v1/captcha/image/{captcha_id}" />
    ```
    """
    # 生成新的验证码
    img_bytes, code = captcha_service.generate_captcha(captcha_id)
    
    # 返回图片流
    return StreamingResponse(
        io.BytesIO(img_bytes),
        media_type="image/png",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )


@router.post("/captcha/verify", response_model=UnifiedResponse, summary="验证图形验证码", tags=["验证码"])
def verify_captcha(request: CaptchaVerifyRequest):
    """
    验证图形验证码（在发送邮箱验证码前需校验图形验证码）
    
    **说明**:
    - 通常在注册/登录时会自动验证验证码
    - 这个接口可用于提前验证
    - 验证成功后验证码会被删除（一次性使用）
    
    **请求参数**:
    ```json
    {
      "captcha_id": "550e8400-e29b-41d4-a716-446655440000",
      "code": "AB3D"
    }
    ```
    
    **响应**:
    - 验证成功: code=20000
    - 验证失败: code=40003（参数错误）
    """
    if captcha_service.verify_captcha(request.captcha_id, request.code):
        return success(message="验证码正确")
    else:
        raise ParameterException("验证码错误或已过期")


@router.delete("/captcha/{captcha_id}", response_model=UnifiedResponse, summary="删除验证码", tags=["验证码"])
def delete_captcha(captcha_id: str):
    """
    删除验证码（清理）
    
    **说明**:
    - 用于清理不再使用的验证码
    - 通常在用户取消操作或切换页面时调用
    """
    captcha_service.delete_captcha(captcha_id)
    return success(message="验证码已删除")

