from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.core.exceptions import UnauthorizedException, TokenInvalidException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user.
    Returns the SQLAlchemy User model instance.
    """
    payload = decode_access_token(token)
    if not payload:
        raise TokenInvalidException()
    
    user_id = payload.get("user_id")
    if not user_id:
        raise UnauthorizedException()
        
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UnauthorizedException()
        
    # 状态校验：检查用户是否被封禁
    from app.models.user import UserStatus
    if user.status == UserStatus.BANNED:
        from app.core.exceptions import UserBannedException
        reason = f"您的账号已被封禁：{user.banned_reason}" if user.banned_reason else "您的账号已被封禁，请联系管理员"
        raise UserBannedException(message=reason)
    
    # 强制下线校验：检查 Redis 中的 token 是否与当前一致
    from app.core.cache import get_redis
    redis_client = get_redis()
    if redis_client:
        token_key = f"user_token:{user_id}"
        stored_token = redis_client.get(token_key)
        # 如果 Redis 中没有 token（说明被强制下线或过期），或者 token 对不上
        if not stored_token or stored_token != token:
            from app.core.exceptions import TokenInvalidException
            raise TokenInvalidException(message="登录已失效或在其他地方登录，请重新登录")
    
    # 刷新用户在线状态（心跳机制）
    try:
        from app.services.online_user_service import refresh_user_online
        refresh_user_online(user_id)
    except Exception as e:
        # 静默失败，不影响主流程
        from app.core.logger import logger
        logger.warning(f"Failed to refresh user online status: {e}")
        
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """确认用户状态活跃"""
    if current_user.status == "inactive":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用"
        )
    return current_user


def get_current_active_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """确认用户是管理员且状态活跃"""
    if current_user.user_type != "admin":
        from app.core.exceptions import ForbiddenException
        raise ForbiddenException()
    if current_user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="管理员账号已被禁用"
        )
    return current_user

