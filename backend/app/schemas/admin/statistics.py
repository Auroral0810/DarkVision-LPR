from pydantic import BaseModel
from datetime import datetime
from typing import List


class DashboardStats(BaseModel):
    """仪表板统计数据"""
    total_users: int
    today_registrations: int
    total_recognitions: int
    today_recognitions: int
    total_revenue: float
    today_revenue: float
    active_users_30d: int
    
    
class UserTrendData(BaseModel):
    """用户趋势数据"""
    date: str
    count: int


class RecognitionTrendData(BaseModel):
    """识别量趋势数据"""
    date: str
    count: int
    success_count: int
    fail_count: int


class UserTypeDistribution(BaseModel):
    """用户类型分布"""
    user_type: str
    count: int
    percentage: float


class PlateTypeDistribution(BaseModel):
    """车牌类型分布"""
    plate_type: str
    count: int
    percentage: float
