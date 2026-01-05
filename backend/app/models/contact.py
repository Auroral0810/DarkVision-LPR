from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from app.core.database import Base

class ContactMessage(Base):
    """联系/咨询消息表"""
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="姓名")
    email = Column(String(100), nullable=False, comment="邮箱")
    message = Column(Text, nullable=False, comment="咨询内容")
    status = Column(Enum('pending', 'processed', 'ignored'), default='pending', nullable=False, comment="处理状态")
    ip_address = Column(String(45), nullable=True, comment="IP地址")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    processed_at = Column(DateTime, nullable=True, comment="处理时间")
    processed_by = Column(Integer, nullable=True, comment="处理人ID")

