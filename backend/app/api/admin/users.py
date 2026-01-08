from fastapi import APIRouter, Depends, HTTPException, Query, status, Response, Request
from app.services import log_service
from fastapi.responses import StreamingResponse
from datetime import datetime
import time, json
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.response import success_response, UnifiedResponse, success # Added success
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
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    t1 = time.time()
    user = user_service.admin_create_user(db, user_in)
    t2 = time.time()
    res = success_response(data=AdminUserListItem.model_validate(user))
    log_service.create_log(
        db, current_admin.id, "user", "create", 
        f"Created user {user.phone}", request=request,
        params=user_in,
        duration=int((t2 - t1) * 1000),
        result=res
    )
    return res

@router.get("/export", summary="导出用户列表")
def export_users(
    params: UserListParams = Depends(),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    """
    导出当前过滤条件下的所有用户数据到 CSV
    """
    # 强制将每页数量设为极大值以一次性导出所有匹配数据
    params.page = 1
    params.page_size = 100000
    
    users, _ = user_service.list_users_for_admin(db, params)
    csv_content = user_service.generate_user_csv(users)
    
    filename = f"users_export_{datetime.now().strftime('%Y%m%d%H%M')}.csv"
    
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )

@router.get("/{user_id}/export", summary="导出用户详情报告")
def get_user_export(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    """
    导出用户的 Word 详情报告
    """
    user_detail = user_service.get_user_detail_info(db, user_id)
    if not user_detail:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    docx_stream = user_service.generate_user_detail_docx(user_detail)
    filename = f"user_report_{user_id}_{datetime.now().strftime('%Y%m%d')}.docx"
    
    return Response(
        content=docx_stream.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )

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
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    db_user = user_service.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    t1 = time.time()
    user = user_service.admin_update_user(db, db_user, user_in)
    t2 = time.time()
    res = success_response(data=AdminUserListItem.model_validate(user))
    log_service.create_log(
        db, current_admin.id, "user", "update", 
        f"Updated user {db_user.phone}", request=request,
        params=user_in,
        duration=int((t2 - t1) * 1000),
        result=res
    )
    return res

@router.put("/{user_id}/type", summary="修改用户类型", response_model=UnifiedResponse)
def update_user_type(
    user_id: int,
    type_in: AdminUpdateUserType,
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    db_user = user_service.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    t1 = time.time()
    old_type = db_user.user_type
    db_user.user_type = type_in.user_type
    db.commit()
    db.refresh(db_user)
    t2 = time.time()
    res = success_response(message="修改成功")
    log_service.create_log(
        db, current_admin.id, "user", "update_type", 
        f"Changed user {db_user.phone} type from {old_type} to {type_in.user_type}", 
        request=request, params=type_in,
        duration=int((t2 - t1) * 1000),
        result=res
    )
    return res

@router.post("/ban", summary="封禁用户", response_model=UnifiedResponse)
def ban_user(
    req: BanUserRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    db_user = user_service.get_user_by_id(db, req.user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    t1 = time.time()
    user_service.ban_user(db, db_user, req.reason, req.banned_until)
    t2 = time.time()
    res = success_response(message="封禁成功")
    log_service.create_log(
        db, current_admin.id, "user", "ban", 
        f"Banned user {db_user.phone} until {req.banned_until}", 
        request=request, params=req,
        duration=int((t2 - t1) * 1000),
        result=res
    )
    return res

@router.post("/{user_id}/unban", summary="解封用户", response_model=UnifiedResponse)
def unban_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    db_user = user_service.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    t1 = time.time()
    user_service.unban_user(db, db_user)
    t2 = time.time()
    res = success_response(message="解封成功")
    log_service.create_log(
        db, current_admin.id, "user", "unban", 
        f"Unbanned user {db_user.phone}", request=request,
        duration=int((t2 - t1) * 1000),
        result=res
    )
    return res

@router.post("/{user_id}/reset-password", summary="重置密码", response_model=UnifiedResponse)
def reset_password(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    db_user = user_service.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    t1 = time.time()
    new_pwd = user_service.reset_user_password(db, db_user)
    t2 = time.time()
    res = success_response(data={"new_password": new_pwd}, message="密码已重置")
    log_service.create_log(
        db, current_admin.id, "user", "reset_pwd", 
        f"Reset password for user {db_user.phone}", request=request,
        duration=int((t2 - t1) * 1000),
        result=res
    )
    return res

@router.post("/{user_id}/force-logout", summary="强制下线", response_model=UnifiedResponse)
async def force_logout(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    from app.services.auth import logout_user
    db_user = user_service.get_user_by_id(db, user_id)
    t1 = time.time()
    logout_user(user_id)
    
    # 实时推送下线通知
    try:
        from app.services.websocket_manager import manager
        await manager.broadcast_to_user(user_id, {
            "type": "force_logout",
            "message": "您已被管理员强制下线"
        })
    except Exception as e:
        # Avoid direct logger call if not imported properly or use app logger
        from app.core.logger import logger
        logger.warning(f"Failed to send websocket notification: {e}")
    t2 = time.time()
        
    res = success_response(message="已强制用户下线")
    log_service.create_log(
        db, current_admin.id, "user", "force_logout", 
        f"Force direct logout for user {db_user.phone if db_user else user_id}", request=request,
        duration=int((t2 - t1) * 1000),
        result=res
    )
    return res

@router.post("/batch-delete", summary="批量删除用户", response_model=UnifiedResponse)
def batch_delete(
    req: BatchDeleteRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    t1 = time.time()
    count = user_service.batch_delete_users(db, req.user_ids)
    t2 = time.time()
    res = success_response(message=f"成功删除 {count} 个用户")
    log_service.create_log(
        db, current_admin.id, "user", "batch_delete", 
        f"Batch deleted {count} users", request=request,
        params=req,
        duration=int((t2 - t1) * 1000),
        result=res
    )
    return res
