from sqlalchemy import Column, BigInteger, String, DateTime, Text, Boolean, Numeric, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class CouponType(str, enum.Enum):
    PERCENTAGE = "percentage"  # 折扣百分比 (e.g., 80 for 20% off)
    FIXED_AMOUNT = "fixed_amount"  # 固定金额减免

class Coupon(Base):
    """优惠券"""
    __tablename__ = "coupons"
    
    id = Column(BigInteger, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True, comment="优惠码")
    type = Column(String(20), nullable=False, default=CouponType.FIXED_AMOUNT, comment="优惠类型")
    value = Column(Numeric(10, 2), nullable=False, comment="优惠值(金额或百分比)")
    min_purchase = Column(Numeric(10, 2), default=0, comment="最低消费金额")
    
    start_time = Column(DateTime, nullable=True, comment="开始时间")
    end_time = Column(DateTime, nullable=True, comment="结束时间")
    
    usage_limit = Column(Integer, default=-1, comment="总使用次数限制(-1无限)")
    used_count = Column(Integer, default=0, comment="已使用次数")
    
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, server_default=func.now())
    
    # 关联使用的订单 - 暂时注释，因为 orders 表缺少 coupon_id
    # orders = relationship("app.models.payment.Order", back_populates="coupon")

class Promotion(Base):
    """限时促销活动"""
    __tablename__ = "promotions"
    
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="活动名称")
    package_id = Column(BigInteger, ForeignKey("packages.id"), nullable=False, comment="关联套餐")
    
    discount_rate = Column(Numeric(5, 2), nullable=False, comment="折扣率")
    
    start_time = Column(DateTime, nullable=False, comment="开始时间")
    end_time = Column(DateTime, nullable=False, comment="结束时间")
    
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, server_default=func.now())
    
    package = relationship("app.models.payment.Package")
