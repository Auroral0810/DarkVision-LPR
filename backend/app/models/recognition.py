from sqlalchemy import Column, BigInteger, String, DateTime, Text, ForeignKey, Enum, Float
from sqlalchemy.sql import func
from app.core.database import Base


class RecognitionRecord(Base):
    """识别记录表（对应数据库 recognition_results 表）"""
    __tablename__ = "recognition_results"
    
    id = Column(BigInteger, primary_key=True, index=True)
    task_id = Column(BigInteger, ForeignKey("recognition_tasks.id"), nullable=True, comment="关联任务ID（批量/视频）")
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")
    original_image_url = Column(String(255), nullable=False, comment="原图URL")
    enhanced_image_url = Column(String(255), nullable=True, comment="增强后图片URL")
    license_plate = Column(String(20), nullable=False, comment="识别的车牌号")
    plate_type = Column(Enum("blue", "yellow", "green", "white", "other"), nullable=True, comment="车牌类型")
    confidence = Column(Float, nullable=False, comment="识别置信度")
    bbox = Column(Text, nullable=True, comment="车牌坐标 JSON [x,y,w,h]")
    enhance_algorithm = Column(String(50), nullable=True, comment="增强算法")
    model_version = Column(String(20), nullable=True, comment="模型版本")
    processed_at = Column(DateTime, nullable=False, comment="处理时间")
    created_at = Column(DateTime, server_default=func.now(), index=True, comment="创建时间")

