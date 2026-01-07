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

