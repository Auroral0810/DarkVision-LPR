from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class AdminRoleDetail(BaseModel):
    """管理员角色详情"""
    id: int
    name: str
    display_name: Optional[str] = None

    class Config:
        from_attributes = True

class AdminUserListItem(BaseModel):
    """管理员看到的用户列表项（包含敏感信息）"""
    id: int
    phone: Optional[str] = None
    nickname: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    user_type: str  # free, vip, enterprise, admin
    status: str  # active, banned, pending
    last_login_at: Optional[datetime] = None
    last_login_ip: Optional[str] = None
    created_at: datetime
    is_online: bool = False
    
    # 封禁信息
    banned_reason: Optional[str] = None
    banned_until: Optional[datetime] = None
    
    # 角色与权限
    roles: List[AdminRoleDetail] = []
    is_admin: bool = False
    
    # 上级账号 (企业子账户使用)
    parent_id: Optional[int] = None
    parent_nickname: Optional[str] = None
    
    # 统计快照
    total_recognition_count: int = 0
    total_order_amount: float = 0.0
    
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
    banned_until: Optional[datetime] = Field(default=None, description="封禁截止时间，不传则永久封禁")


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
    deleted_at: Optional[datetime] = None
    is_deleted: bool = False
    
    # 封禁信息
    banned_reason: Optional[str] = None
    banned_until: Optional[datetime] = None
    
    # 会员信息
    membership_expires_at: Optional[datetime] = None
    
    # 上级账号信息
    parent_id: Optional[int] = None
    parent_nickname: Optional[str] = None
    sub_account_role: Optional[str] = None
    
    # 角色信息
    roles: List[AdminRoleDetail] = []
    is_admin: bool = False
    
    # 登录安全
    login_fail_count: int = 0
    
    # 统计信息
    total_recognition_count: int = 0
    total_order_amount: float = 0.0
    order_count: int = 0
    last_recognition_at: Optional[datetime] = None
    
    # 第三方绑定
    third_party_bindings: List[str] = []
    
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


class AdminUserCreate(BaseModel):
    """管理员创建用户"""
    nickname: str = Field(..., min_length=1, max_length=50)
    phone: str = Field(..., pattern=r'^1[3-9]\d{9}$')
    password: str = Field(..., min_length=6)
    email: Optional[str] = None
    user_type: str = "free"


class AdminUserUpdate(BaseModel):
    """管理员更新用户信息"""
    nickname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    user_type: Optional[str] = None
    status: Optional[str] = None


class AdminUpdateUserType(BaseModel):
    """修改用户类型"""
    user_type: str


class BatchDeleteRequest(BaseModel):
    """批量删除请求"""
    user_ids: List[int]


class ResetPasswordResponse(BaseModel):
    """重置密码响应"""
    new_password: str
