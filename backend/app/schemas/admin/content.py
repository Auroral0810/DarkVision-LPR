from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- Carousel Schemas ---
class CarouselBase(BaseModel):
    title: str
    image_url: str
    link_url: Optional[str] = None
    sort_order: Optional[int] = 0
    is_enabled: Optional[bool] = True

class CarouselCreate(CarouselBase):
    pass

class CarouselUpdate(BaseModel):
    title: Optional[str] = None
    image_url: Optional[str] = None
    link_url: Optional[str] = None
    sort_order: Optional[int] = None
    is_enabled: Optional[bool] = None

class CarouselOut(CarouselBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# --- Announcement Schemas ---
class AnnouncementBase(BaseModel):
    title: str
    content: str
    display_position: str = "top"
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_enabled: Optional[bool] = True

class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    display_position: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_enabled: Optional[bool] = None

class AnnouncementOut(AnnouncementBase):
    id: int
    created_by: int
    created_at: datetime
    class Config:
        from_attributes = True

# --- Document Schemas ---
class DocumentBase(BaseModel):
    title: str
    doc_type: str # tech, service_agreement, privacy_policy
    content: str
    version: str
    is_current: Optional[bool] = False

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    doc_type: Optional[str] = None
    content: Optional[str] = None
    version: Optional[str] = None
    is_current: Optional[bool] = None

class DocumentOut(DocumentBase):
    id: int
    created_by: int
    created_at: datetime
    class Config:
        from_attributes = True

# --- FAQ Schemas ---
class FaqCategoryBase(BaseModel):
    name: str
    sort_order: Optional[int] = 0

class FaqCategoryCreate(FaqCategoryBase):
    pass

class FaqCategoryUpdate(BaseModel):
    name: Optional[str] = None
    sort_order: Optional[int] = None

class FaqCategoryOut(FaqCategoryBase):
    id: int
    class Config:
        from_attributes = True

class FaqBase(BaseModel):
    question: str
    answer: str
    category_id: Optional[int] = None
    sort_order: Optional[int] = 0
    is_hot: Optional[bool] = False

class FaqCreate(FaqBase):
    pass

class FaqUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    category_id: Optional[int] = None
    sort_order: Optional[int] = None
    is_hot: Optional[bool] = None

class FaqOut(FaqBase):
    id: int
    view_count: int
    created_at: datetime
    category: Optional[FaqCategoryOut] = None
    class Config:
        from_attributes = True
