from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.website import website_service
from app.core.response import success_response, UnifiedResponse

router = APIRouter()

@router.get("/website/content", summary="获取官网公开内容", response_model=UnifiedResponse)
async def get_website_content(db: Session = Depends(get_db)):
    """
    获取官网首页、下载、文档等页面的动态内容。
    数据优先从 Redis 缓存读取。
    """
    content = await website_service.get_public_content(db)
    return success_response(data=content)

@router.get("/website/latest-news", summary="获取最新动态", response_model=UnifiedResponse)
async def get_latest_news(db: Session = Depends(get_db)):
    """
    获取最近的5条动态公告，用于仪表盘展示。
    """
    news = website_service.get_latest_news(db, limit=5)
    from app.schemas.website import AnnouncementResponse
    data = [AnnouncementResponse.model_validate(n).model_dump(mode='json') for n in news]
    return success_response(data=data)

