from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class AdminUserListItem(BaseModel):
    """管理员看到的用户列表项（包含敏感信息）"""
    id: int
    phone: Optional[str] = None
    nickname: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    user_type: str  # free, vip, enterprise
    status: str  # active, banned, pending
    last_login_at: Optional[datetime] = None
    last_login_ip: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserListParams(BaseModel):
    """用户列表查询参数"""
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=10, ge=1, le=100, description="每页数量")
    keyword: Optional[str] = Field(default=None, description="搜索关键词（手机号/邮箱/昵称）")
    user_type: Optional[str] = Field(default=None, description="用户类型筛选")
    status: Optional[str] = Field(default=None, description="状态筛选")
    start_date: Optional[str] = Field(default=None, description="注册开始日期")
    end_date: Optional[str] = Field(default=None, description="注册结束日期")


class BanUserRequest(BaseModel):
    """封禁用户请求"""
    user_id: int
    reason: str = Field(..., min_length=1, max_length=500, description="封禁原因")
    ban_until: Optional[datetime] = Field(default=None, description="封禁截止时间，不传则永久封禁")


class AdminUserDetail(BaseModel):
    """管理员看到的用户详情（完整信息）"""
    id: int
    phone: Optional[str] = None
    nickname: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    user_type: str
    status: str
    is_verified: bool
    last_login_at: Optional[datetime] = None
    last_login_ip: Optional[str] = None
    login_count: int = 0
    registration_ip: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    # 会员信息
    membership_expires_at: Optional[datetime] = None
    
    # 统计信息
    total_recognition_count: int = 0
    
    class Config:
        from_attributes = True

class AdminSelfInfo(BaseModel):
    """管理员自己的信息（登录返回用）"""
    id: int
    phone: Optional[str] = None
    nickname: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    user_type: str
    status: str
    roles: List[str] = []
    perms: List[str] = []
    
    # 个人信息
    gender: Optional[str] = None
    birthday: Optional[str] = None  # YYYY-MM-DD
    address: Optional[str] = None
    real_name: Optional[str] = None
    
    # 实名认证状态
    is_verified: bool = False
    verification_status: Optional[str] = None
    
    # 时间信息
    created_at: datetime
    last_login_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
