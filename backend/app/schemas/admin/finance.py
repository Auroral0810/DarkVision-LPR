from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any
from decimal import Decimal
from datetime import date

class RevenueStat(BaseModel):
    date: date
    amount: Decimal

class FinanceKpis(BaseModel):
    today_revenue: Decimal
    month_revenue: Decimal
    pending_orders: int
    refund_pending: int
    revenue_trend: float # Percentage change

class PackageRevenue(BaseModel):
    package_name: str
    revenue: Decimal
    order_count: int

class FinanceReportOut(BaseModel):
    kpis: FinanceKpis
    daily_revenue: List[RevenueStat]
    package_distribution: List[PackageRevenue]
    payment_method_distribution: Dict[str, Decimal]

    model_config = ConfigDict(from_attributes=True)
