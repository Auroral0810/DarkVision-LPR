from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

from app.models.content import Carousel, Announcement, Document, Faq, FaqCategory

class ClientDownload(Base):
    __tablename__ = 'client_downloads'

    id = Column(Integer, primary_key=True, index=True)
    os = Column(String(20), nullable=False)
    version = Column(String(20), nullable=False)
    download_url = Column(String(255), nullable=False)
    changelog = Column(Text, nullable=True)
    release_date = Column(DateTime, nullable=False)
    is_latest = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)

class SystemConfig(Base):
    __tablename__ = 'system_configs'

    id = Column(Integer, primary_key=True, index=True)
    config_key = Column(String(100), unique=True, nullable=False)
    config_value = Column(Text, nullable=False)
    description = Column(String(255), nullable=True)
    is_public = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

