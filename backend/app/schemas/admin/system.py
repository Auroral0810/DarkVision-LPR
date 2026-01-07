from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OperationLogOut(BaseModel):
    id: int
    admin_id: Optional[int]
    module: str
    action: str
    description: Optional[str]
    method: Optional[str]
    path: Optional[str]
    ip_address: Optional[str]
    status: int
    duration: Optional[int]
    created_at: datetime
    admin_username: Optional[str] = None # Calculated field

    class Config:
        from_attributes = True

class LogListParams(BaseModel):
    page: int = 1
    page_size: int = 20
    module: Optional[str] = None
    admin_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
