from fastapi import APIRouter, Request, Depends, Header
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.response import success, UnifiedResponse
from app.models.user import User
from app.models.statistics import PageViewLog, PageType
from app.core.logger import logger
from app.core.security import decode_access_token
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

router = APIRouter()


class PageViewRequest(BaseModel):
    """页面访问埋点请求"""
    page_path: str = Field(..., description="页面路径")
    page_type: PageType = Field(default=PageType.USER, description="页面类型")


def get_optional_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """可选获取当前用户（用于未登录用户的埋点）"""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    try:
        token = authorization.replace("Bearer ", "")
        payload = decode_access_token(token)
        if payload and payload.get("user_id"):
            user_id = payload.get("user_id")
            return db.query(User).filter(User.id == user_id).first()
    except Exception:
        pass
    return None


@router.post("/page-view", response_model=UnifiedResponse, summary="页面访问埋点", tags=["数据统计"])
def track_page_view(
    request_data: PageViewRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
):
    """
    记录页面访问日志
    
    用于统计 PV/UV 数据
    - 如果用户已登录，记录 user_id
    - 记录 IP、User-Agent、Referer 等信息
    """
    try:
        # 获取客户端信息
        client_ip = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent", "")
        referer = request.headers.get("referer", "")
        
        # 创建访问日志
        page_view = PageViewLog(
            user_id=current_user.id if current_user else None,
            page_path=request_data.page_path,
            page_type=request_data.page_type,
            ip_address=client_ip,
            user_agent=user_agent,
            referer=referer if referer else None,
            created_at=datetime.now()
        )
        
        db.add(page_view)
        db.commit()
        
        logger.debug(f"Page view tracked: {request_data.page_path} by user {current_user.id if current_user else 'anonymous'}")
        
        return success(message="记录成功")
    except Exception as e:
        logger.error(f"Failed to track page view: {e}")
        db.rollback()
        # 静默失败，不影响用户体验
        return success(message="记录成功")  # 即使失败也返回成功，避免影响前端

