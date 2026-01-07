"""
定时任务调度器
使用 APScheduler 实现定时任务
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.core.database import SessionLocal
from app.services.visit_statistics_service import aggregate_daily_statistics
from app.core.logger import logger
from datetime import date, timedelta

scheduler = BackgroundScheduler()


def aggregate_daily_statistics_job():
    """每日凌晨 1 点聚合昨日访问统计数据"""
    db = SessionLocal()
    try:
        yesterday = date.today() - timedelta(days=1)
        logger.info(f"Starting daily statistics aggregation for {yesterday}")
        aggregate_daily_statistics(db, yesterday)
        logger.info(f"Daily statistics aggregation completed for {yesterday}")
    except Exception as e:
        logger.error(f"Error in daily statistics aggregation job: {e}")
    finally:
        db.close()


def start_scheduler():
    """启动定时任务调度器"""
    try:
        # 每日凌晨 1:00 执行聚合任务
        scheduler.add_job(
            aggregate_daily_statistics_job,
            trigger=CronTrigger(hour=1, minute=0),
            id='aggregate_daily_statistics',
            name='聚合每日访问统计',
            replace_existing=True
        )
        
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

