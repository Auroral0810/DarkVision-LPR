from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.response import success, UnifiedResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.online_user_service import get_online_user_count
from datetime import datetime

router = APIRouter()


@router.get("/online-users", response_model=UnifiedResponse, summary="获取在线用户数", tags=["管理员-数据统计"])
def get_online_users(
    current_user: User = Depends(get_current_user),
):
    """
    获取当前在线用户数（实时）
    
    返回当前登录了用户系统（user-portal）的在线用户数量
    """
    count = get_online_user_count()
    
    return success(
        data={
            "count": count,
            "timestamp": int(datetime.now().timestamp())
        },
        message="获取成功"
    )

