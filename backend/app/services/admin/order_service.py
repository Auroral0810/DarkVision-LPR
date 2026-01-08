from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from app.models.payment import Order, Package
from app.models.user import User
from app.schemas.admin.order import OrderCreate, OrderUpdate, OrderOut
from datetime import datetime
import uuid

class OrderService:
    def get_orders(self, db: Session, skip: int = 0, limit: int = 20, status: Optional[str] = None) -> List[OrderOut]:
        query = db.query(Order, User.nickname, Package.name.label("package_name")).join(User, Order.user_id == User.id).join(Package, Order.package_id == Package.id)
        if status:
            query = query.filter(Order.status == status)
        
        results = query.order_by(desc(Order.created_at)).offset(skip).limit(limit).all()
        
        orders = []
        for order, nickname, pkg_name in results:
            order_out = OrderOut.model_validate(order)
            order_out.nickname = nickname
            order_out.package_name = pkg_name
            orders.append(order_out)
        return orders

    def get_order_count(self, db: Session, status: Optional[str] = None) -> int:
        query = db.query(func.count(Order.id))
        if status:
            query = query.filter(Order.status == status)
        return query.scalar()

    def create_manual_order(self, db: Session, order_data: OrderCreate) -> Order:
        order_no = f"MANUAL-{uuid.uuid4().hex[:12].upper()}"
        new_order = Order(
            order_no=order_no,
            user_id=order_data.user_id,
            package_id=order_data.package_id,
            amount=order_data.amount,
            status=order_data.status,
            payment_method=order_data.payment_method,
            paid_at=datetime.now() if order_data.status == "paid" else None
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order

    def update_order_status(self, db: Session, order_id: int, status: str) -> Optional[Order]:
        order = db.query(Order).filter(Order.id == order_id).first()
        if order:
            order.status = status
            if status == "paid" and not order.paid_at:
                order.paid_at = datetime.now()
            db.commit()
            db.refresh(order)
        return order

    def refund_order(self, db: Session, order_id: int) -> Optional[Order]:
        return self.update_order_status(db, order_id, "refunded")

order_service = OrderService()
