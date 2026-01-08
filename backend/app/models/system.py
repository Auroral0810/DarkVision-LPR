from sqlalchemy import Column, BigInteger, String, DateTime, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class OperationLog(Base):
    """操作日志表"""
    __tablename__ = "operation_logs"

    id = Column(BigInteger, primary_key=True, index=True)
    admin_id = Column(BigInteger, ForeignKey("users.id"), nullable=True, comment="操作人ID")
    module = Column(String(50), nullable=False, comment="功能模块")
    action = Column(String(50), nullable=False, comment="操作类型")
    description = Column(String(255), nullable=True, comment="详细描述")
    method = Column(String(10), nullable=True, comment="请求方法")
    path = Column(String(255), nullable=True, comment="请求路径")
    params = Column(Text, nullable=True, comment="请求参数")
    result = Column(Text, nullable=True, comment="响应结果")
    status = Column(Integer, default=200, comment="响应状态码")
    ip_address = Column(String(45), nullable=True, comment="IP地址")
    user_agent = Column(String(255), nullable=True, comment="User Agent")
    duration = Column(Integer, nullable=True, comment="耗时(ms)")
    
    created_at = Column(DateTime, server_default=func.now())

    # 关系
    admin = relationship("User", foreign_keys=[admin_id])

class SystemIpRule(Base):
    """系统IP规则表(黑白名单)"""
    __tablename__ = "system_ip_rules"

    id = Column(BigInteger, primary_key=True, index=True)
    ip_address = Column(String(45), unique=True, nullable=False, comment="IP地址")
    type = Column(String(10), nullable=False, default="deny", comment="规则类型: allow/deny")
    remark = Column(String(255), nullable=True, comment="备注")
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
