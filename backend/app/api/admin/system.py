from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.response import success_response, UnifiedResponse
from app.api.deps import get_current_active_admin
from app.schemas.admin.system import OperationLogOut, LogListParams
from app.services import log_service
from app.services import user as user_service

router = APIRouter()

@router.get("/logs", summary="操作日志列表", response_model=UnifiedResponse)
def get_logs(
    params: LogListParams = Depends(),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    logs, total = log_service.list_logs(
        db, 
        page=params.page, 
        page_size=params.page_size, 
        module=params.module, 
        admin_id=params.admin_id,
        start_time=params.start_time,
        end_time=params.end_time
    )
    
    # Enrich with admin username/nickname if needed, currently OperationLog has relationship 'admin'
    
    list_data = []
    for log in logs:
        log_out = OperationLogOut.model_validate(log)
        if log.admin:
            log_out.admin_username = log.admin.nickname
        list_data.append(log_out)
        
    return success_response(data={
        "list": list_data,
        "total": total,
        "page": params.page,
        "pageSize": params.page_size
    })
