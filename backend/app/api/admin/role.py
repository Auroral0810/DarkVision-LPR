from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
import time, json
from typing import List

from app.core.database import get_db
from app.core.response import success_response, UnifiedResponse
from app.api.deps import get_current_active_admin
from app.schemas.admin.admin_user import RoleCreate, RoleUpdate, RoleOut
from app.services.admin.admin_service import admin_service
from app.services import log_service
from app.models.role import Role

router = APIRouter()

@router.get("", summary="获取角色列表", response_model=UnifiedResponse)
def get_roles(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    # Service handles Redis caching and returns either List[Dict] (cached) or List[Role] (db)
    all_roles = admin_service.get_roles(db)
    
    if not all_roles:
        return success_response(data={"list": [], "total": 0, "page": page, "pageSize": page_size})
        
    # Process into list of dicts consistent with schema
    processed_list = []
    if isinstance(all_roles[0], dict):
        processed_list = all_roles
    else:
        for r in all_roles:
            r_out = RoleOut.model_validate(r)
            r_out.permission_ids = [rp.permission_id for rp in r.role_permissions] 
            processed_list.append(r_out.model_dump())

    # Pagination
    total = len(processed_list)
    start = (page - 1) * page_size
    end = start + page_size
    paged_data = processed_list[start:end]

    return success_response(data={
        "list": paged_data,
        "total": total,
        "page": page,
        "pageSize": page_size
    })


@router.get("/{role_id}", summary="获取角色详情", response_model=UnifiedResponse[RoleOut])
def get_role_detail(
    role_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    # For detail, we don't usually cache individually in this service yet
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    
    # Build detail with full permission objects if needed
    # Schema RoleDetail uses permissions: List[PermissionOut] 
    # But for frontend assignment we mainly need IDs.
    # Let's provide both if possible or just what's needed.
    
    # Construct response manually to be safe
    # permissions = [rp.permission for rp in role.role_permissions]
    # ... actually standard model_validate with ORM mode should work if relations are loaded.
    # But `role.permissions` relation isn't explicitly defined in model (commented out), we used `role_permissions`.
    
    # Let's use RoleDetail schema which expects `permissions`.
    # We need to adapt.
    
    # Actually, let's keep it simple: populate permission_ids.
    r_out = RoleOut.model_validate(role)
    r_out.permission_ids = [rp.permission_id for rp in role.role_permissions]
    return success_response(data=r_out)

@router.post("", summary="创建角色", response_model=UnifiedResponse)
def create_role(
    role_in: RoleCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    t1 = time.time()
    role = admin_service.create_role(db, role_in)
    t2 = time.time()
    res = success_response(data=RoleOut.model_validate(role))
    log_service.create_log(
        db, current_admin.id, "role", "create", 
        f"Created role: {role.name}", request=request,
        params=role_in,
        duration=int((t2 - t1) * 1000),
        result=res
    )
    return res

@router.put("/{role_id}", summary="更新角色", response_model=UnifiedResponse)
def update_role(
    role_id: int,
    role_in: RoleUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    t1 = time.time()
    role = admin_service.update_role(db, role_id, role_in)
    t2 = time.time()
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    res = success_response(data=RoleOut.model_validate(role))
    log_service.create_log(
        db, current_admin.id, "role", "update", 
        f"Updated role: {role.name}", request=request,
        params=role_in,
        duration=int((t2 - t1) * 1000),
        result=res
    )
    return res

@router.delete("/{role_id}", summary="删除角色", response_model=UnifiedResponse)
def delete_role(
    role_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    t1 = time.time()
    success = admin_service.delete_role(db, role_id)
    t2 = time.time()
    if not success:
        raise HTTPException(status_code=404, detail="角色不存在")
    res = success_response(message="删除成功")
    log_service.create_log(
        db, current_admin.id, "role", "delete", 
        f"Deleted role ID: {role_id}", request=request,
        duration=int((t2 - t1) * 1000),
        result=res
    )
    return res
