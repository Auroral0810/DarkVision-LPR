from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.response import UnifiedResponse, success_response, error_response
from app.api.deps import get_current_active_admin
from app.models.user import User

from app.schemas.admin.admin_user import (
    AdminUserCreate, AdminUserUpdate, AdminUserOut
)
from app.services.admin.admin_service import admin_service
from app.services import log_service
import time

router = APIRouter()

@router.get("", response_model=UnifiedResponse[List[AdminUserOut]])
def get_admin_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    users = admin_service.get_admin_users(db)
    # Serialize to include roles
    list_data = []
    for u in users:
        # Schema expects `roles: List[RoleOut]`. 
        # `u.admin_roles` gives AdminRole objects. `ar.role` gives Role object.
        # We need to map `u.admin_roles` -> `[ar.role for ar in u.admin_roles]`
        # Pydantic via ORM mode might need help or `admin_roles` logic.
        # In `AdminUserOut`: roles: List[RoleOut].
        # User model has `admin_roles` relationship.
        # Let's populate manually or rely on `from_attributes`.
        # `u.admin_roles` is list of `AdminRole`. `RoleOut` expects `Role` fields.
        # `AdminRole` has `role` relationship.
        # We need to pass the list of roles, not list of AdminRoles.
        # But `AdminUserOut` is a Pydantic model. config `from_attributes=True` works if attribute name matches.
        # If `User` model has a property causing it to return list of roles, good. 
        # `User.admin_roles` -> `AdminRole` (junction).
        # We likely need to construct the list manually.
        
        u_out = AdminUserOut.model_validate(u)
        # Manually populate roles list
        actual_roles = [ar.role for ar in u.admin_roles]
        # RoleOut needs to be validated against these Role objects
        u_out.roles = actual_roles # Pydantic will validate if types match
        list_data.append(u_out)
        
    return success_response(data=list_data)

@router.post("", response_model=UnifiedResponse[AdminUserOut])
def create_admin_user(
    data: AdminUserCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    t1 = time.time()
    try:
        user = admin_service.create_admin_user(db, data)
    except ValueError as e:
        return error_response(message=str(e))
        
    t2 = time.time()
    
    # Prep response
    u_out = AdminUserOut.model_validate(user)
    u_out.roles = [ar.role for ar in user.admin_roles]
    
    res = success_response(data=u_out, message="管理员创建成功")
    log_service.create_log(
        db, current_user.id, "admin_user", "create", 
        f"Created admin user: {user.nickname}", request=request,
        params=data,
        duration=int((t2 - t1) * 1000),
        result=res
    )
    return res

@router.put("/{user_id}", response_model=UnifiedResponse[AdminUserOut])
def update_admin_user(
    user_id: int,
    data: AdminUserUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    t1 = time.time()
    user = admin_service.update_admin_user(db, user_id, data)
    if not user:
        return error_response(message="管理员不存在")
    t2 = time.time()
    
    u_out = AdminUserOut.model_validate(user)
    u_out.roles = [ar.role for ar in user.admin_roles]
    
    res = success_response(data=u_out, message="管理员更新成功")
    log_service.create_log(
        db, current_user.id, "admin_user", "update", 
        f"Updated admin user: {user.nickname}", request=request,
        params=data,
        duration=int((t2 - t1) * 1000),
        result=res
    )
    return res
