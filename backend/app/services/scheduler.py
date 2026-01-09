"""
定时任务调度器
使用 APScheduler 实现定时任务
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.core.database import SessionLocal
from app.services.visit_statistics_service import aggregate_daily_statistics
from app.core.logger import logger
from datetime import date, timedelta, datetime
from typing import Dict, Any, Callable
import os

scheduler = BackgroundScheduler()

# 任务函数映射表
# 所有的定时任务需要在这里注册才能通过管理后台控制
JOB_FUNCTIONS: Dict[str, Callable] = {}

def register_job(code: str):
    """装饰器：注册任务函数"""
    def decorator(f):
        JOB_FUNCTIONS[code] = f
        return f
    return decorator

@register_job("aggregate_daily_statistics")
def aggregate_daily_statistics_job():
    """每日凌晨 1 点聚合昨日访问统计数据"""
    db = SessionLocal()
    try:
        from app.models.statistics import PageType
        yesterday = date.today() - timedelta(days=1)
        logger.info(f"Starting daily statistics aggregation for {yesterday}")
        
        # 聚合所有类型的统计数据
        for p_type in PageType:
             aggregate_daily_statistics(db, yesterday, p_type)
             
        logger.info(f"Daily statistics aggregation completed for {yesterday}")
        
        # 更新任务最后运行时间
        _update_task_run_info("aggregate_daily_statistics")
    except Exception as e:
        logger.error(f"Error in daily statistics aggregation job: {e}")
    finally:
        db.close()

def _update_task_run_info(task_code: str):
    """更新任务的执行元数据"""
    db = SessionLocal()
    try:
        from app.models.system import SystemTask
        task = db.query(SystemTask).filter(SystemTask.task_code == task_code).first()
        if task:
            task.last_run_at = datetime.now()
            # 获取下次执行时间
            job = scheduler.get_job(task_code)
            if job:
                task.next_run_at = job.next_run_time
            db.commit()
    except Exception as e:
        logger.error(f"Failed to update task run info for {task_code}: {e}")
    finally:
        db.close()

def sync_tasks_from_db():
    """从数据库同步任务到调度器"""
    db = SessionLocal()
    try:
        from app.models.system import SystemTask
        # 初始化默认任务到数据库 (如果不存在)
        default_tasks = [
            {
                "name": "聚合每日访问统计",
                "task_code": "aggregate_daily_statistics",
                "cron_expression": "0 1 * * *",
                "remark": "统计每日 PV/UV 数据"
            }
        ]
        
        for dt in default_tasks:
            exists = db.query(SystemTask).filter(SystemTask.task_code == dt["task_code"]).first()
            if not exists:
                db.add(SystemTask(**dt))
        db.commit()

        # 读取所有启用的任务
        tasks = db.query(SystemTask).filter(SystemTask.status == 1).all()
        
        # 清除现有任务 (可选，或者按需更新)
        # scheduler.remove_all_jobs()
        
        for task in tasks:
            if task.task_code in JOB_FUNCTIONS:
                try:
                    scheduler.add_job(
                        JOB_FUNCTIONS[task.task_code],
                        trigger=CronTrigger.from_crontab(task.cron_expression),
                        id=task.task_code,
                        name=task.name,
                        replace_existing=True
                    )
                    # 同步下次运行时间到数据库
                    job = scheduler.get_job(task.task_code)
                    if job:
                        task.next_run_at = job.next_run_time
                except Exception as e:
                    logger.error(f"Failed to add job {task.task_code}: {e}")
        db.commit()
    except Exception as e:
        logger.error(f"Failed to sync tasks from DB: {e}")
    finally:
        db.close()

def start_scheduler():
    """启动定时任务调度器"""
    try:
        # 1. 先同步任务
        sync_tasks_from_db()
        
        # 2. 启动调度器
        if not scheduler.running:
            scheduler.start()
        logger.info("Scheduler started successfully")
    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}")

def stop_scheduler():
    """停止定时任务调度器"""
    try:
        scheduler.shutdown()
        logger.info("Scheduler stopped")
    except Exception as e:
        logger.error(f"Error stopping scheduler: {e}")

def run_task_immediately(task_code: str):
    """立即执行一个任务"""
    if task_code in JOB_FUNCTIONS:
        # 通过线程或者直接调用执行
        # APScheduler 可以触发立即执行
        try:
            scheduler.trigger_job(task_code)
            return True
        except:
            # 如果任务还没在调度器里，直接运行函数
            JOB_FUNCTIONS[task_code]()
            return True
    return False

def toggle_task(task_code: str, enable: bool):
    """开启或关闭任务"""
    if enable:
        sync_tasks_from_db() # 重新同步即可
    else:
        try:
            scheduler.remove_job(task_code)
        except:
            pass
    return True

