from sqlalchemy.orm import Session
from app.models.payment import Package

class PaymentService:
    def get_public_packages(self, db: Session):
        """获取公开的套餐列表"""
        return db.query(Package).filter(Package.is_active == True).all()

payment_service = PaymentService()
