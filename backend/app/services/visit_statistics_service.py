"""
访问统计服务
用于聚合和查询访问统计数据
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from app.models.statistics import PageViewLog, VisitStatistics, PageType
from app.core.logger import logger
from datetime import date, timedelta


def aggregate_daily_statistics(db: Session, target_date: date = None, page_type: PageType = PageType.USER) -> bool:
    """
    聚合指定日期的访问统计数据
    
    Args:
        db: 数据库会话
        target_date: 目标日期，默认为昨天
        page_type: 页面类型
        
    Returns:
        bool: 是否成功
    """
    if target_date is None:
        target_date = date.today() - timedelta(days=1)
    
    try:
        # 查询指定日期的原始日志
        logs = db.query(PageViewLog).filter(
            func.date(PageViewLog.created_at) == target_date,
            PageViewLog.page_type == page_type
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
            VisitStatistics.page_type == page_type
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
                page_type=page_type,
                pv=pv,
                uv=uv,
                login_uv=login_uv
            )
            db.add(stats)
        
        db.commit()
        logger.info(f"Aggregated statistics for {target_date} ({page_type}): PV={pv}, UV={uv}, Login UV={login_uv}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to aggregate daily statistics for {target_date}: {e}")
        db.rollback()
        return False


def record_visit_realtime(db: Session, page_type: PageType, ip_address: str, user_id: int = None) -> bool:
    """
    实时记录访问统计（增量更新）
    
    Args:
        db: 数据库会话
        page_type: 页面类型
        ip_address: IP地址
        user_id: 用户ID
        
    Returns:
        bool: 是否成功
    """
    today = date.today()
    try:
        # 1. 查找或创建今日统计记录
        stats = db.query(VisitStatistics).filter(
            VisitStatistics.stat_date == today,
            VisitStatistics.page_type == page_type
        ).first()
        
        if not stats:
            stats = VisitStatistics(
                stat_date=today,
                page_type=page_type,
                pv=0,
                uv=0,
                login_uv=0
            )
            db.add(stats)
            db.flush()
            
        # 2. 累加 PV
        stats.pv += 1
        
        # 3. 检查是否需要累加 UV (官网使用 IP 统计访客，Portal 使用登录用户统计)
        if page_type == PageType.WEBSITE:
            # 基于 IP 判断访客
            ip_exists = db.query(PageViewLog).filter(
                func.date(PageViewLog.created_at) == today,
                PageViewLog.page_type == page_type,
                PageViewLog.ip_address == ip_address
            ).count()
            
            if ip_exists <= 1:
                stats.uv += 1
        else:
            # USER/ADMIN 门户：UV 定义为“登录用户数”
            if user_id:
                user_exists = db.query(PageViewLog).filter(
                    func.date(PageViewLog.created_at) == today,
                    PageViewLog.page_type == page_type,
                    PageViewLog.user_id == user_id
                ).count()
                
                if user_exists <= 1:
                    stats.uv += 1 # 门户的 UV 即是登录人数
                    stats.login_uv += 1
        
        db.commit()
        return True
    except Exception as e:
        logger.error(f"Failed to record visit realtime: {e}")
        db.rollback()
        return False


def record_page_view_log(
    db: Session, 
    page_type: PageType, 
    ip_address: str, 
    user_id: int = None,
    page_path: str = None,
    user_agent: str = None,
    referrer: str = None
) -> bool:
    """
    记录页面访问日志并更新统计数据
    """
    try:
        # 1. 保存日志
        log = PageViewLog(
            page_type=page_type,
            ip_address=ip_address,
            user_id=user_id,
            page_path=page_path or "/",
            user_agent=user_agent,
            referer=referrer
        )
        db.add(log)
        db.flush() # 获取 ID 和日期信息
        
        # 2. 实时记录统计
        record_visit_realtime(db, page_type, ip_address, user_id)
        
        return True
    except Exception as e:
        logger.error(f"Failed to record page view log: {e}")
        db.rollback()
        return False


def get_today_statistics(db: Session, page_type: PageType = PageType.USER) -> dict:
    """
    获取今日统计数据
    
    Args:
        db: 数据库会话
        page_type: 页面类型
        
    Returns:
        dict: 统计数据
    """
    today = date.today()
    
    stats = db.query(VisitStatistics).filter(
        VisitStatistics.stat_date == today,
        VisitStatistics.page_type == page_type
    ).first()
    
    if stats:
        return {
            "pv": stats.pv,
            "uv": stats.uv,
            "login_uv": stats.login_uv
        }
    
    return {
        "pv": 0,
        "uv": 0,
        "login_uv": 0
    }

