from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.response import success_response, UnifiedResponse
from app.api.deps import get_current_active_admin
from app.schemas.admin.maintenance import (
    CacheStats, CacheKeyInfo, CacheClearRequest,
    SystemTaskOut, SystemTaskCreate, SystemTaskUpdate,
    SystemVersionOut, SystemVersionCreate, SystemVersionUpdate
)
from app.services.admin.cache_service import cache_service
from app.services.admin.task_service import task_service
from app.services.admin.version_service import version_service
from app.services import scheduler as scheduler_service

router = APIRouter()

# --- Cache Management ---
@router.get("/cache/stats", summary="获取缓存统计", response_model=UnifiedResponse)
def get_cache_stats(current_admin = Depends(get_current_active_admin)):
    stats = cache_service.get_stats()
    return success_response(data=stats)

@router.get("/cache/keys", summary="搜索缓存键", response_model=UnifiedResponse)
def search_cache_keys(
    pattern: str = Query("*", description="搜索模式"),
    limit: int = Query(100, ge=1, le=500),
    current_admin = Depends(get_current_active_admin)
):
    keys = cache_service.list_keys(pattern, limit)
    return success_response(data=keys)

@router.post("/cache/clear", summary="清理缓存", response_model=UnifiedResponse)
def clear_cache(
    req: CacheClearRequest,
    current_admin = Depends(get_current_active_admin)
):
    count = cache_service.clear_cache(prefix=req.prefix, keys=req.keys)
    return success_response(message=f"成功清理 {count} 个缓存键")

# --- Task Scheduling ---
@router.get("/tasks", summary="任务列表", response_model=UnifiedResponse)
def list_tasks(
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    tasks = task_service.list_tasks(db)
    return success_response(data=[SystemTaskOut.model_validate(t) for t in tasks])

@router.post("/tasks", summary="创建任务", response_model=UnifiedResponse)
def create_task(
    task_in: SystemTaskCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    task = task_service.create_task(db, task_in)
    return success_response(data=SystemTaskOut.model_validate(task))

@router.put("/tasks/{id}", summary="更新任务", response_model=UnifiedResponse)
def update_task(
    id: int,
    task_in: SystemTaskUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    task = task_service.update_task(db, id, task_in)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return success_response(data=SystemTaskOut.model_validate(task))

@router.delete("/tasks/{id}", summary="删除任务", response_model=UnifiedResponse)
def delete_task(
    id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    if not task_service.delete_task(db, id):
        raise HTTPException(status_code=404, detail="任务不存在")
    return success_response(message="删除成功")

@router.post("/tasks/{id}/toggle", summary="启用/禁用任务", response_model=UnifiedResponse)
def toggle_task(
    id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    task = task_service.toggle_task(db, id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return success_response(data=SystemTaskOut.model_validate(task))

@router.post("/tasks/{id}/run", summary="立即执行任务", response_model=UnifiedResponse)
def run_task(
    id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    from app.models.system import SystemTask
    item = db.query(SystemTask).filter(SystemTask.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="任务不存在")
        
    if scheduler_service.run_task_immediately(item.task_code):
        return success_response(message="执行指令已下发")
    else:
        raise HTTPException(status_code=500, detail="任务执行失败或未注册")

# --- Version Update ---
@router.get("/versions", summary="版本列表", response_model=UnifiedResponse)
def list_versions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    versions, total = version_service.list_versions(db, page, page_size, type)
    return success_response(data={
        "list": [SystemVersionOut.model_validate(v) for v in versions],
        "total": total
    })

@router.post("/versions", summary="发布新版本", response_model=UnifiedResponse)
def create_version(
    version_in: SystemVersionCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    version = version_service.create_version(db, version_in)
    return success_response(data=SystemVersionOut.model_validate(version))

@router.put("/versions/{id}", summary="编辑版本", response_model=UnifiedResponse)
def update_version(
    id: int,
    version_in: SystemVersionUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    version = version_service.update_version(db, id, version_in)
    if not version:
        raise HTTPException(status_code=404, detail="版本记录不存在")
    return success_response(data=SystemVersionOut.model_validate(version))

@router.delete("/versions/{id}", summary="删除版本", response_model=UnifiedResponse)
def delete_version(
    id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_active_admin)
):
    if not version_service.delete_version(db, id):
        raise HTTPException(status_code=404, detail="版本记录不存在")
    return success_response(message="删除成功")
