from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.website import Carousel, Announcement, Document, Faq, FaqCategory
from app.schemas.admin import content as schemas

# --- Carousel Services ---
def list_carousels(db: Session, skip: int = 0, limit: int = 100) -> List[Carousel]:
    return db.query(Carousel).order_by(Carousel.sort_order).offset(skip).limit(limit).all()

def create_carousel(db: Session, item_in: schemas.CarouselCreate) -> Carousel:
    db_item = Carousel(**item_in.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_carousel(db: Session, id: int, item_in: schemas.CarouselUpdate) -> Optional[Carousel]:
    db_item = db.query(Carousel).filter(Carousel.id == id).first()
    if not db_item:
        return None
    
    update_data = item_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_carousel(db: Session, id: int) -> bool:
    db_item = db.query(Carousel).filter(Carousel.id == id).first()
    if not db_item:
        return False
    db.delete(db_item)
    db.commit()
    return True

# --- Announcement Services ---
def list_announcements(db: Session, skip: int = 0, limit: int = 100) -> List[Announcement]:
    return db.query(Announcement).order_by(Announcement.created_at.desc()).offset(skip).limit(limit).all()

def create_announcement(db: Session, item_in: schemas.AnnouncementCreate, user_id: int) -> Announcement:
    db_item = Announcement(**item_in.model_dump(), created_by=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_announcement(db: Session, id: int, item_in: schemas.AnnouncementUpdate) -> Optional[Announcement]:
    db_item = db.query(Announcement).filter(Announcement.id == id).first()
    if not db_item:
        return None
    
    update_data = item_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_announcement(db: Session, id: int) -> bool:
    db_item = db.query(Announcement).filter(Announcement.id == id).first()
    if not db_item:
        return False
    db.delete(db_item)
    db.commit()
    return True

# --- Document Services ---
def list_documents(db: Session, doc_type: str = None) -> List[Document]:
    query = db.query(Document)
    if doc_type:
        query = query.filter(Document.doc_type == doc_type)
    return query.order_by(Document.created_at.desc()).all()

def create_document(db: Session, item_in: schemas.DocumentCreate, user_id: int) -> Document:
    # Set others of same type to not current if this one is current
    if item_in.is_current:
        db.query(Document).filter(
            Document.doc_type == item_in.doc_type, 
            Document.is_current == True
        ).update({"is_current": False})
        
    db_item = Document(**item_in.model_dump(), created_by=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_document(db: Session, id: int, item_in: schemas.DocumentUpdate) -> Optional[Document]:
    db_item = db.query(Document).filter(Document.id == id).first()
    if not db_item:
        return None
    
    if item_in.is_current:
        db.query(Document).filter(
            Document.doc_type == db_item.doc_type if not item_in.doc_type else item_in.doc_type,
            Document.is_current == True
        ).update({"is_current": False})

    update_data = item_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
        
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_document(db: Session, id: int) -> bool:
    db_item = db.query(Document).filter(Document.id == id).first()
    if not db_item:
        return False
    db.delete(db_item)
    db.commit()
    return True

# --- FAQ Services ---
def list_faq_categories(db: Session) -> List[FaqCategory]:
    return db.query(FaqCategory).order_by(FaqCategory.sort_order).all()

def create_faq_category(db: Session, item_in: schemas.FaqCategoryCreate) -> FaqCategory:
    db_item = FaqCategory(**item_in.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_faq_category(db: Session, id: int, item_in: schemas.FaqCategoryUpdate) -> Optional[FaqCategory]:
    db_item = db.query(FaqCategory).filter(FaqCategory.id == id).first()
    if not db_item:
        return None
    update_data = item_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_faq_category(db: Session, id: int) -> bool:
    db_item = db.query(FaqCategory).filter(FaqCategory.id == id).first()
    if not db_item:
        return False
    # FAQs will have null category via FK Set Null if set up, or check manually
    db.delete(db_item)
    db.commit()
    return True

def list_faqs(db: Session, category_id: int = None) -> List[Faq]:
    query = db.query(Faq)
    if category_id:
        query = query.filter(Faq.category_id == category_id)
    return query.order_by(Faq.sort_order).all()

def create_faq(db: Session, item_in: schemas.FaqCreate) -> Faq:
    db_item = Faq(**item_in.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_faq(db: Session, id: int, item_in: schemas.FaqUpdate) -> Optional[Faq]:
    db_item = db.query(Faq).filter(Faq.id == id).first()
    if not db_item:
        return None
    update_data = item_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_faq(db: Session, id: int) -> bool:
    db_item = db.query(Faq).filter(Faq.id == id).first()
    if not db_item:
        return False
    db.delete(db_item)
    db.commit()
    return True
