from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.response import UnifiedResponse, success_response
from app.services.admin.finance_service import finance_service
from app.schemas.admin.finance import FinanceReportOut

router = APIRouter()

@router.get("/report", response_model=UnifiedResponse[FinanceReportOut])
def get_finance_report(db: Session = Depends(get_db)):
    report = finance_service.get_finance_report(db)
    return success_response(data=report)
