from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# --- Recognition Task ---
class RecognitionTaskOut(BaseModel):
    id: int
    task_uuid: str
    user_id: int
    task_type: str
    status: str
    progress: Decimal
    total_items: Optional[int]
    success_count: int
    failed_count: int
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class TaskListParams(BaseModel):
    page: int = 1
    page_size: int = 20
    status: Optional[str] = None
    task_type: Optional[str] = None
    user_id: Optional[int] = None

# --- Recognition Record ---
class RecognitionRecordOut(BaseModel):
    id: int
    task_id: Optional[int]
    user_id: int
    original_image_url: str
    enhanced_image_url: Optional[str]
    license_plate: str
    plate_type: Optional[str]
    confidence: float
    bbox: Optional[List[int]]
    enhance_algorithm: Optional[str]
    model_version: Optional[str]
    processing_time: Optional[float]
    processed_at: datetime
    model_config = ConfigDict(
        from_attributes=True,
        protected_namespaces=()
    )

class RecordListParams(BaseModel):
    page: int = 1
    page_size: int = 20
    user_id: Optional[int] = None
    license_plate: Optional[str] = None
    plate_type: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

# --- Recognition Model ---
class RecognitionModelCreate(BaseModel):
    version: str = Field(..., max_length=20)
    name: str = Field(..., max_length=100)
    accuracy: Optional[Decimal] = None
    description: Optional[str] = None
    file_path: Optional[str] = None
    is_active: bool = False

class RecognitionModelUpdate(BaseModel):
    name: Optional[str] = None
    accuracy: Optional[Decimal] = None
    description: Optional[str] = None
    file_path: Optional[str] = None
    is_active: Optional[bool] = None

class RecognitionModelOut(BaseModel):
    id: int
    version: str
    name: str
    is_active: bool
    accuracy: Optional[Decimal]
    description: Optional[str]
    file_path: Optional[str]
    model_config = ConfigDict(from_attributes=True)

class ModelListParams(BaseModel):
    is_active: Optional[bool] = None
