from sqlalchemy.orm import Session
from sqlalchemy import func, case, desc, and_
from app.models.recognition import RecognitionRecord, RecognitionTask
from app.schemas.analysis import AnalysisResponse, KpiData, TrendItem, DistributionItem, TopPlateItem
from datetime import datetime, timedelta
import math

class AnalysisService:
    def __init__(self, db: Session):
        self.db = db

    def get_dashboard_data(self, user_id: int, time_range: str = 'week') -> AnalysisResponse:
        now = datetime.now()
        
        # Calculate start date based on range
        if time_range == 'week':
            start_date = now - timedelta(days=6) # Last 7 days including today
            prev_start_date = start_date - timedelta(days=7)
            group_fmt = "%Y-%m-%d"
            days_count = 7
        elif time_range == 'month':
            start_date = now - timedelta(days=29)
            prev_start_date = start_date - timedelta(days=30)
            group_fmt = "%Y-%m-%d"
            days_count = 30
        elif time_range == 'year':
            start_date = now - timedelta(days=364) 
            prev_start_date = start_date - timedelta(days=365)
            # For year, we might group by month in a real app, but let's stick to days or simplify
            # Given the chart needs dates, user might prefer weekly/monthly aggregation for 'year' view
            # For simplicity, let's treat year view same or assume simpler date labeling
            # A full year daily chart is too crowded. Let's stick to days logic for now.
            group_fmt = "%Y-%m-%d"
            days_count = 365
        else:
            start_date = now - timedelta(days=6)
            prev_start_date = start_date - timedelta(days=7)
            group_fmt = "%Y-%m-%d"
            days_count = 7

        # Base query for current period
        base_query = self.db.query(RecognitionRecord).filter(
            RecognitionRecord.user_id == user_id,
            RecognitionRecord.is_deleted == False,
            RecognitionRecord.created_at >= start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        )
        
        # Base query for previous period (for trend calculation)
        prev_query = self.db.query(RecognitionRecord).filter(
            RecognitionRecord.user_id == user_id,
            RecognitionRecord.is_deleted == False,
            RecognitionRecord.created_at < start_date.replace(hour=0, minute=0, second=0, microsecond=0),
            RecognitionRecord.created_at >= prev_start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        )

        # 1. KPIs
        def get_kpi_stats(query):
            total = query.count()
            if total == 0:
                return 0, 0, 0, 0
            
            avg_conf = query.with_entities(func.avg(RecognitionRecord.confidence)).scalar() or 0
            # Assuming 'other' type or low confidence implies 'anomaly/error' effectively? 
            # Or better: failed tasks. But RecognitionRecord only stores successful/completed inferences mostly?
            # Actually RecognitionTask has status 'failed'. 
            # Let's count low confidence (<0.8) as "anomaly" for now.
            error_cnt = query.filter(RecognitionRecord.confidence < 0.8).count()
            
            # Calculate real average processing time using the new column
            avg_time = query.with_entities(func.avg(RecognitionRecord.processing_time)).scalar() or 0
            avg_time = int(avg_time) # Convert to int ms
            
            return total, avg_conf, error_cnt, avg_time

        curr_total, curr_conf, curr_err, curr_time = get_kpi_stats(base_query)
        prev_total, prev_conf, prev_err, prev_time = get_kpi_stats(prev_query)

        def calc_trend(curr, prev):
            if prev == 0:
                return 100.0 if curr > 0 else 0.0
            return ((curr - prev) / prev) * 100

        kpi_data = KpiData(
            total_count=curr_total,
            avg_confidence=round(curr_conf * 100, 1), # Store as percentage 0-100
            error_count=curr_err,
            avg_time_ms=curr_time,
            total_count_trend=round(calc_trend(curr_total, prev_total), 1),
            avg_confidence_trend=round(calc_trend(curr_conf, prev_conf), 1),
            error_count_trend=round(calc_trend(curr_err, prev_err), 1),
            avg_time_trend=0.0
        )

        # 2. Trend Chart (Daily)
        # Group by date
        trend_query = base_query.with_entities(
            func.date(RecognitionRecord.created_at).label('date'),
            func.count(RecognitionRecord.id).label('count'),
            func.avg(RecognitionRecord.confidence).label('avg_conf')
        ).group_by(func.date(RecognitionRecord.created_at)).all()

        # Fill missing dates
        date_map = {item.date: item for item in trend_query}
        trend_items = []
        for i in range(days_count if days_count <= 30 else 30): # Cap chart points if year
             # If year, we really should group by month visually, but logic here:
             # Just show last N days for trend chart usually.
             target_date = (start_date + timedelta(days=i)).date()
             # Adjust logic: We want [today-N, ..., today]
             # Simplify: Just show aggregated data for the period properly sorted.
             pass

        # Re-do specific daily range generation
        # Logic: generate list of dates from start_date to now
        trend_list = []
        delta_days = (now.date() - start_date.date()).days + 1
        for i in range(delta_days):
            d = start_date.date() + timedelta(days=i)
            item = date_map.get(d)
            if item:
                count = item.count
                avg_c = (item.avg_conf or 0) * 100
            else:
                count = 0
                avg_c = 0
            trend_list.append(TrendItem(
                date=d.strftime("%m-%d"),
                count=count,
                success_rate=round(avg_c, 1)
            ))

        # 3. Distribution
        dist_query = base_query.with_entities(
            RecognitionRecord.plate_type,
            func.count(RecognitionRecord.id)
        ).group_by(RecognitionRecord.plate_type).all()
        
        type_map = {
            'blue': '蓝牌', 'green': '绿牌', 'yellow': '黄牌', 'white': '白牌', 'other': '其他'
        }
        distribution = [
            DistributionItem(name=type_map.get(row[0], '其他'), value=row[1]) 
            for row in dist_query if row[0]
        ]
        if not distribution: # Mock if empty to show something? Or return empty.
             pass # Frontend handles empty

        # 4. Top Plates
        top_query = base_query.with_entities(
            RecognitionRecord.license_plate,
            func.count(RecognitionRecord.id).label('cnt'),
            func.max(RecognitionRecord.created_at).label('last_seen')
        ).group_by(RecognitionRecord.license_plate)\
         .order_by(desc('cnt'))\
         .limit(5).all()
         
        def format_time_diff(dt):
            diff = now - dt
            if diff.days > 0: return f"{diff.days}天前"
            if diff.seconds > 3600: return f"{diff.seconds // 3600}小时前"
            if diff.seconds > 60: return f"{diff.seconds // 60}分钟前"
            return "刚刚"

        top_plates = [
            TopPlateItem(
                plate=row[0],
                count=row[1],
                last_seen=format_time_diff(row[2])
            ) for row in top_query
        ]

        return AnalysisResponse(
            kpi=kpi_data,
            trend=trend_list,
            distribution=distribution,
            top_plates=top_plates
        )
