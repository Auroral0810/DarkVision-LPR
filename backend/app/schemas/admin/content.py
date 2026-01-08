from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# --- Enums ---
class DisplayPosition(str, Enum):
    popup = 'popup'
    banner = 'banner'
    message_center = 'message_center'

class DocType(str, Enum):
    tech = 'tech'
    service_agreement = 'service_agreement'
    privacy_policy = 'privacy_policy'

# --- Carousel ---
class CarouselBase(BaseModel):
    title: str = Field(..., max_length=100)
    image_url: str = Field(..., max_length=255)
    link_url: Optional[str] = Field(None, max_length=255)
    sort_order: int = 0
    is_enabled: bool = True

class CarouselCreate(CarouselBase):
    pass

class CarouselUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    image_url: Optional[str] = Field(None, max_length=255)
    link_url: Optional[str] = Field(None, max_length=255)
    sort_order: Optional[int] = None
    is_enabled: Optional[bool] = None

class CarouselOut(CarouselBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Announcement ---
class AnnouncementBase(BaseModel):
    title: str
    content: str
    display_position: DisplayPosition
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_enabled: bool = True

class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    display_position: Optional[DisplayPosition] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_enabled: Optional[bool] = None

class AnnouncementOut(AnnouncementBase):
    id: int
    created_by: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Document ---
class DocumentBase(BaseModel):
    title: str
    doc_type: DocType
    content: str
    version: str
    is_current: bool = False

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    doc_type: Optional[DocType] = None
    content: Optional[str] = None
    version: Optional[str] = None
    is_current: Optional[bool] = None

class DocumentOut(DocumentBase):
    id: int
    created_by: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- FAQ Category ---
class FaqCategoryBase(BaseModel):
    name: str
    sort_order: int = 0

class FaqCategoryCreate(FaqCategoryBase):
    pass

class FaqCategoryUpdate(BaseModel):
    name: Optional[str] = None
    sort_order: Optional[int] = None

class FaqCategoryOut(FaqCategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- FAQ ---
class FaqBase(BaseModel):
    question: str
    answer: str
    category_id: Optional[int] = None
    sort_order: int = 0
    is_hot: bool = False

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
    model_config = ConfigDict(from_attributes=True)
