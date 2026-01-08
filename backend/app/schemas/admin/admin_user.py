from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.schemas.user import UserBase

# --- Permission ---
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
    category: Optional[str] = None

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
    category: Optional[str] = None

class PermissionOut(PermissionBase):
    id: int
    created_at: datetime
    children: Optional[List['PermissionOut']] = None
    model_config = ConfigDict(from_attributes=True)

# --- Role ---
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_system: bool = False

class RoleCreate(RoleBase):
    permission_ids: List[int] = []

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permission_ids: Optional[List[int]] = None

class RoleOut(RoleBase):
    id: int
    created_at: datetime
    # We might return permission_ids or full permission objects
    # For list view we might not need them, but for edit we do.
    # Let's include ids for simplicity in UI mapping
    permission_ids: List[int] = [] 

    model_config = ConfigDict(from_attributes=True)

# --- Admin User ---
class AdminUserCreate(BaseModel):
    nickname: str
    phone: str
    password: str
    role_ids: List[int] = []
    real_name: Optional[str] = None # For profile

class AdminUserUpdate(BaseModel):
    nickname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None # Optional reset
    role_ids: Optional[List[int]] = None
    is_active: Optional[bool] = None

class AdminUserOut(UserBase):
    id: int
    user_type: str
    status: str
    created_at: datetime
    roles: List[RoleOut] = []
    
    model_config = ConfigDict(from_attributes=True)
