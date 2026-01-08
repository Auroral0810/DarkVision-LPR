from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
import time, json
from typing import List

from app.core.database import get_db
from app.core.response import success_response, UnifiedResponse
from app.api.deps import get_current_active_admin
from app.schemas.admin.role import RoleCreate, RoleUpdate, RoleOut, RoleDetail
from app.services import role as role_service
from app.services import log_service

router = APIRouter()

@router.get("", summary="获取角色列表", response_model=UnifiedResponse)
def get_roles(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    roles, total = role_service.list_roles(db, skip=(page - 1) * page_size, limit=page_size)
    list_data = []
    
    # Needs to handle permission IDs extraction if schema requires it, 
    # but RoleOut defined permission_ids as List[int].
    # SQLAlchemy model doesn't have `permission_ids` property by default, need to extract.
    for r in roles:
        r_out = RoleOut.model_validate(r)
        # Manually populate permission_ids
        r_out.permission_ids = [rp.permission_id for rp in r.role_permissions] 
        list_data.append(r_out)

    return success_response(data={
        "list": list_data,
        "total": total,
        "page": page,
        "pageSize": page_size
    })

@router.get("/all", summary="获取所有角色(不分页)", response_model=UnifiedResponse)
def get_all_roles(
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    roles = role_service.get_all_roles(db)
    return success_response(data=[RoleOut.model_validate(r) for r in roles])

@router.get("/{role_id}", summary="获取角色详情", response_model=UnifiedResponse)
def get_role_detail(
    role_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    role = role_service.get_role_by_id(db, role_id)
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
    role = role_service.create_role(db, role_in)
    t2 = time.time()
    res = success_response(data=RoleOut.model_validate(role))
    log_service.create_log(
        db, current_admin.id, "role", "create", 
        f"Created role: {role.name}", request=request,
        params=role_in.model_dump_json(),
        duration=int((t2 - t1) * 1000),
        result=json.dumps(res, ensure_ascii=False)
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
    role = role_service.update_role(db, role_id, role_in)
    t2 = time.time()
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    res = success_response(data=RoleOut.model_validate(role))
    log_service.create_log(
        db, current_admin.id, "role", "update", 
        f"Updated role: {role.name}", request=request,
        params=role_in.model_dump_json(),
        duration=int((t2 - t1) * 1000),
        result=json.dumps(res, ensure_ascii=False)
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
    success = role_service.delete_role(db, role_id)
    t2 = time.time()
    if not success:
        raise HTTPException(status_code=404, detail="角色不存在")
    res = success_response(message="删除成功")
    log_service.create_log(
        db, current_admin.id, "role", "delete", 
        f"Deleted role ID: {role_id}", request=request,
        duration=int((t2 - t1) * 1000),
        result=json.dumps(res, ensure_ascii=False)
    )
    return res
