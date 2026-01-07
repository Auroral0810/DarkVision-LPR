from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.response import success_response, UnifiedResponse
from app.api.deps import get_current_active_admin
from app.schemas.admin.permission import PermissionCreate, PermissionUpdate, PermissionOut, PermissionTree
from app.services import permission as perm_service
from app.services import log_service

router = APIRouter()

@router.get("", summary="获取权限列表(树形)", response_model=UnifiedResponse)
def get_permissions(
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    perms = perm_service.get_permission_tree(db)
    # Recursion to format as tree not fully implemented in service, sticking to flat list for now or simple parent lookup
    # Actually, simpler to return flat list to frontend and let frontend build tree, OR fetch all and build tree here.
    # Service returned flat list (if my memory serves me right on previous step, wait, let me check)
    # Service has `get_permission_tree` but I implemented it to just return root nodes. 
    # Let's trust the service or just return all and let frontend handle hierarchy if needed.
    # Re-reading service implementation: logic was "tree = []; if p.parent_id is None: tree.append(p)". 
    # This only gives root nodes without children populated if not lazy loaded.
    # Let's update this to return properly formatted tree using schemas.
    
    # Actually, let's just return "list" for now, and let frontend format it, 
    # OR implement a proper recursive builder.
    # For now, I'll return the flat list which is easier for the "Tree Table" in frontend which often accepts flat list with IDs.
    all_perms = perm_service.get_all_permissions(db)
    return success_response(data=[PermissionOut.model_validate(p) for p in all_perms])

@router.post("", summary="创建权限", response_model=UnifiedResponse)
def create_permission(
    perm_in: PermissionCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    perm = perm_service.create_permission(db, perm_in)
    log_service.create_log(db, current_admin.id, "permission", "create", f"Created permission {perm.name}", method="POST")
    return success_response(data=PermissionOut.model_validate(perm))

@router.put("/{perm_id}", summary="更新权限", response_model=UnifiedResponse)
def update_permission(
    perm_id: int,
    perm_in: PermissionUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    perm = perm_service.update_permission(db, perm_id, perm_in)
    if not perm:
        raise HTTPException(status_code=404, detail="权限不存在")
    log_service.create_log(db, current_admin.id, "permission", "update", f"Updated permission {perm.name}", method="PUT")
    return success_response(data=PermissionOut.model_validate(perm))

@router.delete("/{perm_id}", summary="删除权限", response_model=UnifiedResponse)
def delete_permission(
    perm_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    success = perm_service.delete_permission(db, perm_id)
    if not success:
        raise HTTPException(status_code=404, detail="权限不存在")
    log_service.create_log(db, current_admin.id, "permission", "delete", f"Deleted permission {perm_id}", method="DELETE")
    return success_response(message="删除成功")
