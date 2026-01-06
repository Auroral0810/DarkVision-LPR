from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.analysis import AnalysisResponse
from app.services.analysis import AnalysisService
from app.models.user import User

router = APIRouter()

@router.get("/dashboard", response_model=AnalysisResponse)
def get_analysis_dashboard(
    time_range: str = Query('week', enum=['week', 'month', 'year']),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    获取数据分析看板数据
    """
    service = AnalysisService(db)
    return service.get_dashboard_data(current_user.id, time_range)
