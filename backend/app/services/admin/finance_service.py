from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from typing import List, Dict, Any
from app.models.payment import Order, Package
from app.schemas.admin.finance import FinanceReportOut, FinanceKpis, RevenueStat, PackageRevenue
from datetime import datetime, date, timedelta
from decimal import Decimal

class FinanceService:
    def get_finance_report(self, db: Session) -> FinanceReportOut:
        today = date.today()
        month_start = today.replace(day=1)
        
        # KPIs
        today_revenue = db.query(func.sum(Order.amount)).filter(
            Order.status == "paid",
            func.date(Order.paid_at) == today
        ).scalar() or Decimal("0.00")
        
        month_revenue = db.query(func.sum(Order.amount)).filter(
            Order.status == "paid",
            Order.paid_at >= month_start
        ).scalar() or Decimal("0.00")
        
        pending_orders = db.query(func.count(Order.id)).filter(Order.status == "pending").scalar()
        refund_pending = db.query(func.count(Order.id)).filter(Order.status == "refund_pending").scalar() # Assuming status exists or similar
        
        # Revenue Trend (Daily for last 30 days)
        last_30_days = today - timedelta(days=30)
        daily_stats = db.query(
            cast(Order.paid_at, Date).label("date"),
            func.sum(Order.amount).label("amount")
        ).filter(
            Order.status == "paid",
            Order.paid_at >= last_30_days
        ).group_by(cast(Order.paid_at, Date)).order_by(cast(Order.paid_at, Date)).all()
        
        revenue_trend = []
        for d, amt in daily_stats:
            revenue_trend.append(RevenueStat(date=d, amount=amt))
            
        # Package Distribution
        pkg_stats = db.query(
            Package.name,
            func.sum(Order.amount).label("revenue"),
            func.count(Order.id).label("count")
        ).join(Order, Package.id == Order.package_id).filter(
            Order.status == "paid"
        ).group_by(Package.name).all()
        
        package_dist = [PackageRevenue(package_name=name, revenue=rev, order_count=cnt) for name, rev, cnt in pkg_stats]
        
        # Payment Method Distribution
        pm_stats = db.query(
            Order.payment_method,
            func.sum(Order.amount).label("revenue")
        ).filter(
            Order.status == "paid"
        ).group_by(Order.payment_method).all()
        
        pm_dist = {str(pm): rev for pm, rev in pm_stats if pm}
        
        return FinanceReportOut(
            kpis=FinanceKpis(
                today_revenue=today_revenue,
                month_revenue=month_revenue,
                pending_orders=pending_orders,
                refund_pending=refund_pending if refund_pending is not None else 0,
                revenue_trend=0.0 # Placeholder logic for trend percentage
            ),
            daily_revenue=revenue_trend,
            package_distribution=package_dist,
            payment_method_distribution=pm_dist
        )

finance_service = FinanceService()
