from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.api import deps
from app.services.admin.backup_service import backup_service
from app.schemas.admin.backup import BackupCreate, BackupOut, BackupQuery
from app.core.response import UnifiedResponse, success_response

router = APIRouter()

@router.get("/list", response_model=UnifiedResponse[Any])
def list_backups(
    page: int = 1,
    size: int = 10,
    start_time: str = None,
    end_time: str = None,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_admin)
) -> Any:
    """
    Get list of backups
    """
    query = BackupQuery(page_num=page, page_size=size, start_time=start_time, end_time=end_time)
    records, total = backup_service.get_list(db, query)
    
    # Enrich with user info if needed, already done in schema? No, user relation in model.
    # Schema BackupOut expects creator_name. We need to populate it.
    
    results = []
    for r in records:
        out = BackupOut.model_validate(r)
        if r.creator:
            out.creator_name = r.creator.nickname
        results.append(out)
        
    return success_response(data={"list": results, "total": total})

@router.post("/create", response_model=UnifiedResponse[Any])
def create_backup(
    item: BackupCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_admin)
) -> Any:
    """
    Create a new backup
    """
    record = backup_service.create_backup(db, current_user.id, item.description)
    return success_response(message="Backup created successfully")

@router.post("/{id}/restore", response_model=UnifiedResponse[Any])
def restore_backup(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_admin)
) -> Any:
    """
    Restore from a backup
    """
    if current_user.user_type != "admin":
         raise HTTPException(status_code=403, detail="Only superuser can restore data")
         
    backup_service.restore_backup(db, id)
    return success_response(message="Database restored successfully")

@router.get("/{id}/download")
def download_backup(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_admin)
):
    """
    Download a backup file
    """
    record = backup_service.get_by_id(db, id)
    if not record:
        raise HTTPException(status_code=404, detail="Backup not found")
        
    return FileResponse(record.file_path, filename=record.filename, media_type="application/octet-stream")

@router.delete("/{id}", response_model=UnifiedResponse[Any])
def delete_backup(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_admin)
) -> Any:
    """
    Delete a backup
    """
    if current_user.user_type != "admin":
         raise HTTPException(status_code=403, detail="Permission denied")
         
    backup_service.delete_backup(db, id)
    return success_response(message="Backup deleted successfully")
