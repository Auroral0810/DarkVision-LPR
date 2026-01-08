from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.response import UnifiedResponse, success_response, error_response
from app.api.deps import get_current_active_admin
from app.models.user import User

from app.schemas.admin.content import (
    CarouselCreate, CarouselUpdate, CarouselOut,
    AnnouncementCreate, AnnouncementUpdate, AnnouncementOut,
    DocumentCreate, DocumentUpdate, DocumentOut,
    FaqCreate, FaqUpdate, FaqOut,
    FaqCategoryCreate, FaqCategoryUpdate, FaqCategoryOut
)
from app.services.admin.content_service import content_service

router = APIRouter()

# --- Carousels ---
@router.get("/carousels", response_model=UnifiedResponse[List[CarouselOut]])
def get_carousels(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    items = content_service.get_carousels(db)
    return success_response(data=items)

@router.post("/carousels", response_model=UnifiedResponse[CarouselOut])
def create_carousel(
    data: CarouselCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    item = content_service.create_carousel(db, data)
    return success_response(data=item, message="创建成功")

@router.put("/carousels/{id}", response_model=UnifiedResponse[CarouselOut])
def update_carousel(
    id: int,
    data: CarouselUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    item = content_service.update_carousel(db, id, data)
    if not item:
        return error_response(message="未找到该轮播图")
    return success_response(data=item, message="更新成功")

@router.delete("/carousels/{id}", response_model=UnifiedResponse)
def delete_carousel(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    success = content_service.delete_carousel(db, id)
    if not success:
        return error_response(message="未找到该轮播图")
    return success_response(message="删除成功")

# --- Announcements ---
@router.get("/announcements", response_model=UnifiedResponse[List[AnnouncementOut]])
def get_announcements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    items = content_service.get_announcements(db)
    return success_response(data=items)

@router.post("/announcements", response_model=UnifiedResponse[AnnouncementOut])
def create_announcement(
    data: AnnouncementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    item = content_service.create_announcement(db, data, current_user.id)
    return success_response(data=item, message="创建成功")

@router.put("/announcements/{id}", response_model=UnifiedResponse[AnnouncementOut])
def update_announcement(
    id: int,
    data: AnnouncementUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    item = content_service.update_announcement(db, id, data)
    if not item:
        return error_response(message="未找到该公告")
    return success_response(data=item, message="更新成功")

@router.delete("/announcements/{id}", response_model=UnifiedResponse)
def delete_announcement(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    success = content_service.delete_announcement(db, id)
    if not success:
        return error_response(message="未找到该公告")
    return success_response(message="删除成功")

# --- Documents ---
@router.get("/documents", response_model=UnifiedResponse[List[DocumentOut]])
def get_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    items = content_service.get_documents(db)
    return success_response(data=items)

@router.post("/documents", response_model=UnifiedResponse[DocumentOut])
def create_document(
    data: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    item = content_service.create_document(db, data, current_user.id)
    return success_response(data=item, message="创建成功")

@router.put("/documents/{id}", response_model=UnifiedResponse[DocumentOut])
def update_document(
    id: int,
    data: DocumentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    item = content_service.update_document(db, id, data)
    if not item:
        return error_response(message="未找到该文档")
    return success_response(data=item, message="更新成功")

@router.delete("/documents/{id}", response_model=UnifiedResponse)
def delete_document(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    success = content_service.delete_document(db, id)
    if not success:
        return error_response(message="未找到该文档")
    return success_response(message="删除成功")

# --- FAQ Categories ---
@router.get("/faq-categories", response_model=UnifiedResponse[List[FaqCategoryOut]])
def get_faq_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    items = content_service.get_faq_categories(db)
    return success_response(data=items)

@router.post("/faq-categories", response_model=UnifiedResponse[FaqCategoryOut])
def create_faq_category(
    data: FaqCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    item = content_service.create_faq_category(db, data)
    return success_response(data=item, message="创建成功")

@router.put("/faq-categories/{id}", response_model=UnifiedResponse[FaqCategoryOut])
def update_faq_category(
    id: int,
    data: FaqCategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    item = content_service.update_faq_category(db, id, data)
    if not item:
        return error_response(message="未找到该分类")
    return success_response(data=item, message="更新成功")

@router.delete("/faq-categories/{id}", response_model=UnifiedResponse)
def delete_faq_category(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    success = content_service.delete_faq_category(db, id)
    if not success:
        return error_response(message="未找到该分类")
    return success_response(message="删除成功")

# --- FAQs ---
@router.get("/faqs", response_model=UnifiedResponse[List[FaqOut]])
def get_faqs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    items = content_service.get_faqs(db)
    return success_response(data=items)

@router.post("/faqs", response_model=UnifiedResponse[FaqOut])
def create_faq(
    data: FaqCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    item = content_service.create_faq(db, data)
    return success_response(data=item, message="创建成功")

@router.put("/faqs/{id}", response_model=UnifiedResponse[FaqOut])
def update_faq(
    id: int,
    data: FaqUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    item = content_service.update_faq(db, id, data)
    if not item:
        return error_response(message="未找到该FAQ")
    return success_response(data=item, message="更新成功")

@router.delete("/faqs/{id}", response_model=UnifiedResponse)
def delete_faq(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    success = content_service.delete_faq(db, id)
    if not success:
        return error_response(message="未找到该FAQ")
    return success_response(message="删除成功")
