from sqlalchemy.orm import Session
from typing import List, Optional
import json
from datetime import datetime

from app.models.content import Carousel, Announcement, Document, Faq, FaqCategory
from app.schemas.admin.content import (
    CarouselCreate, CarouselUpdate, CarouselOut,
    AnnouncementCreate, AnnouncementUpdate, AnnouncementOut,
    DocumentCreate, DocumentUpdate, DocumentOut,
    FaqCreate, FaqUpdate, FaqOut,
    FaqCategoryCreate, FaqCategoryUpdate, FaqCategoryOut
)
from app.core.redis import redis_client

CACHE_KEY_CAROUSELS = "admin:content:carousels"
CACHE_KEY_ANNOUNCEMENTS = "admin:content:announcements"
CACHE_KEY_DOCUMENTS = "admin:content:documents"
CACHE_KEY_FAQS = "admin:content:faqs"
CACHE_KEY_FAQ_CATEGORIES = "admin:content:faq_categories"

class ContentService:
    # --- Carousels ---
    def get_carousels(self, db: Session) -> List[Carousel]:
        cache_key = CACHE_KEY_CAROUSELS
        if redis_client:
            try:
                cached = redis_client.get(cache_key)
                if cached: return json.loads(cached)
            except Exception: pass
        
        items = db.query(Carousel).order_by(Carousel.sort_order.asc(), Carousel.id.desc()).all()
        
        if redis_client and items:
            try:
                serialized = [CarouselOut.model_validate(i).model_dump(mode='json') for i in items]
                redis_client.setex(cache_key, 3600, json.dumps(serialized))
            except Exception: pass
        return items

    def create_carousel(self, db: Session, data: CarouselCreate) -> Carousel:
        item = Carousel(**data.model_dump())
        db.add(item)
        db.commit()
        db.refresh(item)
        if redis_client: redis_client.delete(CACHE_KEY_CAROUSELS)
        return item

    def update_carousel(self, db: Session, id: int, data: CarouselUpdate) -> Optional[Carousel]:
        item = db.query(Carousel).filter(Carousel.id == id).first()
        if not item: return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
        if redis_client: redis_client.delete(CACHE_KEY_CAROUSELS)
        return item

    def delete_carousel(self, db: Session, id: int) -> bool:
        item = db.query(Carousel).filter(Carousel.id == id).first()
        if not item: return False
        db.delete(item)
        db.commit()
        if redis_client: redis_client.delete(CACHE_KEY_CAROUSELS)
        return True

    # --- Announcements ---
    def get_announcements(self, db: Session) -> List[Announcement]:
        cache_key = CACHE_KEY_ANNOUNCEMENTS
        if redis_client:
            try:
                cached = redis_client.get(cache_key)
                if cached:
                    return json.loads(cached)
            except Exception:
                pass
        
        items = db.query(Announcement).order_by(Announcement.created_at.desc()).all()
        
        if redis_client and items:
            try:
                serialized = [AnnouncementOut.model_validate(i).model_dump(mode='json') for i in items]
                redis_client.setex(cache_key, 3600, json.dumps(serialized))
            except Exception:
                pass
        return items

    def create_announcement(self, db: Session, data: AnnouncementCreate, user_id: int) -> Announcement:
        item = Announcement(**data.model_dump(), created_by=user_id)
        db.add(item)
        db.commit()
        db.refresh(item)
        if redis_client: redis_client.delete(CACHE_KEY_ANNOUNCEMENTS)
        return item

    def update_announcement(self, db: Session, id: int, data: AnnouncementUpdate) -> Optional[Announcement]:
        item = db.query(Announcement).filter(Announcement.id == id).first()
        if not item: return None
        
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(item, key, value)
        
        db.commit()
        db.refresh(item)
        if redis_client: redis_client.delete(CACHE_KEY_ANNOUNCEMENTS)
        return item

    def delete_announcement(self, db: Session, id: int) -> bool:
        item = db.query(Announcement).filter(Announcement.id == id).first()
        if not item: return False
        db.delete(item)
        db.commit()
        if redis_client: redis_client.delete(CACHE_KEY_ANNOUNCEMENTS)
        return True

    # --- Documents ---
    def get_documents(self, db: Session) -> List[Document]:
        cache_key = CACHE_KEY_DOCUMENTS
        if redis_client:
            try:
                cached = redis_client.get(cache_key)
                if cached:
                    return json.loads(cached)
            except Exception:
                pass
        
        items = db.query(Document).order_by(Document.created_at.desc()).all()
        
        if redis_client and items:
            try:
                serialized = [DocumentOut.model_validate(i).model_dump(mode='json') for i in items]
                redis_client.setex(cache_key, 3600, json.dumps(serialized))
            except Exception:
                pass
        return items

    def create_document(self, db: Session, data: DocumentCreate, user_id: int) -> Document:
        if data.is_current:
            # Set defined type's other docs to not current
            db.query(Document).filter(Document.doc_type == data.doc_type).update({"is_current": False})
            
        item = Document(**data.model_dump(), created_by=user_id)
        db.add(item)
        db.commit()
        db.refresh(item)
        if redis_client: redis_client.delete(CACHE_KEY_DOCUMENTS)
        return item

    def update_document(self, db: Session, id: int, data: DocumentUpdate) -> Optional[Document]:
        item = db.query(Document).filter(Document.id == id).first()
        if not item: return None
        
        if data.is_current:
             db.query(Document).filter(Document.doc_type == (data.doc_type or item.doc_type)).update({"is_current": False})

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(item, key, value)
        
        db.commit()
        db.refresh(item)
        if redis_client: redis_client.delete(CACHE_KEY_DOCUMENTS)
        return item

    def delete_document(self, db: Session, id: int) -> bool:
        item = db.query(Document).filter(Document.id == id).first()
        if not item: return False
        db.delete(item)
        db.commit()
        if redis_client: redis_client.delete(CACHE_KEY_DOCUMENTS)
        return True

    # --- FAQs ---
    def get_faqs(self, db: Session) -> List[Faq]:
        cache_key = CACHE_KEY_FAQS
        if redis_client:
            try:
                cached = redis_client.get(cache_key)
                if cached:
                    return json.loads(cached)
            except Exception:
                pass
        
        items = db.query(Faq).order_by(Faq.sort_order.asc(), Faq.id.desc()).all()
        
        if redis_client and items:
            try:
                serialized = [FaqOut.model_validate(i).model_dump(mode='json') for i in items]
                redis_client.setex(cache_key, 3600, json.dumps(serialized))
            except Exception:
                pass
        return items

    def create_faq(self, db: Session, data: FaqCreate) -> Faq:
        item = Faq(**data.model_dump())
        db.add(item)
        db.commit()
        db.refresh(item)
        if redis_client: redis_client.delete(CACHE_KEY_FAQS)
        return item

    def update_faq(self, db: Session, id: int, data: FaqUpdate) -> Optional[Faq]:
        item = db.query(Faq).filter(Faq.id == id).first()
        if not item: return None
        
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(item, key, value)
        
        db.commit()
        db.refresh(item)
        if redis_client: redis_client.delete(CACHE_KEY_FAQS)
        return item

    def delete_faq(self, db: Session, id: int) -> bool:
        item = db.query(Faq).filter(Faq.id == id).first()
        if not item: return False
        db.delete(item)
        db.commit()
        if redis_client: redis_client.delete(CACHE_KEY_FAQS)
        return True

    # --- FAQ Categories ---
    def get_faq_categories(self, db: Session) -> List[FaqCategory]:
        cache_key = CACHE_KEY_FAQ_CATEGORIES
        if redis_client:
             try:
                cached = redis_client.get(cache_key)
                if cached: return json.loads(cached)
             except Exception: pass
        
        items = db.query(FaqCategory).order_by(FaqCategory.sort_order.asc()).all()
        
        if redis_client and items:
            try:
                serialized = [FaqCategoryOut.model_validate(i).model_dump(mode='json') for i in items]
                redis_client.setex(cache_key, 3600, json.dumps(serialized))
            except Exception: pass
        return items

    def create_faq_category(self, db: Session, data: FaqCategoryCreate) -> FaqCategory:
        item = FaqCategory(**data.model_dump())
        db.add(item)
        db.commit()
        db.refresh(item)
        if redis_client: redis_client.delete(CACHE_KEY_FAQ_CATEGORIES)
        return item

    def update_faq_category(self, db: Session, id: int, data: FaqCategoryUpdate) -> Optional[FaqCategory]:
        item = db.query(FaqCategory).filter(FaqCategory.id == id).first()
        if not item: return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
        if redis_client: redis_client.delete(CACHE_KEY_FAQ_CATEGORIES)
        return item
    
    def delete_faq_category(self, db: Session, id: int) -> bool:
        item = db.query(FaqCategory).filter(FaqCategory.id == id).first()
        if not item: return False
        db.delete(item)
        db.commit()
        if redis_client: redis_client.delete(CACHE_KEY_FAQ_CATEGORIES)
        return True

content_service = ContentService()
