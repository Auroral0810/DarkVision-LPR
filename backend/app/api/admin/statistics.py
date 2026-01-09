from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.response import success, UnifiedResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.online_user_service import get_online_user_count
from app.services.admin.statistics_service import StatisticsService
from datetime import datetime, date, timedelta
from typing import List, Optional
from app.schemas.admin import statistics as schemas

router = APIRouter()

@router.get("/dashboard", response_model=UnifiedResponse, summary="获取仪表板核心统计", tags=["管理员-数据统计"])
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取仪表板核心 KPI 指标"""
    stats = StatisticsService.get_dashboard_stats(db)
    return success(data=stats)

@router.get("/user-trend", response_model=UnifiedResponse, summary="获取用户增长趋势", tags=["管理员-数据统计"])
def get_user_trend(
    start_date: Optional[date] = Query(None, description="开始日期 (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="结束日期 (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取指定日期范围内的用户注册趋势"""
    if not end_date:
        end_date = date.today()
    if not start_date:
        start_date = end_date - timedelta(days=7)
    
    trend = StatisticsService.get_user_trend(db, start_date, end_date)
    return success(data=trend)

@router.get("/recognition-trend", response_model=UnifiedResponse, summary="获取识别量趋势", tags=["管理员-数据统计"])
def get_recognition_trend(
    start_date: Optional[date] = Query(None, description="开始日期 (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="结束日期 (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取指定日期范围内的识别趋势数据"""
    if not end_date:
        end_date = date.today()
    if not start_date:
        start_date = end_date - timedelta(days=7)
    
    trend = StatisticsService.get_recognition_trend(db, start_date, end_date)
    return success(data=trend)

@router.get("/user-distribution", response_model=UnifiedResponse, summary="获取用户类型分布", tags=["管理员-数据统计"])
def get_user_distribution(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取不同类型用户的分布统计"""
    dist = StatisticsService.get_user_type_distribution(db)
    return success(data=dist)

@router.get("/plate-distribution", response_model=UnifiedResponse, summary="获取车牌类型分布统计", tags=["管理员-数据统计"])
def get_plate_distribution(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取识别出的车牌类型分布情况"""
    dist = StatisticsService.get_plate_type_distribution(db)
    return success(data=dist)

@router.get("/activity-heatmap", response_model=UnifiedResponse, summary="获取用户活跃度热力图", tags=["管理员-数据统计"])
def get_user_activity_heatmap(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户在不同时间段的活跃度分布（星期 vs 小时）"""
    data = StatisticsService.get_user_activity_heatmap(db)
    return success(data=data)

@router.get("/online-users", response_model=UnifiedResponse, summary="获取在线用户数", tags=["管理员-数据统计"])
def get_online_users(
    current_user: User = Depends(get_current_user),
):
    """
    获取当前在线用户数（实时）
    
    返回当前登录了用户系统（user-portal）的在线用户数量
    """
    count = get_online_user_count()
    
    return success(
        data={
            "count": count,
            "timestamp": int(datetime.now().timestamp())
        },
        message="获取成功"
    )

