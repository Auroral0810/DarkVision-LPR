from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class ContactCreate(BaseModel):
    """创建咨询消息Schema"""
    name: str = Field(..., min_length=1, max_length=100, description="姓名")
    email: EmailStr = Field(..., description="邮箱")
    message: str = Field(..., min_length=1, max_length=2000, description="咨询内容")

class ContactResponse(BaseModel):
    """咨询消息响应Schema"""
    message: str = "提交成功"

