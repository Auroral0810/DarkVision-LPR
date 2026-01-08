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
    result: Optional[str]
    params: Optional[str]
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
    order_by: Optional[str] = "created_at"
    order_type: Optional[str] = "desc" # desc or asc

# --- IP Rules ---
class IpRuleBase(BaseModel):
    ip_address: str
    type: str  # allow / deny
    remark: Optional[str] = None

class IpRuleCreate(IpRuleBase):
    pass

class IpRuleUpdate(BaseModel):
    type: Optional[str] = None
    remark: Optional[str] = None

class IpRuleOut(IpRuleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Security Config ---
class SecurityConfigOut(BaseModel):
    login_fail_limit: int = 5
    login_lock_duration: int = 30  # minutes
    api_rate_limit: int = 100  # requests per minute
    enable_ip_whitelist: bool = False

class SecurityConfigUpdate(BaseModel):
    login_fail_limit: Optional[int] = None
    login_lock_duration: Optional[int] = None
    api_rate_limit: Optional[int] = None
    enable_ip_whitelist: Optional[bool] = None

# --- System Logs (from files) ---
class SystemLogOut(BaseModel):
    content: str
    filename: str
    total_lines: int

class SystemLogParams(BaseModel):
    log_type: str = "app"  # app or error
    lines: int = 100
