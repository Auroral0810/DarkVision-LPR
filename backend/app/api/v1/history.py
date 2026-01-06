from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.history import RecognitionHistoryList
from app.services.recognition import recognition_service
from app.core.response import success_response, UnifiedResponse

router = APIRouter()

@router.get("", response_model=UnifiedResponse[RecognitionHistoryList], summary="查询识别历史记录")
async def get_recognition_history(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    start_date: Optional[datetime] = Query(None, description="开始时间"),
    end_date: Optional[datetime] = Query(None, description="结束时间"),
    license_plate: Optional[str] = Query(None, description="车牌号关键字"),
    plate_type: Optional[str] = Query(None, description="车牌类型"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    根据筛选条件获取用户的车牌识别历史记录
    """
    items, total = recognition_service.get_history(
        user_id=current_user.id,
        db=db,
        page=page,
        page_size=page_size,
        start_date=start_date,
        end_date=end_date,
        license_plate=license_plate,
        plate_type=plate_type
    )
    
    # 显式转换为 Pydantic 模型以支持序列化
    from app.schemas.history import RecognitionHistoryItem
    history_items = [RecognitionHistoryItem.model_validate(item) for item in items]
    
    total_pages = (total + page_size - 1) // page_size
    
    return success_response(data={
        "items": [item.model_dump(mode='json') for item in history_items],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    })
