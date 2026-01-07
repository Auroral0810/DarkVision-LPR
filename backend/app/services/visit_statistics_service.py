"""
访问统计服务
用于聚合和查询访问统计数据
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from app.models.statistics import PageViewLog, VisitStatistics, PageType
from app.core.logger import logger
from datetime import date, timedelta


def aggregate_daily_statistics(db: Session, target_date: date = None) -> bool:
    """
    聚合指定日期的访问统计数据
    
    Args:
        db: 数据库会话
        target_date: 目标日期，默认为昨天
        
    Returns:
        bool: 是否成功
    """
    if target_date is None:
        target_date = date.today() - timedelta(days=1)
    
    try:
        # 查询指定日期的原始日志
        logs = db.query(PageViewLog).filter(
            func.date(PageViewLog.created_at) == target_date,
            PageViewLog.page_type == PageType.USER
        ).all()
        
        # 计算统计数据
        pv = len(logs)
        
        # UV: 基于 IP 地址去重
        unique_ips = set(log.ip_address for log in logs if log.ip_address)
        uv = len(unique_ips)
        
        # 登录用户数: 基于 user_id 去重
        unique_users = set(log.user_id for log in logs if log.user_id)
        login_uv = len(unique_users)
        
        # 查询或创建统计记录
        stats = db.query(VisitStatistics).filter(
            VisitStatistics.stat_date == target_date,
            VisitStatistics.page_type == PageType.USER
        ).first()
        
        if stats:
            # 更新现有记录
            stats.pv = pv
            stats.uv = uv
            stats.login_uv = login_uv
        else:
            # 创建新记录
            stats = VisitStatistics(
                stat_date=target_date,
                page_type=PageType.USER,
                pv=pv,
                uv=uv,
                login_uv=login_uv
            )
            db.add(stats)
        
        db.commit()
        logger.info(f"Aggregated statistics for {target_date}: PV={pv}, UV={uv}, Login UV={login_uv}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to aggregate daily statistics for {target_date}: {e}")
        db.rollback()
        return False


def aggregate_today_statistics(db: Session) -> bool:
    """
    聚合今日访问统计数据（实时更新）
    
    Args:
        db: 数据库会话
        
    Returns:
        bool: 是否成功
    """
    return aggregate_daily_statistics(db, date.today())


def get_today_statistics(db: Session) -> dict:
    """
    获取今日统计数据
    
    Args:
        db: 数据库会话
        
    Returns:
        dict: 统计数据
    """
    today = date.today()
    
    stats = db.query(VisitStatistics).filter(
        VisitStatistics.stat_date == today,
        VisitStatistics.page_type == PageType.USER
    ).first()
    
    if stats:
        return {
            "pv": stats.pv,
            "uv": stats.uv,
            "login_uv": stats.login_uv
        }
    
    # 如果今日统计数据不存在，从原始日志实时计算
    logs = db.query(PageViewLog).filter(
        func.date(PageViewLog.created_at) == today,
        PageViewLog.page_type == PageType.USER
    ).all()
    
    pv = len(logs)
    unique_ips = set(log.ip_address for log in logs if log.ip_address)
    uv = len(unique_ips)
    unique_users = set(log.user_id for log in logs if log.user_id)
    login_uv = len(unique_users)
    
    return {
        "pv": pv,
        "uv": uv,
        "login_uv": login_uv
    }

