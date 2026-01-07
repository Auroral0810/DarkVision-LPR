from sqlalchemy import Column, BigInteger, String, Enum, DateTime, Text, Integer, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class PageType(str, enum.Enum):
    """页面类型枚举"""
    ADMIN = "admin"
    USER = "user"
    WEBSITE = "website"


class PageViewLog(Base):
    """页面访问日志表"""
    __tablename__ = "page_view_logs"
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=True, index=True, comment="登录用户ID，未登录为NULL")
    page_path = Column(String(255), nullable=False, comment="页面路径")
    page_type = Column(
        Enum(PageType, native_enum=False, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        default=PageType.USER,
        comment="页面类型"
    )
    ip_address = Column(String(45), nullable=True, comment="IP地址")
    user_agent = Column(Text, nullable=True, comment="User-Agent")
    referer = Column(String(500), nullable=True, comment="来源页面")
    created_at = Column(DateTime, server_default=func.now(), index=True, comment="创建时间")
    
    # 关系
    user = relationship("User", foreign_keys=[user_id])


class VisitStatistics(Base):
    """访问统计表"""
    __tablename__ = "visit_statistics"
    
    stat_date = Column(Date, primary_key=True, index=True, comment="统计日期")
    page_type = Column(
        Enum(PageType, native_enum=False, values_callable=lambda obj: [e.value for e in obj]),
        primary_key=True,
        nullable=False,
        default=PageType.USER,
        comment="页面类型"
    )
    pv = Column(Integer, default=0, comment="页面浏览量")
    uv = Column(Integer, default=0, comment="独立访客数（基于IP）")
    login_uv = Column(Integer, default=0, comment="登录用户数（基于user_id）")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

