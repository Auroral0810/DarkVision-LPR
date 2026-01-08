from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import time, json
from typing import List

from app.core.database import get_db
from app.core.response import success_response, UnifiedResponse
from app.api.deps import get_current_active_admin
from app.schemas.admin.admin_user import PermissionCreate, PermissionUpdate, PermissionOut
from app.services.admin.admin_service import admin_service
from app.services import log_service

router = APIRouter()

@router.get("", summary="获取权限列表(树形)", response_model=UnifiedResponse[List[PermissionOut]])
def get_permissions(
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    perms = admin_service.get_permission_tree(db)
    return success_response(data=perms)

@router.post("", summary="创建权限", response_model=UnifiedResponse)
def create_permission(
    perm_in: PermissionCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    t1 = time.time()
    perm = admin_service.create_permission(db, perm_in)
    t2 = time.time()
    res = success_response(data=PermissionOut.model_validate(perm))
    log_service.create_log(
        db, current_admin.id, "permission", "create", 
        f"Created permission: {perm.name}", request=request,
        params=perm_in,
        duration=int((t2 - t1) * 1000),
        result=res
    )
    return res

@router.put("/{perm_id}", summary="更新权限", response_model=UnifiedResponse)
def update_permission(
    perm_id: int,
    perm_in: PermissionUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    t1 = time.time()
    perm = admin_service.update_permission(db, perm_id, perm_in)
    t2 = time.time()
    if not perm:
        raise HTTPException(status_code=404, detail="权限不存在")
    res = success_response(data=PermissionOut.model_validate(perm))
    log_service.create_log(
        db, current_admin.id, "permission", "update", 
        f"Updated permission: {perm.name}", request=request,
        params=perm_in,
        duration=int((t2 - t1) * 1000),
        result=res
    )
    return res

@router.delete("/{perm_id}", summary="删除权限", response_model=UnifiedResponse)
def delete_permission(
    perm_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    t1 = time.time()
    success = admin_service.delete_permission(db, perm_id)
    t2 = time.time()
    if not success:
        raise HTTPException(status_code=404, detail="权限不存在")
    res = success_response(message="删除成功")
    log_service.create_log(
        db, current_admin.id, "permission", "delete", 
        f"Deleted permission ID: {perm_id}", request=request,
        duration=int((t2 - t1) * 1000),
        result=res
    )
    return res
