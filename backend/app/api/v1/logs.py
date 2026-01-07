from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.core.database import get_db
from app.core.response import success, UnifiedResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.models.statistics import PageViewLog, VisitStatistics, PageType
from app.core.logger import logger
from datetime import date, timedelta
from typing import Optional
from pydantic import BaseModel

router = APIRouter()


class VisitStatsVO(BaseModel):
    """访客统计响应"""
    todayUvCount: int
    totalUvCount: int
    uvGrowthRate: float
    todayPvCount: int
    totalPvCount: int
    pvGrowthRate: float


class VisitTrendVO(BaseModel):
    """访问趋势响应"""
    dates: list[str]
    pvList: list[int]
    uvList: list[int]
    ipList: list[int]


@router.get("/visit-stats", response_model=UnifiedResponse, summary="获取访客统计", tags=["数据统计"])
def get_visit_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取访客统计数据（UV/PV）
    
    返回今日和总体的 UV/PV 数据，以及较昨日的增长率
    """
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    try:
        # Helper to get global stats (sum of all page types) for a range or specific date
        def get_global_stats(target_date):
            return db.query(
                func.sum(VisitStatistics.pv).label('pv'),
                func.sum(VisitStatistics.uv).label('uv')
            ).filter(
                VisitStatistics.stat_date == target_date
            ).first()

        # 今日统计 (实时累加)
        # 访客数(UV): 官网访客(IP) + 用户中心登录数 + 管理中心登录数
        def get_total_uv_for_date(target_date):
            # 获取官网 UV
            website_uv = db.query(VisitStatistics.uv).filter(
                VisitStatistics.stat_date == target_date,
                VisitStatistics.page_type == PageType.WEBSITE
            ).scalar() or 0
            
            # 获取用户中心登录数
            user_login_uv = db.query(VisitStatistics.login_uv).filter(
                VisitStatistics.stat_date == target_date,
                VisitStatistics.page_type == PageType.USER
            ).scalar() or 0
            
            # 获取管理端登录数
            admin_login_uv = db.query(VisitStatistics.login_uv).filter(
                VisitStatistics.stat_date == target_date,
                VisitStatistics.page_type == PageType.ADMIN
            ).scalar() or 0
            
            return website_uv + user_login_uv + admin_login_uv

        today_pv = int(db.query(func.sum(VisitStatistics.pv)).filter(VisitStatistics.stat_date == today).scalar() or 0)
        today_uv = get_total_uv_for_date(today)
        
        # 昨日统计
        yesterday_pv = int(db.query(func.sum(VisitStatistics.pv)).filter(VisitStatistics.stat_date == yesterday).scalar() or 0)
        yesterday_uv = get_total_uv_for_date(yesterday)
        
        # 总统计
        total_pv = int(db.query(func.sum(VisitStatistics.pv)).scalar() or 0)
        # 总 UV 同样是各端累加
        total_uv = (db.query(func.sum(VisitStatistics.uv)).filter(VisitStatistics.page_type == PageType.WEBSITE).scalar() or 0) + \
                   (db.query(func.sum(VisitStatistics.login_uv)).filter(VisitStatistics.page_type != PageType.WEBSITE).scalar() or 0)
        total_uv = int(total_uv)
        
        # 计算增长率
        pv_growth_rate = 0.0
        uv_growth_rate = 0.0
        
        if yesterday_pv > 0:
            pv_growth_rate = round((today_pv - yesterday_pv) / yesterday_pv * 100, 1)
        elif today_pv > 0:
            pv_growth_rate = 100.0
        
        if yesterday_uv > 0:
            uv_growth_rate = round((today_uv - yesterday_uv) / yesterday_uv * 100, 1)
        elif today_uv > 0:
            uv_growth_rate = 100.0
        
        result = VisitStatsVO(
            todayUvCount=today_uv,
            totalUvCount=total_uv,
            uvGrowthRate=uv_growth_rate,
            todayPvCount=today_pv,
            totalPvCount=total_pv,
            pvGrowthRate=pv_growth_rate
        )
        
        return success(data=result.model_dump(), message="获取成功")
        
    except Exception as e:
        logger.error(f"Failed to get visit stats: {e}")
        # 返回默认值
        result = VisitStatsVO(
            todayUvCount=0,
            totalUvCount=0,
            uvGrowthRate=0.0,
            todayPvCount=0,
            totalPvCount=0,
            pvGrowthRate=0.0
        )
        return success(data=result.model_dump(), message="获取成功")


@router.get("/visit-trend", response_model=UnifiedResponse, summary="获取访问趋势", tags=["数据统计"])
def get_visit_trend(
    startDate: str = Query(..., description="开始日期，格式：YYYY-MM-DD"),
    endDate: str = Query(..., description="结束日期，格式：YYYY-MM-DD"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取访问趋势数据
    
    返回指定日期范围内的 PV/UV/IP 趋势数据
    """
    try:
        # 解析日期
        start = date.fromisoformat(startDate)
        end = date.fromisoformat(endDate)
        
        # 查询特定日期范围内的聚合数据
        # 按日期分组，聚合所有页面类型的 PV/UV
        stats_list = db.query(
            VisitStatistics.stat_date,
            func.sum(VisitStatistics.pv).label('pv'),
            func.sum(VisitStatistics.uv).label('uv'),
            func.sum(VisitStatistics.login_uv).label('login_uv')
        ).filter(
            VisitStatistics.stat_date >= start,
            VisitStatistics.stat_date <= end
        ).group_by(VisitStatistics.stat_date).order_by(VisitStatistics.stat_date).all()
        
        # 构建日期范围
        dates = []
        pv_list = []
        uv_list = []
        ip_list = []
        
        current_date = start
        # Convert list of rows to dict for easy lookup
        stats_dict = {stat.stat_date: stat for stat in stats_list}
        
        while current_date <= end:
            dates.append(current_date.strftime("%Y-%m-%d"))
            stat = stats_dict.get(current_date)
            if stat:
                pv_list.append(int(stat.pv or 0))
                uv_list.append(int(stat.uv or 0))
                ip_list.append(int(stat.uv or 0))  # 使用 UV 作为 IP 数（简化处理）
            else:
                # 如果某天没有统计数据，返回 0
                pv_list.append(0)
                uv_list.append(0)
                ip_list.append(0)
            
            current_date += timedelta(days=1)
        
        result = VisitTrendVO(
            dates=dates,
            pvList=pv_list,
            uvList=uv_list,
            ipList=ip_list
        )
        
        return success(data=result.model_dump(), message="获取成功")
        
    except Exception as e:
        logger.error(f"Failed to get visit trend: {e}")
        # 返回空数据
        result = VisitTrendVO(
            dates=[],
            pvList=[],
            uvList=[],
            ipList=[]
        )
        return success(data=result.model_dump(), message="获取成功")

