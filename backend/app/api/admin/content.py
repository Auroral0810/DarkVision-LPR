from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.api.deps import get_current_active_admin
from app.services import content as content_service
from app.schemas.admin import content as schemas
from app.core.response import UnifiedResponse, success_response

router = APIRouter()

# --- Carousels ---
@router.get("/carousels", response_model=UnifiedResponse, summary="轮播图列表")
def list_carousels(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    items = content_service.list_carousels(db, skip, limit)
    return success_response(data=[schemas.CarouselOut.model_validate(item) for item in items])

@router.post("/carousels", response_model=UnifiedResponse, summary="创建轮播图")
def create_carousel(
    item_in: schemas.CarouselCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    item = content_service.create_carousel(db, item_in)
    return success_response(data=schemas.CarouselOut.model_validate(item))

@router.put("/carousels/{id}", response_model=UnifiedResponse, summary="更新轮播图")
def update_carousel(
    id: int,
    item_in: schemas.CarouselUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    item = content_service.update_carousel(db, id, item_in)
    if not item:
        raise HTTPException(status_code=404, detail="Carousel not found")
    return success_response(data=schemas.CarouselOut.model_validate(item))

@router.delete("/carousels/{id}", response_model=UnifiedResponse, summary="删除轮播图")
def delete_carousel(
    id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    if not content_service.delete_carousel(db, id):
        raise HTTPException(status_code=404, detail="Carousel not found")
    return success_response(msg="删除成功")

# --- Announcements ---
@router.get("/announcements", response_model=UnifiedResponse, summary="公告列表")
def list_announcements(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    items = content_service.list_announcements(db, skip, limit)
    return success_response(data=[schemas.AnnouncementOut.model_validate(item) for item in items])

@router.post("/announcements", response_model=UnifiedResponse, summary="发布公告")
def create_announcement(
    item_in: schemas.AnnouncementCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    item = content_service.create_announcement(db, item_in, user_id=admin.id)
    return success_response(data=schemas.AnnouncementOut.model_validate(item))

@router.put("/announcements/{id}", response_model=UnifiedResponse, summary="更新公告")
def update_announcement(
    id: int,
    item_in: schemas.AnnouncementUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    item = content_service.update_announcement(db, id, item_in)
    if not item:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return success_response(data=schemas.AnnouncementOut.model_validate(item))

@router.delete("/announcements/{id}", response_model=UnifiedResponse, summary="删除公告")
def delete_announcement(
    id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    if not content_service.delete_announcement(db, id):
        raise HTTPException(status_code=404, detail="Announcement not found")
    return success_response(msg="删除成功")

# --- Documents ---
@router.get("/documents", response_model=UnifiedResponse, summary="文档列表")
def list_documents(
    doc_type: Optional[str] = None,
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    items = content_service.list_documents(db, doc_type)
    return success_response(data=[schemas.DocumentOut.model_validate(item) for item in items])

@router.post("/documents", response_model=UnifiedResponse, summary="创建文档")
def create_document(
    item_in: schemas.DocumentCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    item = content_service.create_document(db, item_in, user_id=admin.id)
    return success_response(data=schemas.DocumentOut.model_validate(item))

@router.put("/documents/{id}", response_model=UnifiedResponse, summary="更新文档")
def update_document(
    id: int,
    item_in: schemas.DocumentUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    item = content_service.update_document(db, id, item_in)
    if not item:
        raise HTTPException(status_code=404, detail="Document not found")
    return success_response(data=schemas.DocumentOut.model_validate(item))

@router.delete("/documents/{id}", response_model=UnifiedResponse, summary="删除文档")
def delete_document(
    id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    if not content_service.delete_document(db, id):
        raise HTTPException(status_code=404, detail="Document not found")
    return success_response(msg="删除成功")

# --- FAQs ---
@router.get("/faqs/categories", response_model=UnifiedResponse, summary="FAQ分类列表")
def list_faq_categories(
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    items = content_service.list_faq_categories(db)
    return success_response(data=[schemas.FaqCategoryOut.model_validate(item) for item in items])

@router.post("/faqs/categories", response_model=UnifiedResponse, summary="创建FAQ分类")
def create_faq_category(
    item_in: schemas.FaqCategoryCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    item = content_service.create_faq_category(db, item_in)
    return success_response(data=schemas.FaqCategoryOut.model_validate(item))

@router.put("/faqs/categories/{id}", response_model=UnifiedResponse, summary="更新FAQ分类")
def update_faq_category(
    id: int,
    item_in: schemas.FaqCategoryUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    item = content_service.update_faq_category(db, id, item_in)
    if not item:
        raise HTTPException(status_code=404, detail="Category not found")
    return success_response(data=schemas.FaqCategoryOut.model_validate(item))

@router.delete("/faqs/categories/{id}", response_model=UnifiedResponse, summary="删除FAQ分类")
def delete_faq_category(
    id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    if not content_service.delete_faq_category(db, id):
        raise HTTPException(status_code=404, detail="Category not found")
    return success_response(msg="删除成功")

@router.get("/faqs", response_model=UnifiedResponse, summary="FAQ列表")
def list_faqs(
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    items = content_service.list_faqs(db, category_id)
    return success_response(data=[schemas.FaqOut.model_validate(item) for item in items])

@router.post("/faqs", response_model=UnifiedResponse, summary="创建FAQ")
def create_faq(
    item_in: schemas.FaqCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    item = content_service.create_faq(db, item_in)
    return success_response(data=schemas.FaqOut.model_validate(item))

@router.put("/faqs/{id}", response_model=UnifiedResponse, summary="更新FAQ")
def update_faq(
    id: int,
    item_in: schemas.FaqUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    item = content_service.update_faq(db, id, item_in)
    if not item:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return success_response(data=schemas.FaqOut.model_validate(item))

@router.delete("/faqs/{id}", response_model=UnifiedResponse, summary="删除FAQ")
def delete_faq(
    id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_active_admin)
):
    if not content_service.delete_faq(db, id):
        raise HTTPException(status_code=404, detail="FAQ not found")
    return success_response(msg="删除成功")
