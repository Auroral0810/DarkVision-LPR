from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _truncate_password(password: str, max_bytes: int = 72) -> str:
    """
    安全地截断密码到指定字节数
    
    Args:
        password: 原始密码
        max_bytes: 最大字节数（bcrypt限制为72）
        
    Returns:
        str: 截断后的密码
    """
    password_bytes = password.encode('utf-8')
    if len(password_bytes) <= max_bytes:
        return password
    
    # 截断到最大字节数，但要确保不会在UTF-8字符中间截断
    truncated = password_bytes[:max_bytes]
    
    # 尝试解码，如果失败则继续向前减少直到成功
    for i in range(len(truncated), max(0, len(truncated) - 4), -1):
        try:
            return truncated[:i].decode('utf-8')
        except UnicodeDecodeError:
            continue
    
    # 如果还是失败，返回空字符串（理论上不会到这里）
    return ""


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    
    Args:
        plain_password: 明文密码
        hashed_password: 哈希密码
        
    Returns:
        bool: 密码是否匹配
    """
    try:
        # 截断密码到72字节
        truncated_password = _truncate_password(plain_password, 72)
        return pwd_context.verify(truncated_password, hashed_password)
    except Exception as e:
        from app.core.logger import logger
        logger.error(f"Password verification error: {e}")
        return False


def get_password_hash(password: str) -> str:
    """
    生成密码哈希
    
    Args:
        password: 明文密码
        
    Returns:
        str: 密码哈希
    """
    try:
        # 截断密码到72字节
        truncated_password = _truncate_password(password, 72)
        return pwd_context.hash(truncated_password)
    except Exception as e:
        from app.core.logger import logger
        logger.error(f"Password hashing error: {e}")
        raise


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建JWT访问令牌
    
    Args:
        data: JWT payload数据
        expires_delta: 过期时间增量
        
    Returns:
        str: JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    解码JWT令牌
    
    Args:
        token: JWT token
        
    Returns:
        Optional[dict]: 解码后的payload，失败返回None
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
