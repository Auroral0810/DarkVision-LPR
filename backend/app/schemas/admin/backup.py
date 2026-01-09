from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class BackupBase(BaseModel):
    description: Optional[str] = None

class BackupCreate(BackupBase):
    pass

class BackupUpdate(BackupBase):
    pass

class BackupOut(BackupBase):
    id: int
    filename: str
    file_size: int
    created_at: datetime
    created_by: Optional[int]
    creator_name: Optional[str] = None
    status: str
    file_path: str

    class Config:
        from_attributes = True

class BackupQuery(BaseModel):
    page_num: int = 1
    page_size: int = 10
    start_time: Optional[str] = None
    end_time: Optional[str] = None
