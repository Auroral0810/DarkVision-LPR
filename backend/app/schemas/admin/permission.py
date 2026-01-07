from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PermissionBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    type: str = "menu"
    parent_id: Optional[int] = None
    path: Optional[str] = None
    component: Optional[str] = None
    icon: Optional[str] = None
    sort_order: int = 0

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    parent_id: Optional[int] = None
    path: Optional[str] = None
    component: Optional[str] = None
    icon: Optional[str] = None
    sort_order: Optional[int] = None

class PermissionOut(PermissionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    children: List['PermissionOut'] = []

    class Config:
        from_attributes = True

PermissionOut.model_rebuild()

class PermissionTree(PermissionOut):
    pass
