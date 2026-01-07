from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.response import success_response, UnifiedResponse
from app.services import user as user_service
from app.schemas.admin.user import (
    AdminUserListItem, UserListParams, AdminUserDetail,
    AdminUserCreate, AdminUserUpdate, AdminUpdateUserType,
    BanUserRequest, BatchDeleteRequest, ResetPasswordResponse
)
from app.schemas.user import UserDetailInfo
from app.api.deps import get_current_active_admin

router = APIRouter()

@router.get("", summary="获取用户列表", response_model=UnifiedResponse)
def get_users(
    params: UserListParams = Depends(),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    users, total = user_service.list_users_for_admin(db, params)
    data = {
        "list": [AdminUserListItem.model_validate(u) for u in users],
        "total": total,
        "page": params.page,
        "pageSize": params.page_size
    }
    return success_response(data=data)

@router.post("", summary="创建用户", response_model=UnifiedResponse)
def create_user(
    user_in: AdminUserCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    user = user_service.admin_create_user(db, user_in)
    return success_response(data=AdminUserListItem.model_validate(user))

@router.get("/export", summary="导出用户列表", response_model=UnifiedResponse)
def export_users(
    params: UserListParams = Depends(),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    # TODO: 实现真正的 Excel 导出逻辑
    # 目前仅返回已过滤的数据统计或占位
    return success_response(message="正在准备导出数据...")

@router.get("/{user_id}", summary="获取用户详情", response_model=UnifiedResponse)
def get_user_detail(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    user_detail = user_service.get_user_detail_info(db, user_id)
    if not user_detail:
        raise HTTPException(status_code=404, detail="用户不存在")
    return success_response(data=user_detail)

@router.put("/{user_id}", summary="编辑用户信息", response_model=UnifiedResponse)
def update_user(
    user_id: int,
    user_in: AdminUserUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    db_user = user_service.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    user = user_service.admin_update_user(db, db_user, user_in)
    return success_response(data=AdminUserListItem.model_validate(user))

@router.put("/{user_id}/type", summary="修改用户类型", response_model=UnifiedResponse)
def update_user_type(
    user_id: int,
    type_in: AdminUpdateUserType,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    db_user = user_service.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    db_user.user_type = type_in.user_type
    db.commit()
    db.refresh(db_user)
    return success_response(message="修改成功")

@router.post("/ban", summary="封禁用户", response_model=UnifiedResponse)
def ban_user(
    req: BanUserRequest,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    db_user = user_service.get_user_by_id(db, req.user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    user_service.ban_user(db, db_user, req.reason, req.banned_until)
    return success_response(message="封禁成功")

@router.post("/{user_id}/unban", summary="解封用户", response_model=UnifiedResponse)
def unban_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    db_user = user_service.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    user_service.unban_user(db, db_user)
    return success_response(message="解封成功")

@router.post("/{user_id}/reset-password", summary="重置密码", response_model=UnifiedResponse)
def reset_password(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    db_user = user_service.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    new_pwd = user_service.reset_user_password(db, db_user)
    return success_response(data={"new_password": new_pwd}, message="密码已重置")

@router.post("/{user_id}/force-logout", summary="强制下线", response_model=UnifiedResponse)
def force_logout(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    from app.services.auth import logout_user
    logout_user(user_id)
    return success_response(message="已强制用户下线")

@router.post("/batch-delete", summary="批量删除用户", response_model=UnifiedResponse)
def batch_delete(
    req: BatchDeleteRequest,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    count = user_service.batch_delete_users(db, req.user_ids)
    return success_response(message=f"成功删除 {count} 个用户")
