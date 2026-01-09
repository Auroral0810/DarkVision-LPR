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

class SystemTask(Base):
    """系统定时任务表"""
    __tablename__ = "system_tasks"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="任务名称")
    task_code = Column(String(100), unique=True, nullable=False, comment="任务代码/ID")
    cron_expression = Column(String(100), nullable=False, comment="Cron表达式")
    status = Column(Integer, default=1, comment="状态: 0=禁用, 1=启用")
    remark = Column(String(255), nullable=True, comment="备注")
    last_run_at = Column(DateTime, nullable=True, comment="最后运行时间")
    next_run_at = Column(DateTime, nullable=True, comment="下次运行时间")
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class SystemVersion(Base):
    """系统版本历史表"""
    __tablename__ = "system_versions"

    id = Column(BigInteger, primary_key=True, index=True)
    version_number = Column(String(50), nullable=False, comment="版本号")
    title = Column(String(100), nullable=False, comment="标题")
    content = Column(Text, nullable=False, comment="更新内容")
    type = Column(String(20), default="system", comment="类型: system/app/api")
    is_force = Column(Integer, default=0, comment="是否强制更新: 0=否, 1=是")
    download_url = Column(String(255), nullable=True, comment="下载地址")
    
    created_at = Column(DateTime, server_default=func.now())
