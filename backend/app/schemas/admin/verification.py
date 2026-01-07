from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.schemas.admin.user import AdminUserListItem

# Reuse or define minimal user info for the list
class VerificationUserSimple(BaseModel):
    id: int
    nickname: str
    phone: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None

class VerificationListItem(BaseModel):
    """实名认证列表项"""
    id: int
    user_id: int
    user: VerificationUserSimple
    
    # 认证信息
    real_name: Optional[str] = None
    id_card_number: Optional[str] = None
    
    # 图片信息
    id_card_front: str
    id_card_back: str
    face_photo: Optional[str] = None
    
    status: str
    reject_reason: Optional[str] = None
    
    created_at: datetime
    updated_at: Optional[datetime] = None
    reviewed_at: Optional[datetime] = None
    reviewer_id: Optional[int] = None

    class Config:
        from_attributes = True

class VerificationAuditRequest(BaseModel):
    """审核操作请求"""
    action: str = Field(..., description="approve 或 reject")
    reject_reason: Optional[str] = Field(None, description="驳回原因，reject时必填")

class VerificationListParams(BaseModel):
    page: int = 1
    page_size: int = 10
    status: Optional[str] = None # pending, approved, rejected
    keyword: Optional[str] = None # 搜索昵称或手机号
