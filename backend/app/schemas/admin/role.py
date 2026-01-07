from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.admin.permission import PermissionOut

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    permission_ids: List[int] = []

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permission_ids: Optional[List[int]] = None

class RoleOut(RoleBase):
    id: int
    is_system: bool
    created_at: datetime
    # permissions: List[PermissionOut] = [] # Optional to include detailed permissions
    permission_ids: List[int] = []  # Just return IDs for easier frontend handling
    permissions: List[PermissionOut] = [] # Return full permission objects as well

    class Config:
        from_attributes = True

class RoleDetail(RoleOut):
    permissions: List[PermissionOut] = []
