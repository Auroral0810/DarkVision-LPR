from sqlalchemy.orm import Session
from app.models.system import OperationLog
from typing import Optional
from datetime import datetime

def create_log(
    db: Session,
    admin_id: Optional[int],
    module: str,
    action: str,
    description: Optional[str] = None,
    method: Optional[str] = None,
    path: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    status: int = 200,
    duration: Optional[int] = None,
    result: Optional[str] = None,
    params: Optional[str] = None
):
    """记录操作日志"""
    try:
        log = OperationLog(
            admin_id=admin_id,
            module=module,
            action=action,
            description=description,
            method=method,
            path=path,
            ip_address=ip_address,
            user_agent=user_agent,
            status=status,
            duration=duration,
            result=result,
            params=params
        )
        db.add(log)
        db.commit()
    except Exception as e:
        print(f"Failed to write log: {e}") 
        # Log failure shouldn't stop the main flow, usually.

def list_logs(
    db: Session,
    page: int = 1, 
    page_size: int = 20, 
    module: Optional[str] = None, 
    admin_id: Optional[int] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
):
    query = db.query(OperationLog)
    
    if module:
        query = query.filter(OperationLog.module == module)
    if admin_id:
        query = query.filter(OperationLog.admin_id == admin_id)
    if start_time:
        query = query.filter(OperationLog.created_at >= start_time)
    if end_time:
        query = query.filter(OperationLog.created_at <= end_time)
        
    total = query.count()
    logs = query.order_by(OperationLog.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return logs, total
