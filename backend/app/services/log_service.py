from sqlalchemy.orm import Session
from app.models.system import OperationLog
from typing import Optional, Any
from datetime import datetime
from fastapi import Request
from fastapi.encoders import jsonable_encoder
import json

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
    result: Optional[Any] = None,
    params: Optional[Any] = None,
    request: Optional[Request] = None
):
    """记录操作日志"""
    try:
        # 如果提供了 request，自动提取信息
        final_ip = ip_address
        final_ua = user_agent
        final_method = method
        final_path = path

        if request:
            final_ip = request.client.host if request.client else ip_address
            final_ua = request.headers.get("user-agent") if not user_agent else user_agent
            final_method = request.method if not method else method
            final_path = request.url.path if not path else path

        # 处理序列化
        final_result = result
        if result is not None and not isinstance(result, (str, bytes)):
            try:
                final_result = json.dumps(jsonable_encoder(result), ensure_ascii=False)
            except Exception:
                final_result = str(result)
        
        final_params = params
        if params is not None and not isinstance(params, (str, bytes)):
            try:
                final_params = json.dumps(jsonable_encoder(params), ensure_ascii=False)
            except Exception:
                final_params = str(params)

        log = OperationLog(
            admin_id=admin_id,
            module=module,
            action=action,
            description=description,
            method=final_method,
            path=final_path,
            ip_address=final_ip,
            user_agent=final_ua,
            status=status,
            duration=duration,
            result=final_result,
            params=final_params
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
    end_time: Optional[datetime] = None,
    order_by: str = "created_at",
    order_type: str = "desc"
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
        
    # 动态排序
    if hasattr(OperationLog, order_by):
        col = getattr(OperationLog, order_by)
        if order_type == "asc":
            query = query.order_by(col.asc())
        else:
            query = query.order_by(col.desc())
    else:
        query = query.order_by(OperationLog.created_at.desc())

    total = query.count()
    logs = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return logs, total

def get_system_logs(log_type: str = "app", lines: int = 100):
    """从日志文件读取系统日志"""
    import os
    
    log_dir = "logs"
    filename = "app.log" if log_type == "app" else "error.log"
    file_path = os.path.join(log_dir, filename)
    
    if not os.path.exists(file_path):
        return {
            "content": f"Log file {filename} not found.",
            "filename": filename,
            "total_lines": 0
        }
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # 读取最后 N 行
            all_lines = f.readlines()
            total = len(all_lines)
            last_lines = all_lines[-lines:] if total > lines else all_lines
            content = "".join(last_lines)
            
            return {
                "content": content,
                "filename": filename,
                "total_lines": total
            }
    except Exception as e:
        return {
            "content": f"Error reading log file: {str(e)}",
            "filename": filename,
            "total_lines": 0
        }
