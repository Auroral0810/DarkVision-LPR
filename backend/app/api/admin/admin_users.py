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
    return success_response(data=users)

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
    u_out.roles = [RoleOut.model_validate(ar.role) for ar in user.admin_roles]
    
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
    u_out.roles = [RoleOut.model_validate(ar.role) for ar in user.admin_roles]
    
    res = success_response(data=u_out, message="管理员更新成功")
    log_service.create_log(
        db, current_user.id, "admin_user", "update", 
        f"Updated admin user: {user.nickname}", request=request,
        params=data,
        duration=int((t2 - t1) * 1000),
        result=res
    )
    return res
