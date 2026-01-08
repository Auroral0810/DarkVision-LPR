from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import time
from typing import List, Optional

from app.core.database import get_db
from app.core.response import success_response, UnifiedResponse
from app.api.deps import get_current_active_admin
from app.schemas.admin.system import (
    OperationLogOut, LogListParams, 
    IpRuleOut, IpRuleCreate, IpRuleUpdate,
    SecurityConfigOut, SecurityConfigUpdate,
    SystemLogOut, SystemLogParams
)
from app.services import log_service
import json
from app.services import user as user_service
from app.services import security_service

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
        end_time=params.end_time,
        order_by=params.order_by,
        order_type=params.order_type
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

@router.get("/logs/system", summary="系统日志(文件)", response_model=UnifiedResponse)
def get_system_logs(
    params: SystemLogParams = Depends(),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    data = log_service.get_system_logs(params.log_type, params.lines)
    return success_response(data=data)

# --- IP Rules ---
@router.get("/ip-rules", summary="IP规则列表", response_model=UnifiedResponse)
def get_ip_rules(
    rule_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    rules = security_service.get_ip_rules(db, rule_type)
    return success_response(data=[IpRuleOut.model_validate(r) for r in rules])

@router.post("/ip-rules", summary="添加IP规则", response_model=UnifiedResponse)
def add_ip_rule(
    rule_in: IpRuleCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    t1 = time.time()
    rule = security_service.add_ip_rule(db, rule_in)
    t2 = time.time()
    res = success_response(data=IpRuleOut.model_validate(rule))
    log_service.create_log(
        db, current_admin.id, "system", "add_ip_rule", 
        f"Added IP rule: {rule.ip_address} ({rule.type})", 
        request=request, params=rule_in.model_dump_json(),
        duration=int((t2 - t1) * 1000),
        result=json.dumps(res, ensure_ascii=False)
    )
    return res

@router.delete("/ip-rules/{id}", summary="删除IP规则", response_model=UnifiedResponse)
def delete_ip_rule(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    t1 = time.time()
    success = security_service.delete_ip_rule(db, id)
    t2 = time.time()
    if not success:
        raise HTTPException(status_code=404, detail="Rule not found")
    res = success_response(message="删除成功")
    log_service.create_log(
        db, current_admin.id, "system", "delete_ip_rule", 
        f"Deleted IP rule ID: {id}", request=request,
        duration=int((t2 - t1) * 1000),
        result=json.dumps(res, ensure_ascii=False)
    )
    return res

# --- Security Config ---
@router.get("/security/config", summary="获取安全配置", response_model=UnifiedResponse)
def get_security_config(
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    config = security_service.get_security_config(db)
    return success_response(data=config)

@router.put("/security/config", summary="更新安全配置", response_model=UnifiedResponse)
def update_security_config(
    config_in: SecurityConfigUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    t1 = time.time()
    config = security_service.update_security_config(db, config_in)
    t2 = time.time()
    res = success_response(data=config)
    log_service.create_log(
        db, current_admin.id, "system", "update_security_config", 
        f"Updated security configuration", 
        request=request, params=config_in.model_dump_json(),
        duration=int((t2 - t1) * 1000),
        result=json.dumps(res, ensure_ascii=False)
    )
    return res
