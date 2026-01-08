from sqlalchemy import Column, BigInteger, String, Enum, DateTime, Text, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum
# Note: AdminRole relationship usage relies on string reference or subsequent imports.


class UserType(str, enum.Enum):
    """用户类型枚举（值必须与数据库一致）"""
    FREE = "free"
    VIP = "vip"
    ENTERPRISE = "enterprise"
    ADMIN = "admin"

class UserStatus(str, enum.Enum):
    """用户状态枚举（值必须与数据库一致）"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"

class User(Base):
    __tablename__ = "users"
    
    id = Column(BigInteger, primary_key=True, index=True)
    phone = Column(String(11), unique=True, nullable=True, index=True, comment="手机号")
    nickname = Column(String(50), unique=True, nullable=False, index=True, comment="昵称")
    email = Column(String(100), unique=True, nullable=True, comment="邮箱")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    avatar_url = Column(String(255), nullable=True, comment="头像URL")
    user_type = Column(Enum(UserType, native_enum=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False, default=UserType.FREE, comment="用户类型")
    parent_id = Column(BigInteger, ForeignKey("users.id"), nullable=True, comment="企业主账户ID")
    status = Column(Enum(UserStatus, native_enum=False, values_callable=lambda obj: [e.value for e in obj]), nullable=False, default=UserStatus.ACTIVE, comment="状态")
    banned_reason = Column(Text, nullable=True, comment="封禁原因")
    banned_until = Column(DateTime, nullable=True, comment="封禁到期时间")
    last_login_at = Column(DateTime, nullable=True, comment="最后登录时间")
    last_login_ip = Column(String(45), nullable=True, comment="最后登录IP")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    deleted_at = Column(DateTime, nullable=True, comment="软删除时间")
    
    # 关系
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    membership = relationship("UserMembership", back_populates="user", uselist=False)
    real_name_verification = relationship("RealNameVerification", back_populates="user", uselist=False, foreign_keys="[RealNameVerification.user_id]")
    admin_roles = relationship("AdminRole", back_populates="user")
    third_party_logins = relationship("ThirdPartyLogin", back_populates="user")
    
    @property
    def is_verified(self) -> bool:
        """是否已通过实名认证"""
        return self.real_name_verification and self.real_name_verification.status == "approved"

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    real_name = Column(String(50), nullable=True, comment="真实姓名")
    id_card_number = Column(String(18), nullable=True, comment="身份证号")
    gender = Column(Enum("male", "female", "unknown"), nullable=True, comment="性别")
    birthday = Column(DateTime, nullable=True, comment="生日")
    address = Column(Text, nullable=True, comment="地址")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="profile")

class UserMembership(Base):
    __tablename__ = "user_memberships"
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    # membership_type 字段已废弃，改为关联 packages 表
    # membership_type = Column(Enum("free", "vip_monthly", "vip_yearly", "enterprise_custom"), nullable=False)
    package_id = Column(BigInteger, ForeignKey("packages.id"), nullable=False, default=1) # Default to free package ID 1
    start_date = Column(DateTime, nullable=False)
    expire_date = Column(DateTime, nullable=True, comment="永久为NULL")
    is_active = Column(BigInteger, nullable=False, default=1)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="membership")
    package = relationship("app.models.payment.Package", back_populates="memberships")
    
    @property
    def membership_type(self):
        """兼容旧代码：返回套餐代码"""
        if self.package:
            return self.package.code
        return "free"


class SubAccount(Base):
    """企业子账户"""
    __tablename__ = "sub_accounts"
    
    id = Column(BigInteger, primary_key=True, index=True)
    enterprise_user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, comment="企业主账户ID")
    sub_user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, comment="子账户用户ID")
    role = Column(Enum("admin", "operator", "viewer"), nullable=False, default="operator", comment="权限级别")
    quota_daily = Column(Integer, nullable=True, comment="每日识别限额")
    created_at = Column(DateTime, server_default=func.now())


class RealNameVerification(Base):
    """实名认证"""
    __tablename__ = "real_name_verifications"
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), unique=True, nullable=False)
    id_card_front = Column(String(255), nullable=False, comment="身份证正面")
    id_card_back = Column(String(255), nullable=False, comment="身份证反面")
    face_photo = Column(String(255), nullable=True, comment="人脸照片")
    status = Column(Enum("pending", "approved", "rejected"), nullable=False, default="pending")
    reject_reason = Column(Text, nullable=True)
    reviewed_by = Column(BigInteger, ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    user = relationship("User", back_populates="real_name_verification", foreign_keys=[user_id])
    reviewer = relationship("User", foreign_keys=[reviewed_by])

class ThirdPartyLogin(Base):
    """第三方登录绑定"""
    __tablename__ = "third_party_logins"
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    provider = Column(Enum("wechat", "qq", "github", "google", "weibo"), nullable=False)
    open_id = Column(String(255), nullable=False)
    union_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    user = relationship("User", back_populates="third_party_logins")

class LoginLog(Base):
    """登录日志"""
    __tablename__ = "login_logs"
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    success = Column(Boolean, nullable=False, default=False)
    failure_reason = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), index=True)
    
    user = relationship("User")
