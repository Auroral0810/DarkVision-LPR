from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class BackupRecord(Base):
    __tablename__ = "backup_records"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    filename = Column(String(255), nullable=False, comment="备份文件名")
    file_path = Column(String(255), nullable=False, comment="文件存储路径")
    file_size = Column(BigInteger, default=0, comment="文件大小(bytes)")
    created_by = Column(BigInteger, ForeignKey("users.id"), nullable=True, comment="操作人ID")
    created_at = Column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    status = Column(String(20), default="success", comment="状态: success/failed")
    description = Column(String(255), nullable=True, comment="备注")
    is_deleted = Column(Boolean, default=False, comment="是否逻辑删除")
    
    # Relationships
    creator = relationship("User", foreign_keys=[created_by])
