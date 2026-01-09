from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime

# --- Cache Management ---
class CacheStats(BaseModel):
    redis_version: str
    uptime_in_seconds: int
    used_memory_human: str
    connected_clients: int
    keys_count: int

class CacheKeyInfo(BaseModel):
    key: str
    type: str
    ttl: int
    size: int

class CacheClearRequest(BaseModel):
    prefix: Optional[str] = None
    keys: Optional[List[str]] = None

# --- Task Scheduling ---
class SystemTaskBase(BaseModel):
    name: str
    task_code: str
    cron_expression: str
    remark: Optional[str] = None
    status: int = 1

class SystemTaskCreate(SystemTaskBase):
    pass

class SystemTaskUpdate(BaseModel):
    name: Optional[str] = None
    cron_expression: Optional[str] = None
    remark: Optional[str] = None
    status: Optional[int] = None

class SystemTaskOut(SystemTaskBase):
    id: int
    last_run_at: Optional[datetime] = None
    next_run_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Version Update ---
class SystemVersionBase(BaseModel):
    version_number: str
    title: str
    content: str
    type: str = "system"
    is_force: int = 0
    download_url: Optional[str] = None

class SystemVersionCreate(SystemVersionBase):
    pass

class SystemVersionUpdate(BaseModel):
    version_number: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    type: Optional[str] = None
    is_force: Optional[int] = None
    download_url: Optional[str] = None

class SystemVersionOut(SystemVersionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
