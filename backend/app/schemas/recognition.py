from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime

class RecognitionResultResponse(BaseModel):
    id: int
    user_id: int
    original_image_url: str
    license_plate: str
    confidence: float
    bbox: Optional[List[Any]] = None
    plate_type: Optional[str] = None
    processed_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

class RecognitionTaskResponse(BaseModel):
    id: int
    task_uuid: str
    status: str
    progress: float
    total_items: Optional[int]
    success_count: int
    failed_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class BatchRecognitionRequest(BaseModel):
    image_urls: List[str] = Field(..., max_items=50, description="OSS image URLs list, max 50")
