from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.recognition import RecognitionResultResponse

class RecognitionHistoryParams(BaseModel):
    page: int = 1
    page_size: int = 10
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    license_plate: Optional[str] = None
    plate_type: Optional[str] = None

class RecognitionHistoryItem(RecognitionResultResponse):
    pass

class RecognitionHistoryList(BaseModel):
    items: List[RecognitionHistoryItem]
    total: int
    page: int
    page_size: int
    total_pages: int

class RecognitionHistoryStats(BaseModel):
    total_count: int
    today_count: int
    success_rate: float
