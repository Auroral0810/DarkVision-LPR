from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import time
from typing import List

from app.core.database import get_db
from app.core.response import success_response, UnifiedResponse
from app.api.deps import get_current_active_admin
from app.services.admin import recognition as recon_admin_service
from app.services import log_service
from app.schemas.admin.recognition import (
    RecognitionTaskOut, TaskListParams,
    RecognitionRecordOut, RecordListParams,
    RecognitionModelOut, RecognitionModelCreate, RecognitionModelUpdate, ModelListParams
)

router = APIRouter()

# --- Recognition Tasks ---
@router.get("/tasks", summary="获取识别任务列表", response_model=UnifiedResponse)
def get_tasks(
    params: TaskListParams = Depends(),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    tasks, total = recon_admin_service.list_tasks(db, params)
    return success_response(data={
        "list": [RecognitionTaskOut.model_validate(t) for t in tasks],
        "total": total
    })

@router.delete("/tasks/{id}", summary="删除识别任务", response_model=UnifiedResponse)
def delete_task(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    t1 = time.time()
    success = recon_admin_service.delete_task(db, id)
    t2 = time.time()
    
    if not success:
        raise HTTPException(status_code=404, detail="任务不存在")
        
    res = success_response(message="删除成功")
    log_service.create_log(
        db, current_admin.id, "recognition", "delete_task", 
        f"Deleted task ID: {id}", request=request,
        duration=int((t2 - t1) * 1000), result=res
    )
    return res

# --- Recognition Records ---
@router.get("/records", summary="获取识别记录列表", response_model=UnifiedResponse)
def get_records(
    params: RecordListParams = Depends(),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    records, total = recon_admin_service.list_records(db, params)
    return success_response(data={
        "list": [RecognitionRecordOut.model_validate(r) for r in records],
        "total": total
    })

@router.delete("/records/{id}", summary="删除识别记录", response_model=UnifiedResponse)
def delete_record(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    t1 = time.time()
    success = recon_admin_service.delete_record(db, id)
    t2 = time.time()
    
    if not success:
        raise HTTPException(status_code=404, detail="记录不存在")
        
    res = success_response(message="删除成功")
    log_service.create_log(
        db, current_admin.id, "recognition", "delete_record", 
        f"Deleted record ID: {id}", request=request,
        duration=int((t2 - t1) * 1000), result=res
    )
    return res

# --- Model Management ---
@router.get("/models", summary="获取模型列表", response_model=UnifiedResponse)
def get_models(
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    models = recon_admin_service.list_models(db)
    return success_response(data=[RecognitionModelOut.model_validate(m) for m in models])

@router.post("/models", summary="创建模型版本", response_model=UnifiedResponse)
def create_model(
    model_in: RecognitionModelCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    t1 = time.time()
    model = recon_admin_service.create_model(db, model_in)
    t2 = time.time()
    
    res = success_response(data=RecognitionModelOut.model_validate(model))
    log_service.create_log(
        db, current_admin.id, "recognition", "create_model", 
        f"Created model version: {model.version}", request=request,
        params=model_in,
        duration=int((t2 - t1) * 1000), result=res
    )
    return res

@router.put("/models/{id}", summary="更新模型版本", response_model=UnifiedResponse)
def update_model(
    id: int,
    model_in: RecognitionModelUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    t1 = time.time()
    model = recon_admin_service.update_model(db, id, model_in)
    t2 = time.time()
    
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")
        
    res = success_response(data=RecognitionModelOut.model_validate(model))
    log_service.create_log(
        db, current_admin.id, "recognition", "update_model", 
        f"Updated model version: {model.version}", request=request,
        params=model_in,
        duration=int((t2 - t1) * 1000), result=res
    )
    return res

@router.delete("/models/{id}", summary="删除模型版本", response_model=UnifiedResponse)
def delete_model(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    t1 = time.time()
    success = recon_admin_service.delete_model(db, id)
    t2 = time.time()
    
    if not success:
        raise HTTPException(status_code=404, detail="模型不存在")
        
    res = success_response(message="删除成功")
    log_service.create_log(
        db, current_admin.id, "recognition", "delete_model", 
        f"Deleted model ID: {id}", request=request,
        duration=int((t2 - t1) * 1000), result=res
    )
    return res
