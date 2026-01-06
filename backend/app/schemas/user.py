from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from datetime import datetime
from app.models.user import UserType, UserStatus


# ===== 注册相关 =====
class UserRegister(BaseModel):
    """用户注册（支持手机或邮箱）"""
    phone: Optional[str] = Field(None, min_length=11, max_length=11, pattern="^1[3-9]\d{9}$")
    sms_code: Optional[str] = Field(None, min_length=6, max_length=6, description="短信验证码")
    email: Optional[EmailStr] = None
    email_code: Optional[str] = Field(None, min_length=6, max_length=6, description="邮箱验证码")
    nickname: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=6, max_length=20)
    
    @model_validator(mode='after')
    def validate_register_method(self):
        if not self.phone and not self.email:
            raise ValueError("必须提供手机号或邮箱")
        
        if self.phone and not self.sms_code:
            raise ValueError("使用手机号注册必须提供短信验证码")
            
        if self.email and not self.email_code and not self.phone:
            # 如果只提供邮箱，必须提供邮箱验证码
            # 如果提供了手机号（作为主账号），邮箱可以是附加信息，不需要验证码（或者视业务逻辑而定）
            # 这里简化逻辑：如果作为注册账号，必须验证
            raise ValueError("使用邮箱注册必须提供邮箱验证码")
            
        return self
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone": "13800138000",
                "sms_code": "123456",
                "nickname": "新用户",
                "password": "123456"
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
    phone: Optional[str] = None
    nickname: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None
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
    account: str = Field(..., description="手机号或邮箱")
    code: str = Field(..., min_length=6, max_length=6, description="验证码")
    new_password: str = Field(..., min_length=6, max_length=20)
    confirm_password: str = Field(..., min_length=6, max_length=20)


# ===== 用户信息更新 =====
class UserProfileUpdate(BaseModel):
    """更新用户基本信息"""
    nickname: Optional[str] = Field(None, min_length=2, max_length=50)
    avatar_url: Optional[str] = None
    gender: Optional[str] = Field(None, pattern="^(male|female|unknown)$")
    birthday: Optional[str] = None  # YYYY-MM-DD格式
    address: Optional[str] = None  # 省/市/区/详细地址
