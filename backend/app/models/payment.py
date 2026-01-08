from sqlalchemy import Column, BigInteger, String, DateTime, Text, Boolean, Numeric, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Package(Base):
    """套餐定义"""
    __tablename__ = "packages"
    
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(50), nullable=False, comment="套餐名称")
    code = Column(String(50), unique=True, nullable=False, comment="套餐标识(free, vip_monthly, etc)")
    price = Column(Numeric(10, 2), nullable=False, default=0.00, comment="价格")
    duration_months = Column(Integer, nullable=True, comment="有效期月数(NULL为无限)")
    description = Column(String(255), nullable=True, comment="简短描述")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, server_default=func.now())
    
    features = relationship("PackageFeature", back_populates="package", cascade="all, delete-orphan")
    memberships = relationship("app.models.user.UserMembership", back_populates="package")

class PackageFeature(Base):
    """套餐功能明细"""
    __tablename__ = "package_features"
    
    id = Column(BigInteger, primary_key=True, index=True)
    package_id = Column(BigInteger, ForeignKey("packages.id"), nullable=False, index=True)
    feature_key = Column(String(50), nullable=False, comment="功能键")
    feature_value = Column(String(255), nullable=False, comment="功能值")
    
    package = relationship("Package", back_populates="features")

class Order(Base):
    """订单"""
    __tablename__ = "orders"
    
    id = Column(BigInteger, primary_key=True, index=True)
    order_no = Column(String(64), unique=True, nullable=False, index=True, comment="订单号")
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    package_id = Column(BigInteger, ForeignKey("packages.id"), nullable=False, index=True)
    
    # 金额相关
    amount = Column(Numeric(10, 2), nullable=False, comment="实付金额")
    original_amount = Column(Numeric(10, 2), nullable=True, comment="原价(优惠前)")
    discount_amount = Column(Numeric(10, 2), default=0, comment="优惠金额")
    
    # 关联优惠券
    coupon_id = Column(BigInteger, ForeignKey("coupons.id"), nullable=True, comment="使用的优惠券ID")
    
    status = Column(String(20), nullable=False, default='pending', comment="状态: pending, paid, cancelled, refunded")
    payment_method = Column(String(20), nullable=True, comment="支付方式: wechat, alipay, bank")
    paid_at = Column(DateTime, nullable=True, comment="支付时间")
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    user = relationship("app.models.user.User")
    package = relationship("Package")
    coupon = relationship("app.models.marketing.Coupon", back_populates="orders")
