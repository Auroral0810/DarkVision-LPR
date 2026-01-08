from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ThirdPartyBinding(BaseModel):
    """第三方账号绑定信息"""
    provider: str
    bound: bool
    nickname: Optional[str] = None
    open_id: Optional[str] = None
    created_at: Optional[datetime] = None

class MembershipBenefit(BaseModel):
    """会员权益信息"""
    membership_type: str
    membership_name: str
    expire_date: Optional[datetime] = None
    is_active: bool
    
    # 具体权益
    daily_quota: int = 10
    batch_recognition: bool = False
    video_recognition: bool = False
    api_access: bool = False
    cloud_storage: bool = False
    
    # 描述文本
    description: str = ""

class UserSettingsOut(BaseModel):
    """账户设置全量信息"""
    # 1. 基本信息
    id: int
    nickname: str
    phone: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    gender: str = "unknown"
    birthday: Optional[str] = None
    address: Optional[str] = None
    
    # 2. 实名认证
    is_verified: bool
    verification_status: str  # pending, approved, rejected, none
    real_name: Optional[str] = None
    id_card_number: Optional[str] = None
    reject_reason: Optional[str] = None
    
    # 3. 第三方绑定
    third_party_bindings: List[ThirdPartyBinding] = []
    
    # 4. 会员权益
    membership_benefits: MembershipBenefit
    
    class Config:
        from_attributes = True
