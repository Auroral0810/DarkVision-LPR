from sqlalchemy import Column, BigInteger, String, DateTime, Text, ForeignKey, Enum, Float
from sqlalchemy.sql import func
from app.core.database import Base


class RecognitionRecord(Base):
    """识别记录表"""
    __tablename__ = "recognition_records"
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")
    image_url = Column(String(255), nullable=False, comment="原图URL")
    plate_number = Column(String(20), nullable=True, comment="识别的车牌号")
    confidence = Column(Float, nullable=True, comment="识别置信度")
    status = Column(Enum("success", "failed", "processing"), nullable=False, default="processing", comment="识别状态")
    error_message = Column(Text, nullable=True, comment="错误信息")
    created_at = Column(DateTime, server_default=func.now(), index=True, comment="创建时间")

