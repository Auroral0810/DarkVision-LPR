from pydantic import BaseModel
from typing import List, Optional

class KpiData(BaseModel):
    total_count: int
    avg_confidence: float
    error_count: int
    avg_time_ms: int
    
    # Trends for comparison (vs previous period)
    total_count_trend: float
    avg_confidence_trend: float
    error_count_trend: float
    avg_time_trend: float

class TrendItem(BaseModel):
    date: str
    count: int
    success_rate: float

class DistributionItem(BaseModel):
    name: str # Plate type
    value: int

class TopPlateItem(BaseModel):
    plate: str
    count: int
    last_seen: str # e.g. "10 mins ago"

class AnalysisResponse(BaseModel):
    kpi: KpiData
    trend: List[TrendItem]
    distribution: List[DistributionItem]
    top_plates: List[TopPlateItem]
