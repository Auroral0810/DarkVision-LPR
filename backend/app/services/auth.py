from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, date, timedelta
from typing import Optional
from app.models.user import User, UserType, UserStatus, UserProfile, UserMembership, LoginLog
from app.models.recognition import RecognitionTask, RecognitionRecord
from app.core.security import verify_password, get_password_hash, create_access_token
from app.schemas.user import (
    UserRegister, UserLoginByPhone, UserLoginByEmail,
    UserDetailInfo, PasswordChange, RecentRecognitionRecord, RecognitionStats, 
    RealNameVerificationSubmit
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
from app.utils.oss import oss_uploader
import re
import json


def register_user(db: Session, user_data: UserRegister) -> User:
    """
    用户注册（支持手机或邮箱）
    
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
    # 1. 验证手机号注册逻辑
    if user_data.phone:
        # 验证手机号格式
        if not re.match(r"^1[3-9]\d{9}$", user_data.phone):
            raise ParameterException("手机号格式不正确")
        
        # 验证短信验证码
        if not user_data.sms_code:
            raise ParameterException("手机号注册必须提供短信验证码")
            
        if not verification_service.verify_code("register", user_data.phone, user_data.sms_code):
            raise ParameterException("短信验证码错误或已过期")
    
        # 检查手机号是否已存在
        existing_user = db.query(User).filter(User.phone == user_data.phone).first()
        if existing_user:
            raise PhoneExistedException()

    # 2. 验证邮箱注册逻辑
    if user_data.email:
        # 如果是纯邮箱注册（无手机号），必须验证邮箱验证码
        if not user_data.phone:
            if not user_data.email_code:
                raise ParameterException("邮箱注册必须提供邮箱验证码")
                
            if not verification_service.verify_code("register", user_data.email, user_data.email_code):
                raise ParameterException("邮箱验证码错误或已过期")
        
        # 检查邮箱是否已存在
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise EmailExistedException()

    # 3. 检查昵称是否已存在
    existing_nickname = db.query(User).filter(User.nickname == user_data.nickname).first()
    if existing_nickname:
        raise UserExistedException("昵称已被使用")
    
    # 4. 创建用户（只能注册为普通用户 FREE）
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
    
    identifier = user_data.phone or user_data.email
    logger.info(f"User registered: {identifier} (id: {new_user.id})")
    
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
    
    # 设置用户在线状态
    from app.services.online_user_service import set_user_online
    set_user_online(user.id)


from app.schemas.password import ResetPasswordRequest
from app.core.exceptions import ResourceNotFoundException, VerificationException

def reset_password(db: Session, reset_data: ResetPasswordRequest) -> User:
    """
    重置用户密码
    
    Args:
        db: 数据库会话
        reset_data: 重置密码请求数据
        
    Returns:
        User: 更新后的用户对象
        
    Raises:
        ParameterException: 参数错误
        ResourceNotFoundException: 用户不存在
        VerificationException: 验证码错误
    """
    # 1. 验证两次密码是否一致
    if reset_data.new_password != reset_data.confirm_password:
        raise ParameterException("两次输入的密码不一致")
        
    # 2. 判断账号类型 (手机/邮箱) 并验证验证码
    is_email = '@' in reset_data.account
    scene = "reset_password"
    
    user = None
    if is_email:
        # 验证邮箱验证码
        if not verification_service.verify_code(scene, reset_data.account, reset_data.code):
            raise VerificationException("验证码无效或已过期")
        # 查找用户
        user = db.query(User).filter(User.email == reset_data.account).first()
    else:
        # 验证短信验证码
        if not verification_service.verify_code(scene, reset_data.account, reset_data.code):
            raise VerificationException("验证码无效或已过期")
        # 查找用户
        user = db.query(User).filter(User.phone == reset_data.account).first()
        
    if not user:
        raise ResourceNotFoundException("该账号未注册")
        
    # 3. 更新密码
    user.password_hash = get_password_hash(reset_data.new_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # 4. 清除用户所有登录 Token (登出)
    logout_user(user.id)
    
    return user

def update_password(db: Session, user_id: int, password_data: PasswordChange) -> User:
    """
    修改密码（需要旧密码）
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        password_data: 密码修改信息
        
    Returns:
        User: 更新后的用户对象
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException()
    
    # 验证旧密码
    if not verify_password(password_data.old_password, user.password_hash):
        raise ParameterException("旧密码错误")
        
    # 验证新密码一致性 (Schema层面已有部分校验，这里再次确认业务逻辑)
    if password_data.new_password != password_data.confirm_password:
        raise ParameterException("两次输入的密码不一致")
        
    if password_data.old_password == password_data.new_password:
        raise ParameterException("新密码不能与旧密码相同")
        
    # 更新密码
    user.password_hash = get_password_hash(password_data.new_password)
    db.commit()
    db.refresh(user)
    
    # 清除用户所有登录 Token (强制下线)
    logout_user(user.id)
    
    return user


def get_recent_recognition_records(db: Session, user_id: int, limit: int = 5) -> list[RecentRecognitionRecord]:
    """
    获取用户最近的识别记录
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        limit: 返回记录数量，默认5条
        
    Returns:
        list[RecentRecognitionRecord]: 识别记录列表
    """
    try:
        # 查询最近的识别结果
        results = db.query(RecognitionRecord).filter(
            RecognitionRecord.user_id == user_id,
            RecognitionRecord.is_deleted == False
        ).order_by(
            RecognitionRecord.processed_at.desc()
        ).limit(limit).all()
        
        # 辅助函数：生成签名URL
        def get_signed_url(url: Optional[str]) -> Optional[str]:
            if not url or 'oss-accesspoint.aliyuncs.com' not in url:
                return url
            try:
                from app.utils.oss import oss_uploader
                import re
                match = re.search(r'oss-accesspoint\.aliyuncs\.com/(.+)', url)
                if match:
                    object_key = match.group(1)
                    return oss_uploader.generate_presigned_url(object_key, expires=86400)
            except Exception as e:
                logger.warning(f"Failed to generate presigned URL for image: {e}")
            return url
        
        records = []
        for result in results:
            # 映射车牌类型
            plate_type_map = {
                'blue': '蓝牌',
                'yellow': '黄牌',
                'green': '绿牌',
                'white': '白牌',
                'other': '其他'
            }
            plate_type = plate_type_map.get(result.plate_type, '其他')
            
            # 格式化时间
            date_str = result.processed_at.strftime('%Y-%m-%d %H:%M:%S') if result.processed_at else ''
            
            # 置信度转为百分比
            confidence = round(float(result.confidence) * 100, 1) if result.confidence else 0.0
            
            # 生成签名URL
            signed_image_url = get_signed_url(result.original_image_url)
            
            records.append(RecentRecognitionRecord(
                id=result.id,
                date=date_str,
                plate=result.license_plate or '',
                type=plate_type,
                confidence=confidence,
                image_url=signed_image_url
            ))
        
        return records
    except Exception as e:
        logger.error(f"Failed to get recent recognition records for user {user_id}: {e}")
        return []


def get_recognition_stats(db: Session, user_id: int) -> RecognitionStats:
    """
    获取用户识别成功率统计
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        
    Returns:
        RecognitionStats: 识别统计数据
    """
    try:
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        # 今日统计
        today_tasks = db.query(RecognitionTask).filter(
            RecognitionTask.user_id == user_id,
            func.date(RecognitionTask.created_at) == today
        ).all()
        
        today_total = len(today_tasks)
        today_success = sum(1 for task in today_tasks if task.status == 'completed')
        success_rate_today = round((today_success / today_total * 100), 1) if today_total > 0 else 0.0
        
        # 昨日统计
        yesterday_tasks = db.query(RecognitionTask).filter(
            RecognitionTask.user_id == user_id,
            func.date(RecognitionTask.created_at) == yesterday
        ).all()
        
        yesterday_total = len(yesterday_tasks)
        yesterday_success = sum(1 for task in yesterday_tasks if task.status == 'completed')
        success_rate_yesterday = round((yesterday_success / yesterday_total * 100), 1) if yesterday_total > 0 else 0.0
        
        # 计算变化
        rate_change = round(success_rate_today - success_rate_yesterday, 1)
        
        return RecognitionStats(
            success_rate_today=success_rate_today,
            success_rate_yesterday=success_rate_yesterday,
            rate_change=rate_change
        )
    except Exception as e:
        logger.error(f"Failed to get recognition stats for user {user_id}: {e}")
        # 返回默认值
        return RecognitionStats(
            success_rate_today=0.0,
            success_rate_yesterday=0.0,
            rate_change=0.0
        )


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
                data = json.loads(cached_data)
                # logger.info(f"User detail loaded from cache: {user_id}")
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
        RealNameVerification.user_id == user_id
    ).first()
    
    is_verified = (verification.status == "approved") if verification else False
    verification_status = verification.status if verification else None
    reject_reason = verification.reject_reason if verification else None
    
    # 获取原始照片URL
    id_card_front = verification.id_card_front if verification else None
    id_card_back = verification.id_card_back if verification else None
    face_photo = verification.face_photo if verification else None
    
    # 获取用户Profile信息
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    real_name = profile.real_name if profile else None
    gender = profile.gender if profile else None
    birthday = profile.birthday.strftime('%Y-%m-%d') if profile and profile.birthday else None
    address = profile.address if profile else None
    
    # 检查是否是企业主账户
    from app.models.user import SubAccount
    is_enterprise_main = user.user_type == UserType.ENTERPRISE
    sub_account_count = 0
    if is_enterprise_main:
        sub_account_count = db.query(func.count(SubAccount.id)).filter(
            SubAccount.enterprise_user_id == user_id
        ).scalar() or 0
    
    # 处理OSS URL：生成带签名的临时访问URL
    def get_signed_url(url: Optional[str]) -> Optional[str]:
        if not url or 'oss-accesspoint.aliyuncs.com' not in url:
            return url
        try:
            from app.utils.oss import oss_uploader
            match = re.search(r'oss-accesspoint\.aliyuncs\.com/(.+)', url)
            if match:
                object_key = match.group(1)
                return oss_uploader.generate_presigned_url(object_key, expires=86400)
        except Exception as e:
            logger.warning(f"Failed to generate presigned URL: {e}")
        return url

    avatar_display_url = get_signed_url(user.avatar_url)
    id_card_front_url = get_signed_url(id_card_front)
    id_card_back_url = get_signed_url(id_card_back)
    face_photo_url = get_signed_url(face_photo)
    
    # 获取最近识别记录（实时数据，不缓存）
    recent_records = get_recent_recognition_records(db, user_id, limit=5)
    
    # 获取识别成功率统计（实时数据，不缓存）
    recognition_stats = get_recognition_stats(db, user_id)
    
    # 获取用户角色（临时逻辑：根据 user_type 映射，后期改为查询 admin_roles 表）
    roles = []
    if user.user_type == UserType.ADMIN:
        roles = ["ROOT"]
    elif user.user_type == UserType.ENTERPRISE:
        roles = ["ENTERPRISE"]
    else:
        roles = ["USER"]
    
    # 构建详细信息
    user_detail = UserDetailInfo(
        id=user.id,
        phone=user.phone,
        nickname=user.nickname,
        email=user.email,
        avatar_url=avatar_display_url,
        user_type=user.user_type,
        status=user.status,
        roles=roles,
        membership_type=membership.membership_type if membership else "free",
        membership_expire_date=membership.expire_date if membership else None,
        is_membership_active=membership.is_active if membership else False,
        gender=gender,
        birthday=birthday,
        address=address,
        daily_quota=daily_quota,
        used_quota_today=used_quota_today,
        remaining_quota_today=max(0, daily_quota - used_quota_today),
        is_verified=is_verified,
        verification_status=verification_status,
        id_card_front=id_card_front_url,
        id_card_back=id_card_back_url,
        face_photo=face_photo_url,
        reject_reason=reject_reason,
        real_name=real_name,
        is_enterprise_main=is_enterprise_main,
        sub_account_count=sub_account_count,
        created_at=user.created_at,
        last_login_at=user.last_login_at,
        recent_records=recent_records,
        recognition_stats=recognition_stats
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
            # logger.info(f"User detail cached: {user_id}")
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


def update_user_profile(db: Session, user_id: int, profile_data: dict) -> User:
    """
    更新用户基本信息
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        profile_data: 要更新的字段字典
        
    Returns:
        User: 更新后的用户对象
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException()
    
    # 更新用户表字段
    if 'nickname' in profile_data and profile_data['nickname']:
        # 检查昵称是否已被其他用户使用
        existing = db.query(User).filter(
            User.nickname == profile_data['nickname'],
            User.id != user_id
        ).first()
        if existing:
            raise ParameterException("昵称已被使用")
        user.nickname = profile_data['nickname']
    
    if 'avatar_url' in profile_data:
        user.avatar_url = profile_data['avatar_url']
    
    # 更新用户扩展信息表
    from app.models.user import UserProfile
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        profile = UserProfile(user_id=user_id)
        db.add(profile)
    
    if 'gender' in profile_data and profile_data['gender']:
        profile.gender = profile_data['gender']
    
    if 'birthday' in profile_data:
        if profile_data['birthday']:
            from datetime import datetime
            try:
                profile.birthday = datetime.strptime(profile_data['birthday'], '%Y-%m-%d')
            except ValueError:
                raise ParameterException("生日格式错误，应为YYYY-MM-DD")
        else:
            profile.birthday = None
    
    if 'address' in profile_data:
        profile.address = profile_data['address']
    
    db.commit()
    db.refresh(user)
    
    # 清除用户信息缓存
    redis_client = get_redis()
    if redis_client:
        cache_key = f"user_detail:{user_id}"
        redis_client.delete(cache_key)
    
    return user


def get_user_by_id(db: Session, user_id: int) -> User:
    """根据ID获取用户"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException()
    return user


def logout_user(user_id: int) -> bool:
    """
    用户登出 - 清除所有 Redis 缓存数据
    
    Args:
        user_id: 用户ID
        
    Returns:
        bool: 是否成功
    """
    redis_client = get_redis()
    if not redis_client:
        logger.warning(f"Redis not available, cannot clear cache for user {user_id}")
        return False
    
    try:
        # 1. 删除 token
        token_key = f"user_token:{user_id}"
        deleted_token = redis_client.delete(token_key)
        logger.debug(f"Deleted token key {token_key}: {deleted_token > 0}")
        
        # 2. 删除用户详情缓存
        detail_key = f"user_detail:{user_id}"
        deleted_detail = redis_client.delete(detail_key)
        logger.debug(f"Deleted user detail key {detail_key}: {deleted_detail > 0}")
        
        # 3. 删除在线状态
        online_key = f"online_users:{user_id}"
        deleted_online = redis_client.delete(online_key)
        logger.debug(f"Deleted online user key {online_key}: {deleted_online > 0}")
        
        # 4. 尝试删除可能的其他缓存 key（如果有的话）
        # 例如：用户会话、权限缓存等
        session_key = f"user_session:{user_id}"
        redis_client.delete(session_key)
        
        logger.info(f"User {user_id} logged out successfully. Cleared Redis keys: token={deleted_token > 0}, detail={deleted_detail > 0}, online={deleted_online > 0}")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to clear Redis cache for user {user_id}: {e}")
        return False


def invalidate_user_cache(user_id: int):
    """使用户缓存失效"""
    redis_client = get_redis()
    if redis_client:
        detail_key = f"user_detail:{user_id}"
        redis_client.delete(detail_key)
        logger.info(f"User cache invalidated: {user_id}")


def log_login_attempt(
    db: Session,
    user_id: Optional[int],
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    success: bool = True,
    failure_reason: Optional[str] = None,
    account: Optional[str] = None  # 用于失败时查找用户ID
):
    """
    记录登录日志
    
    Args:
        db: 数据库会话
        user_id: 用户ID（失败时可能为None）
        ip_address: IP地址
        user_agent: 用户代理字符串
        success: 是否成功
        failure_reason: 失败原因（失败时填写）
        account: 账号（手机号或邮箱，用于失败时查找用户ID）
    """
    try:
        # 如果失败且user_id为None，尝试通过账号查找用户ID
        final_user_id = user_id
        if not success and not user_id and account:
            try:
                if '@' in account:
                    user = db.query(User).filter(User.email == account).first()
                else:
                    user = db.query(User).filter(User.phone == account).first()
                if user:
                    final_user_id = user.id
            except Exception:
                pass
        
        # 如果仍然找不到，使用0作为占位符（表示未知用户）
        if not final_user_id:
            final_user_id = 0
        
        login_log = LoginLog(
            user_id=final_user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            failure_reason=failure_reason,
            created_at=datetime.now()
        )
        db.add(login_log)
        db.commit()
    except Exception as e:
        logger.error(f"Failed to log login attempt: {e}")
        db.rollback()


def submit_real_name_verification(db: Session, user_id: int, verify_data: RealNameVerificationSubmit):
    """
    提交实名认证申请
    
    1. 调用第三方接口核验姓名和身份证号
    2. 核验通过后，记录申请信息等待管理员人工审核照片
    """
    from app.services.id_verification import id_verification_service
    from app.models.user import RealNameVerification, UserProfile
    
    # 1. 调用第三方接口核验
    res = id_verification_service.verify_id_card(verify_data.real_name, verify_data.id_card_number)
    
    if not res["success"]:
        # 如果是核验结果不一致（res="2" or "3"），抛出具体异常
        if res["res"] in ["2", "3"]:
            raise ParameterException(f"实名认证失败：{res['description']}")
        # 其他接口请求错误
        raise ParameterException(f"{res['description']}")
    
    # 2. 如果核验一致 (res="1")，记录申请等待照片人工审核
    # 检查是否已有申请
    verification = db.query(RealNameVerification).filter(RealNameVerification.user_id == user_id).first()
    if verification:
        verification.id_card_front = verify_data.id_card_front
        verification.id_card_back = verify_data.id_card_back
        verification.face_photo = verify_data.face_photo
        verification.status = "pending"
        verification.reject_reason = None
        verification.created_at = datetime.now()
    else:
        verification = RealNameVerification(
            user_id=user_id,
            id_card_front=verify_data.id_card_front,
            id_card_back=verify_data.id_card_back,
            face_photo=verify_data.face_photo,
            status="pending"
        )
        db.add(verification)
    
    # 同时同步更新 UserProfile 中的姓名和身份证号
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        profile = UserProfile(user_id=user_id)
        db.add(profile)
    
    profile.real_name = verify_data.real_name
    profile.id_card_number = verify_data.id_card_number
    
    db.commit()
    
    # 清除用户信息缓存，确保下次获取详细信息时能看到最新状态
    redis_client = get_redis()
    if redis_client:
        redis_client.delete(f"user_detail:{user_id}")
    
    return True


def withdraw_real_name_verification(db: Session, user_id: int):
    """
    撤回实名认证申请
    
    只有在审核中（pending）状态下才能撤回
    撤回后直接删除申请记录
    """
    from app.models.user import RealNameVerification
    from app.core.exceptions import ParameterException
    
    verification = db.query(RealNameVerification).filter(
        RealNameVerification.user_id == user_id
    ).first()
    
    if not verification:
        raise ParameterException("未找到实名认证申请记录")
        
    if verification.status != "pending":
        raise ParameterException(f"当前状态为 {verification.status}，无法撤回申请")
    
    # 删除申请记录
    db.delete(verification)
    db.commit()
    
    # 清除用户信息缓存
    redis_client = get_redis()
    if redis_client:
        redis_client.delete(f"user_detail:{user_id}")
    
    return True
