from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class ResetPasswordRequest(BaseModel):
    """重置密码请求 Schema"""
    account: str = Field(..., description="手机号或邮箱")
    code: str = Field(..., min_length=6, max_length=6, description="验证码")
    new_password: str = Field(..., min_length=6, max_length=20, description="新密码")
    confirm_password: str = Field(..., min_length=6, max_length=20, description="确认新密码")

