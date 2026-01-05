from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from typing import Optional
from app.models.user import User, UserType, UserStatus, UserProfile, UserMembership
from app.core.security import verify_password, get_password_hash, create_access_token
from app.schemas.user import (
    UserRegister, UserLoginByPhone, UserLoginByEmail,
    UserDetailInfo
)
from app.core.cache import get_redis
from app.core.logger import logger
from app.core.exceptions import (
    PhoneExistedException,
    EmailExistedException,
    UserNotFoundException,
    WrongPasswordException,
    UserBannedException,
    UserExistedException,
    ParameterException
)
from app.services.verification import verification_service
import re
import json


def register_user(db: Session, user_data: UserRegister) -> User:
    """
    用户注册（需要验证码）
    
    Args:
        db: 数据库会话
        user_data: 注册信息
        
    Returns:
        User: 创建的用户对象
        
    Raises:
        PhoneExistedException: 手机号已存在
        EmailExistedException: 邮箱已存在
        UserExistedException: 昵称已存在
        ParameterException: 参数错误或验证码错误
    """
    # 验证手机号格式
    if not re.match(r"^1[3-9]\d{9}$", user_data.phone):
        raise ParameterException("手机号格式不正确")
    
    # 验证短信验证码
    if not verification_service.verify_code("register", user_data.phone, user_data.sms_code):
        raise ParameterException("验证码错误或已过期")
    
    # 检查手机号是否已存在
    existing_user = db.query(User).filter(User.phone == user_data.phone).first()
    if existing_user:
        raise PhoneExistedException()
    
    # 检查昵称是否已存在
    existing_nickname = db.query(User).filter(User.nickname == user_data.nickname).first()
    if existing_nickname:
        raise UserExistedException("昵称已被使用")
    
    # 如果提供了邮箱，检查邮箱是否已存在
    if user_data.email:
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise EmailExistedException()
    
    # 创建用户（只能注册为普通用户 FREE）
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        phone=user_data.phone,
        nickname=user_data.nickname,
        email=user_data.email,
        password_hash=hashed_password,
        user_type=UserType.FREE,
        status=UserStatus.ACTIVE,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # 创建用户档案
    user_profile = UserProfile(
        user_id=new_user.id,
        created_at=datetime.now()
    )
    db.add(user_profile)
    
    # 创建会员记录（FREE用户默认配置）
    user_membership = UserMembership(
        user_id=new_user.id,
        membership_type="free",
        start_date=datetime.now(),
        expire_date=None,  # 免费用户无过期时间
        is_active=True,
        created_at=datetime.now()
    )
    db.add(user_membership)
    
    db.commit()
    
    # 发送欢迎邮件（异步，失败不影响注册）
    if user_data.email:
        try:
            from app.services.email import email_service
            email_service.send_welcome_email(user_data.email, user_data.nickname)
        except Exception as e:
            logger.warning(f"Failed to send welcome email: {e}")
    
    logger.info(f"User registered: {new_user.phone} (id: {new_user.id})")
    
    return new_user


def authenticate_by_phone_password(db: Session, login_data: UserLoginByPhone) -> User:
    """手机号+密码登录"""
    user = db.query(User).filter(User.phone == login_data.phone).first()
    if not user:
        raise WrongPasswordException()
    
    if not verify_password(login_data.password, user.password_hash):
        raise WrongPasswordException()
    
    return user


def authenticate_by_phone_code(db: Session, login_data: UserLoginByPhone) -> User:
    """手机号+验证码登录"""
    # 验证验证码
    if not verification_service.verify_code("login", login_data.phone, login_data.sms_code):
        raise ParameterException("验证码错误或已过期")
    
    # 查找用户
    user = db.query(User).filter(User.phone == login_data.phone).first()
    if not user:
        raise UserNotFoundException("用户不存在")
    
    return user


def authenticate_by_email_password(db: Session, login_data: UserLoginByEmail) -> User:
    """邮箱+密码登录"""
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        raise WrongPasswordException()
    
    if not verify_password(login_data.password, user.password_hash):
        raise WrongPasswordException()
    
    return user


def authenticate_by_email_code(db: Session, login_data: UserLoginByEmail) -> User:
    """邮箱+验证码登录"""
    # 验证验证码
    if not verification_service.verify_code("login", login_data.email, login_data.email_code):
        raise ParameterException("验证码错误或已过期")
    
    # 查找用户
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        raise UserNotFoundException("用户不存在")
    
    return user


def check_user_status(user: User):
    """检查用户状态"""
    if user.status == UserStatus.BANNED:
        raise UserBannedException()
    
    # 可以添加更多状态检查


def update_login_info(db: Session, user: User, ip_address: Optional[str] = None):
    """更新登录信息"""
    user.last_login_at = datetime.now()
    if ip_address:
        user.last_login_ip = ip_address
    db.commit()


def get_user_detail_info(db: Session, user_id: int) -> UserDetailInfo:
    """
    获取用户详细信息（包含会员、额度、认证状态等）
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        
    Returns:
        UserDetailInfo: 用户详细信息
    """
    # 先尝试从 Redis 缓存获取
    redis_client = get_redis()
    cache_key = f"user_detail:{user_id}"
    
    if redis_client:
        cached_data = redis_client.get(cache_key)
        if cached_data:
            try:
                data = json.loads(cached_data.decode('utf-8'))
                logger.info(f"User detail loaded from cache: {user_id}")
                return UserDetailInfo(**data)
            except Exception as e:
                logger.warning(f"Failed to load user detail from cache: {e}")
    
    # 缓存未命中，从数据库查询
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException()
    
    # 获取会员信息
    membership = db.query(UserMembership).filter(
        UserMembership.user_id == user_id,
        UserMembership.is_active == True
    ).first()
    
    # 获取今日已用额度
    from app.models.recognition import RecognitionRecord
    today = date.today()
    used_quota_today = db.query(func.count(RecognitionRecord.id)).filter(
        RecognitionRecord.user_id == user_id,
        func.date(RecognitionRecord.created_at) == today
    ).scalar() or 0
    
    # 根据用户类型设置每日额度
    daily_quota_map = {
        UserType.FREE: 10,
        UserType.VIP: 100,
        UserType.ENTERPRISE: 1000,
        UserType.ADMIN: 999999
    }
    daily_quota = daily_quota_map.get(user.user_type, 10)
    
    # 检查实名认证状态
    from app.models.user import RealNameVerification
    verification = db.query(RealNameVerification).filter(
        RealNameVerification.user_id == user_id,
        RealNameVerification.status == "approved"
    ).first()
    
    is_verified = verification is not None
    real_name = None
    if verification and hasattr(verification, 'real_name'):
        # 从 user_profiles 表获取
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        real_name = profile.real_name if profile else None
    
    # 检查是否是企业主账户
    from app.models.user import SubAccount
    is_enterprise_main = user.user_type == UserType.ENTERPRISE
    sub_account_count = 0
    if is_enterprise_main:
        sub_account_count = db.query(func.count(SubAccount.id)).filter(
            SubAccount.enterprise_user_id == user_id
        ).scalar() or 0
    
    # 构建详细信息
    user_detail = UserDetailInfo(
        id=user.id,
        phone=user.phone,
        nickname=user.nickname,
        email=user.email,
        avatar_url=user.avatar_url,
        user_type=user.user_type,
        status=user.status,
        membership_type=membership.membership_type if membership else "free",
        membership_expire_date=membership.expire_date if membership else None,
        is_membership_active=membership.is_active if membership else False,
        daily_quota=daily_quota,
        used_quota_today=used_quota_today,
        remaining_quota_today=max(0, daily_quota - used_quota_today),
        is_verified=is_verified,
        real_name=real_name,
        is_enterprise_main=is_enterprise_main,
        sub_account_count=sub_account_count,
        created_at=user.created_at,
        last_login_at=user.last_login_at
    )
    
    # 缓存到 Redis（5分钟）
    if redis_client:
        try:
            cache_data = user_detail.model_dump(mode='json')
            # 处理 datetime 序列化
            for key, value in cache_data.items():
                if isinstance(value, datetime):
                    cache_data[key] = value.isoformat()
            redis_client.setex(cache_key, 300, json.dumps(cache_data))
            logger.info(f"User detail cached: {user_id}")
        except Exception as e:
            logger.warning(f"Failed to cache user detail: {e}")
    
    return user_detail


def create_user_token(user: User) -> str:
    """
    创建用户访问令牌
    
    Args:
        user: 用户对象
        
    Returns:
        str: JWT token
    """
    token_data = {
        "user_id": user.id,
        "phone": user.phone,
        "user_type": user.user_type.value
    }
    access_token = create_access_token(data=token_data)
    
    # 将token存入Redis
    redis_client = get_redis()
    if redis_client:
        token_key = f"user_token:{user.id}"
        redis_client.setex(token_key, 7 * 24 * 3600, access_token)
    
    return access_token


def get_user_by_id(db: Session, user_id: int) -> User:
    """根据ID获取用户"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException()
    return user


def logout_user(user_id: int) -> bool:
    """
    用户登出
    
    Args:
        user_id: 用户ID
        
    Returns:
        bool: 是否成功
    """
    redis_client = get_redis()
    if redis_client:
        # 删除 token
        token_key = f"user_token:{user_id}"
        redis_client.delete(token_key)
        
        # 删除用户详情缓存
        detail_key = f"user_detail:{user_id}"
        redis_client.delete(detail_key)
        
        logger.info(f"User logged out: {user_id}")
    
    return True


def invalidate_user_cache(user_id: int):
    """使用户缓存失效"""
    redis_client = get_redis()
    if redis_client:
        detail_key = f"user_detail:{user_id}"
        redis_client.delete(detail_key)
        logger.info(f"User cache invalidated: {user_id}")
