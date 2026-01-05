from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.user import UserType, UserStatus


# ===== 注册相关 =====
class UserRegister(BaseModel):
    """用户注册（需要验证码）"""
    phone: str = Field(..., min_length=11, max_length=11, pattern="^1[3-9]\d{9}$")
    sms_code: str = Field(..., min_length=6, max_length=6, description="短信验证码")
    nickname: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=6, max_length=20)
    email: Optional[EmailStr] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone": "13800138000",
                "sms_code": "123456",
                "nickname": "新用户",
                "password": "123456",
                "email": "user@example.com"
            }
        }


# ===== 登录相关 =====
class UserLoginByPhone(BaseModel):
    """手机号登录"""
    phone: str = Field(..., min_length=11, max_length=11)
    password: Optional[str] = Field(None, min_length=6)
    sms_code: Optional[str] = Field(None, min_length=6, max_length=6)
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone": "13800138000",
                "password": "123456"  # 或使用 sms_code
            }
        }


class UserLoginByEmail(BaseModel):
    """邮箱登录"""
    email: EmailStr
    password: Optional[str] = Field(None, min_length=6)
    email_code: Optional[str] = Field(None, min_length=6, max_length=6)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "123456"  # 或使用 email_code
            }
        }


class SMSCodeRequest(BaseModel):
    """请求短信验证码"""
    phone: str = Field(..., min_length=11, max_length=11, pattern="^1[3-9]\d{9}$")
    scene: str = Field(..., description="使用场景: login/register/reset_password")


class EmailCodeRequest(BaseModel):
    """请求邮箱验证码"""
    email: EmailStr
    scene: str = Field(..., description="使用场景: login/register/reset_password")


# ===== Token响应 =====
class Token(BaseModel):
    """Token响应"""
    access_token: str
    token_type: str = "bearer"


# ===== 用户信息响应 =====
class UserBasicInfo(BaseModel):
    """用户基本信息"""
    id: int
    phone: str
    nickname: str
    email: Optional[str]
    avatar_url: Optional[str]
    user_type: UserType
    status: UserStatus
    
    class Config:
        from_attributes = True


class UserDetailInfo(UserBasicInfo):
    """用户详细信息（包含会员和统计）"""
    # 会员信息
    membership_type: Optional[str] = None
    membership_expire_date: Optional[datetime] = None
    is_membership_active: bool = False
    
    # 识别额度
    daily_quota: int = 0
    used_quota_today: int = 0
    remaining_quota_today: int = 0
    
    # 实名认证状态
    is_verified: bool = False
    real_name: Optional[str] = None
    
    # 企业信息
    is_enterprise_main: bool = False
    sub_account_count: int = 0
    
    # 时间信息
    created_at: datetime
    last_login_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """登录响应"""
    access_token: str
    token_type: str = "bearer"
    user_info: UserDetailInfo


# ===== Token数据（JWT payload）=====
class TokenData(BaseModel):
    """Token数据"""
    user_id: Optional[int] = None
    phone: Optional[str] = None
    user_type: Optional[str] = None


# ===== 密码相关 =====
class PasswordChange(BaseModel):
    """修改密码"""
    old_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6, max_length=20)
    confirm_password: str = Field(..., min_length=6, max_length=20)


class PasswordReset(BaseModel):
    """重置密码（通过验证码）"""
    phone: str = Field(..., min_length=11, max_length=11)
    sms_code: str = Field(..., min_length=6, max_length=6)
    new_password: str = Field(..., min_length=6, max_length=20)
