from sqlalchemy import Column, BigInteger, String, DateTime, Text, ForeignKey, Enum, Float, Integer, JSON, DECIMAL, Date, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class RecognitionTask(Base):
    """识别任务主表"""
    __tablename__ = "recognition_tasks"
    
    id = Column(BigInteger, primary_key=True, index=True)
    task_uuid = Column(String(64), unique=True, nullable=False, comment="业务任务UUID")
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, comment="用户ID")
    task_type = Column(Enum('single', 'batch', 'video', 'realtime'), nullable=False, comment="任务类型")
    status = Column(Enum('pending', 'processing', 'completed', 'failed'), default='pending', nullable=False, comment="任务状态")
    progress = Column(DECIMAL(5, 2), default=0.00, comment="进度")
    total_items = Column(Integer, nullable=True, comment="总数量")
    success_count = Column(Integer, default=0, comment="成功数量")
    failed_count = Column(Integer, default=0, comment="失败数量")
    started_at = Column(DateTime, nullable=True, comment="开始时间")
    finished_at = Column(DateTime, nullable=True, comment="结束时间")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    is_deleted = Column(Boolean, default=False, nullable=False, comment="是否软删除")
    
    results = relationship("RecognitionRecord", back_populates="task")


class RecognitionRecord(Base):
    """识别结果表（对应数据库 recognition_results 表）"""
    __tablename__ = "recognition_results"
    
    id = Column(BigInteger, primary_key=True, index=True)
    task_id = Column(BigInteger, ForeignKey("recognition_tasks.id"), nullable=True, comment="关联任务ID")
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")
    original_image_url = Column(String(255), nullable=False, comment="原图URL")
    enhanced_image_url = Column(String(255), nullable=True, comment="增强后图片URL")
    license_plate = Column(String(20), nullable=False, comment="识别的车牌号")
    plate_type = Column(Enum("blue", "yellow", "green", "white", "other"), nullable=True, comment="车牌类型")
    confidence = Column(Float, nullable=False, comment="识别置信度")
    bbox = Column(JSON, nullable=True, comment="车牌坐标 JSON [x,y,w,h]")
    enhance_algorithm = Column(String(50), nullable=True, comment="增强算法")
    model_version = Column(String(20), nullable=True, comment="模型版本")
    processing_time = Column(Float, nullable=True, comment="处理时长(ms)")
    processed_at = Column(DateTime, nullable=False, comment="处理时间")
    created_at = Column(DateTime, server_default=func.now(), index=True, comment="创建时间")
    is_deleted = Column(Boolean, default=False, nullable=False, comment="是否软删除")

    task = relationship("RecognitionTask", back_populates="results")


class RecognitionStatistic(Base):
    """识别统计（限额）"""
    __tablename__ = "recognition_statistics"

    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True, nullable=False)
    sub_user_id = Column(BigInteger, ForeignKey("users.id"), nullable=True, comment="子账户独立统计")
    stat_date = Column(Date, primary_key=True, nullable=False)
    daily_count = Column(Integer, default=0)
    monthly_count = Column(Integer, default=0)
    video_count = Column(Integer, default=0)
    api_count = Column(Integer, default=0)

class RecognitionModel(Base):
    """模型版本"""
    __tablename__ = "recognition_models"
    
    id = Column(BigInteger, primary_key=True, index=True)
    version = Column(String(20), unique=True, nullable=False, comment="版本号")
    name = Column(String(100), nullable=False, comment="模型名称")
    is_active = Column(Boolean, default=False, nullable=False, comment="是否当前线上模型")
    accuracy = Column(DECIMAL(5, 2), nullable=True, comment="识别准确率")
    description = Column(Text, nullable=True, comment="模型描述")
    file_path = Column(String(255), nullable=True, comment="模型权重路径")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
