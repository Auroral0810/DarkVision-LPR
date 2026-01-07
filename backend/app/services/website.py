import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.cache import get_redis
from app.models.website import Carousel, Announcement, ClientDownload, Faq, Document, SystemConfig
from app.schemas.website import (
    CarouselResponse, AnnouncementResponse, ClientDownloadResponse, 
    FaqResponse, DocumentResponse, SystemConfigResponse
)
from typing import List, Dict, Any

CACHE_KEY_WEBSITE_CONTENT = "website:content:public"
CACHE_EXPIRE_SECONDS = 3600  # 1 hour

class WebsiteService:
    @staticmethod
    async def get_public_content(db: Session) -> Dict[str, Any]:
        # Try to get from Redis first
        redis_client = get_redis()
        cached_content = None
        if redis_client:
            try:
                cached_content = redis_client.get(CACHE_KEY_WEBSITE_CONTENT)
            except Exception as e:
                print(f"Redis get failed: {e}")

        if cached_content:
            # Redis stores strings, so we load it back to dict
            return json.loads(cached_content)

        # Fetch from DB if not in cache
        content = {
            "carousels": WebsiteService._get_carousels(db),
            "announcements": WebsiteService._get_announcements(db),
            "downloads": WebsiteService._get_downloads(db),
            "faqs": WebsiteService._get_faqs(db),
            "documents": WebsiteService._get_documents(db),
            "configs": WebsiteService._get_configs(db)
        }

        # Cache the result (serialize to JSON)
        # Note: Pydantic models need to be dumped to json-serializable dicts
        # But here we are returning dicts from the helper methods mostly, 
        # actually helper methods return ORM objects usually. 
        # Let's verify helpers return Pydantic-ready dicts or lists.
        
        # To simplify, we will let FastAPI response_model handle serialization for the API response,
        # but for Redis we need to serialize manually.
        # A better approach for Redis caching complex structures is caching per section or using FastAPICache.
        # Here we will do manual serialization for demonstration.
        
        serialized_content = {
            "carousels": [CarouselResponse.model_validate(c).model_dump(mode='json') for c in content["carousels"]],
            "announcements": [AnnouncementResponse.model_validate(a).model_dump(mode='json') for a in content["announcements"]],
            "downloads": [ClientDownloadResponse.model_validate(d).model_dump(mode='json') for d in content["downloads"]],
            "faqs": [FaqResponse.model_validate(f).model_dump(mode='json') for f in content["faqs"]],
            "documents": [DocumentResponse.model_validate(d).model_dump(mode='json') for d in content["documents"]],
            "configs": [SystemConfigResponse.model_validate(c).model_dump(mode='json') for c in content["configs"]]
        }
        
        if redis_client:
            try:
                redis_client.setex(CACHE_KEY_WEBSITE_CONTENT, CACHE_EXPIRE_SECONDS, json.dumps(serialized_content))
            except Exception as e:
                print(f"Redis set failed: {e}")
        
        return serialized_content

    @staticmethod
    def _get_carousels(db: Session) -> List[Carousel]:
        return db.query(Carousel).filter(Carousel.is_enabled == True).order_by(Carousel.sort_order).all()

    @staticmethod
    def _get_announcements(db: Session) -> List[Announcement]:
        now = datetime.now()
        return db.query(Announcement).filter(
            Announcement.is_enabled == True,
            (Announcement.start_time <= now) | (Announcement.start_time == None),
            (Announcement.end_time >= now) | (Announcement.end_time == None)
        ).all()

    @staticmethod
    def _get_downloads(db: Session) -> List[ClientDownload]:
        # Get latest per OS
        # Simple approach: filter is_latest=True
        return db.query(ClientDownload).filter(ClientDownload.is_latest == True).all()

    @staticmethod
    def _get_faqs(db: Session) -> List[Faq]:
        return db.query(Faq).order_by(Faq.sort_order).all()

    @staticmethod
    def _get_documents(db: Session) -> List[Document]:
        return db.query(Document).filter(Document.is_current == True).all()

    @staticmethod
    def _get_configs(db: Session) -> List[SystemConfig]:
        return db.query(SystemConfig).filter(SystemConfig.is_public == True).all()

    @staticmethod
    def get_latest_news(db: Session, limit: int = 5) -> List[Announcement]:
        """
        获取最新的公告/动态
        """
        now = datetime.now()
        return db.query(Announcement).filter(
            Announcement.is_enabled == True,
            (Announcement.start_time <= now) | (Announcement.start_time == None),
            (Announcement.end_time >= now) | (Announcement.end_time == None)
        ).order_by(Announcement.created_at.desc()).limit(limit).all()

    @staticmethod
    def clear_cache():
        redis_client = get_redis()
        if redis_client:
            try:
                redis_client.delete(CACHE_KEY_WEBSITE_CONTENT)
            except Exception as e:
                print(f"Redis delete failed: {e}")

website_service = WebsiteService()

