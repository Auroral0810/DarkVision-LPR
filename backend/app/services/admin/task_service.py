from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from app.models.system import SystemTask
from app.schemas.admin.maintenance import SystemTaskCreate, SystemTaskUpdate
from app.services import scheduler as scheduler_service

class TaskService:
    @staticmethod
    def list_tasks(db: Session) -> List[SystemTask]:
        """获取所有定时任务"""
        return db.query(SystemTask).all()

    @staticmethod
    def create_task(db: Session, task_in: SystemTaskCreate) -> SystemTask:
        """创建定时任务"""
        task = SystemTask(**task_in.model_dump())
        db.add(task)
        db.commit()
        db.refresh(task)
        
        # 如果是启用状态，同步到调度器
        if task.status == 1:
            scheduler_service.sync_tasks_from_db()
            
        return task

    @staticmethod
    def update_task(db: Session, id: int, task_in: SystemTaskUpdate) -> Optional[SystemTask]:
        """更新定时任务"""
        task = db.query(SystemTask).filter(SystemTask.id == id).first()
        if not task:
            return None
            
        update_data = task_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
            
        db.commit()
        db.refresh(task)
        
        # 同步调度器状态
        if "status" in update_data or "cron_expression" in update_data:
            scheduler_service.toggle_task(task.task_code, task.status == 1)
            
        return task

    @staticmethod
    def delete_task(db: Session, id: int) -> bool:
        """删除定时任务"""
        task = db.query(SystemTask).filter(SystemTask.id == id).first()
        if task:
            # 先从调度器移除
            scheduler_service.toggle_task(task.task_code, False)
            db.delete(task)
            db.commit()
            return True
        return False

    @staticmethod
    def toggle_task(db: Session, id: int) -> Optional[SystemTask]:
        """切换任务状态"""
        task = db.query(SystemTask).filter(SystemTask.id == id).first()
        if not task:
            return None
            
        task.status = 1 if task.status == 0 else 0
        db.commit()
        db.refresh(task)
        
        scheduler_service.toggle_task(task.task_code, task.status == 1)
        return task

task_service = TaskService()
