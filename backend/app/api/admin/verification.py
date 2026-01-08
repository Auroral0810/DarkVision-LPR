from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import Any

from app.core.database import get_db
from app.core.response import success_response, UnifiedResponse
from app.api.deps import get_current_active_admin
from app.services.verification import verification_service
from app.utils.image import get_image_url
from app.services import log_service
from app.schemas.admin.verification import (
    VerificationListParams, 
    VerificationListItem, 
    VerificationAuditRequest,
    VerificationUserSimple
)

router = APIRouter()

@router.get("", summary="获取实名认证列表", response_model=UnifiedResponse)
def list_verifications(
    params: VerificationListParams = Depends(),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    items, total = verification_service.list_verifications(db, params)
    
    # 手动组装响应数据，因为涉及跨表字段映射
    data_list = []
    for v in items:
        # 获取关联的 UserProfile 信息
        profile = v.user.profile if v.user and v.user.profile else None
        
        item_dict = {
            "id": v.id,
            "user_id": v.user_id,
            "user": VerificationUserSimple(
                id=v.user.id,
                nickname=v.user.nickname,
                phone=v.user.phone,
                email=v.user.email,
                avatar_url=get_image_url(v.user.avatar_url)
            ),
            "real_name": profile.real_name if profile else None,
            "id_card_number": profile.id_card_number if profile else None,
            "id_card_front": get_image_url(v.id_card_front),
            "id_card_back": get_image_url(v.id_card_back),
            "face_photo": get_image_url(v.face_photo),
            "status": v.status,
            "reject_reason": v.reject_reason,
            "created_at": v.created_at,
            "updated_at": None,
            "reviewed_at": v.reviewed_at,
            "reviewer_id": v.reviewed_by
        }
        data_list.append(item_dict)

    return success_response({
        "list": data_list,
        "total": total,
        "page": params.page,
        "pageSize": params.page_size
    })

@router.post("/{id}/audit", summary="审核实名认证")
def audit_verification(
    id: int,
    audit_in: VerificationAuditRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    import time, json
    if audit_in.action == 'reject' and not audit_in.reject_reason:
        raise HTTPException(status_code=400, detail="驳回必须填写原因")
        
    t1 = time.time()
    result = verification_service.audit_verification(
        db, 
        verification_id=id, 
        admin_id=current_admin.id, 
        action=audit_in.action, 
        reason=audit_in.reject_reason
    )
    t2 = time.time()
    
    if not result:
        raise HTTPException(status_code=404, detail="认证记录不存在")
    
    res = success_response(message="审核完成")
    log_service.create_log(
        db, current_admin.id, "verification", "audit", 
        f"Audited verification ID: {id}, action: {audit_in.action}", 
        request=request, params=audit_in,
        duration=int((t2 - t1) * 1000),
        result=res
    )
    
    return res
