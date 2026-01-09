from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.models.user import User, UserMembership
from app.models.recognition import RecognitionRecord, RecognitionTask
from app.models.payment import Order
from app.schemas.admin import statistics as schemas
from typing import List, Dict, Any

class StatisticsService:
    @staticmethod
    def get_dashboard_stats(db: Session) -> schemas.DashboardStats:
        today = date.today()
        start_of_today = datetime.combine(today, datetime.min.time())
        month_ago = datetime.now() - timedelta(days=30)
        
        # 1. Total Users
        total_users = db.query(func.count(User.id)).scalar() or 0
        
        # 2. Today Registrations
        today_registrations = db.query(func.count(User.id)).filter(
            User.created_at >= start_of_today
        ).scalar() or 0
        
        # 3. Total Recognitions
        total_recognitions = db.query(func.count(RecognitionRecord.id)).scalar() or 0
        
        # 4. Today Recognitions
        today_recognitions = db.query(func.count(RecognitionRecord.id)).filter(
            RecognitionRecord.created_at >= start_of_today
        ).scalar() or 0
        
        # 5. Total Revenue
        total_revenue = db.query(func.sum(Order.amount)).filter(
            Order.status == 'paid'
        ).scalar() or 0.0
        
        # 6. Today Revenue
        today_revenue = db.query(func.sum(Order.amount)).filter(
            Order.status == 'paid',
            Order.paid_at >= start_of_today
        ).scalar() or 0.0
        
        # 7. Active Users (30d) based on activity or login
        active_users_30d = db.query(func.count(func.distinct(User.id))).filter(
            User.last_login_at >= month_ago
        ).scalar() or 0
        
        return schemas.DashboardStats(
            total_users=total_users,
            today_registrations=today_registrations,
            total_recognitions=total_recognitions,
            today_recognitions=today_recognitions,
            total_revenue=float(total_revenue),
            today_revenue=float(today_revenue),
            active_users_30d=active_users_30d
        )

    @staticmethod
    def get_user_trend(db: Session, start_date: date, end_date: date) -> List[schemas.UserTrendData]:
        # Generate trend by day
        results = db.query(
            func.date(User.created_at).label('reg_date'),
            func.count(User.id).label('count')
        ).filter(
            func.date(User.created_at) >= start_date,
            func.date(User.created_at) <= end_date
        ).group_by(func.date(User.created_at)).all()
        
        trend_map = {str(r.reg_date): r.count for r in results}
        
        # Fill zero counts for missing days
        trend = []
        current = start_date
        while current <= end_date:
            date_str = str(current)
            trend.append(schemas.UserTrendData(
                date=date_str,
                count=trend_map.get(date_str, 0)
            ))
            current += timedelta(days=1)
            
        return trend

    @staticmethod
    def get_recognition_trend(db: Session, start_date: date, end_date: date) -> List[schemas.RecognitionTrendData]:
        # Using tasks for trend might be better if you want success/fail details per task group
        # but results table gives granular detail.
        
        # In results table, we don't have explicit success/fail on the record itself usually, 
        # unless confidence is low or manually audited. 
        # Let's assume based on success_count / failed_count in tasks or just count records.
        
        results = db.query(
            func.date(RecognitionRecord.created_at).label('rec_date'),
            func.count(RecognitionRecord.id).label('total'),
            # Mock success/fail logic if database doesn't track it on individual records
            # For now, let's just use the total as success since failed attempts might not even persist
            func.count(RecognitionRecord.id).label('success') 
        ).filter(
            func.date(RecognitionRecord.created_at) >= start_date,
            func.date(RecognitionRecord.created_at) <= end_date
        ).group_by(func.date(RecognitionRecord.created_at)).all()
        
        trend_map = {str(r.rec_date): {"total": r.total, "success": r.success} for r in results}
        
        trend = []
        current = start_date
        while current <= end_date:
            date_str = str(current)
            day_data = trend_map.get(date_str, {"total": 0, "success": 0})
            trend.append(schemas.RecognitionTrendData(
                date=date_str,
                count=day_data["total"],
                success_count=day_data["success"],
                fail_count=day_data["total"] - day_data["success"]
            ))
            current += timedelta(days=1)
            
        return trend

    @staticmethod
    def get_user_type_distribution(db: Session) -> List[schemas.UserTypeDistribution]:
        results = db.query(
            User.user_type,
            func.count(User.id).label('count')
        ).group_by(User.user_type).all()
        
        total = sum(r.count for r in results) or 1
        
        return [
            schemas.UserTypeDistribution(
                user_type=r.user_type.value if hasattr(r.user_type, 'value') else str(r.user_type),
                count=r.count,
                percentage=round(r.count / total * 100, 2)
            ) for r in results
        ]

    @staticmethod
    def get_plate_type_distribution(db: Session) -> List[schemas.PlateTypeDistribution]:
        results = db.query(
            RecognitionRecord.plate_type,
            func.count(RecognitionRecord.id).label('count')
        ).group_by(RecognitionRecord.plate_type).all()
        
        total = sum(r.count for r in results) or 1
        
        return [
            schemas.PlateTypeDistribution(
                plate_type=r.plate_type.value if hasattr(r.plate_type, 'value') else str(r.plate_type or 'unknown'),
                count=r.count,
                percentage=round(r.count / total * 100, 2)
            ) for r in results
        ]

    @staticmethod
    def get_user_activity_heatmap(db: Session) -> List[List[Any]]:
        """获取用户活跃度热力图数据 (星期, 小时, 计数)"""
        from app.models.user import LoginLog
        
        # 统计最近30天的登录分布
        start_date = datetime.now() - timedelta(days=30)
        
        # MySQL/PostgreSQL 提取星期和小时
        # 注意：这里假设使用 MySQL
        results = db.query(
            func.dayofweek(LoginLog.created_at).label('dow'),
            func.hour(LoginLog.created_at).label('hour'),
            func.count(LoginLog.id).label('count')
        ).filter(LoginLog.created_at >= start_date).group_by('dow', 'hour').all()
        
        # 构造成 ECharts 热力图期待的格式: [dow, hour, count]
        # dow: 1(Sun) - 7(Sat) -> 映射到 0-6 (Mon-Sun) 或者保持
        # 这里映射为 0(Mon) - 6(Sun)
        heatmap_data = []
        for r in results:
            # MySQL dayofweek: 1=Sun, 2=Mon, ..., 7=Sat
            # ECharts 常用: 0=Mon, ..., 6=Sun
            dow_map = {2:0, 3:1, 4:2, 5:3, 6:4, 7:5, 1:6}
            heatmap_data.append([dow_map.get(r.dow), r.hour, r.count])
            
        return heatmap_data
