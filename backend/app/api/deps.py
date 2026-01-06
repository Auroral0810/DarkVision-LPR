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
        
    return user

