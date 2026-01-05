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
    # success_response wrapper might need adjustment if it wraps in "data" field
    # But for now let's return the content directly which matches response_model
    # or wrap it if your frontend expects { code: 200, data: {...} }
    # Using success_response standardizes it.
    return success_response(data=content)

