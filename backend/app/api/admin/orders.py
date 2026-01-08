from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.response import UnifiedResponse, success_response, error_response
from app.services.admin.order_service import order_service
from app.schemas.admin.order import OrderOut, OrderCreate

router = APIRouter()

@router.get("/", response_model=UnifiedResponse[List[OrderOut]])
def list_orders(
    skip: int = 0,
    limit: int = 20,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    orders = order_service.get_orders(db, skip, limit, status)
    total = order_service.get_order_count(db, status)
    return success_response(data=orders, message=f"Total: {total}")

@router.post("/manual", response_model=UnifiedResponse)
def create_manual_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    order = order_service.create_manual_order(db, order_data)
    return success_response(data={"id": order.id, "order_no": order.order_no}, message="订单创建成功")

@router.post("/{order_id}/refund", response_model=UnifiedResponse)
def refund_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = order_service.refund_order(db, order_id)
    if not order:
        return error_response(message="订单未找到")
    return success_response(message="订单已申请退款")
