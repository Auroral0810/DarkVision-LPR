from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

# --- Shared Base Models ---

class CarouselBase(BaseModel):
    title: str
    image_url: str
    link_url: Optional[str] = None
    sort_order: int = 0
    is_enabled: bool = True

class AnnouncementBase(BaseModel):
    title: str
    content: str
    display_position: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_enabled: bool = True

class ClientDownloadBase(BaseModel):
    os: str
    version: str
    download_url: str
    changelog: Optional[str] = None
    release_date: datetime
    is_latest: bool = True

class FaqBase(BaseModel):
    question: str
    answer: str
    sort_order: int = 0
    view_count: int = 0
    is_hot: bool = False
    category_id: Optional[int] = None

class DocumentBase(BaseModel):
    title: str
    doc_type: str
    content: str
    version: str
    is_current: bool = True

# --- Response Models (Include ID) ---

class CarouselResponse(CarouselBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AnnouncementResponse(AnnouncementBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ClientDownloadResponse(ClientDownloadBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class FaqResponse(FaqBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class DocumentResponse(DocumentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class SystemConfigResponse(BaseModel):
    config_key: str
    config_value: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

# --- Aggregated Website Content Response ---

class WebsiteContentResponse(BaseModel):
    carousels: List[CarouselResponse]
    announcements: List[AnnouncementResponse]
    downloads: List[ClientDownloadResponse]
    faqs: List[FaqResponse]
    documents: List[DocumentResponse]
    configs: List[SystemConfigResponse]

