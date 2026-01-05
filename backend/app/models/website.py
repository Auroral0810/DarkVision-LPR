from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Carousel(Base):
    __tablename__ = 'carousels'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    image_url = Column(String(255), nullable=False)
    link_url = Column(String(255), nullable=True)
    sort_order = Column(Integer, default=0)
    is_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

class Announcement(Base):
    __tablename__ = 'announcements'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    display_position = Column(String(50), nullable=False) # Enum in DB, String here is fine
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    is_enabled = Column(Boolean, default=True)
    created_by = Column(Integer, nullable=False) # ForeignKey to users.id
    created_at = Column(DateTime, default=datetime.now)

class FaqCategory(Base):
    __tablename__ = 'faq_categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    sort_order = Column(Integer, default=0)
    
    faqs = relationship("Faq", back_populates="category")

class Faq(Base):
    __tablename__ = 'faqs'

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey('faq_categories.id'), nullable=True)
    question = Column(String(255), nullable=False)
    answer = Column(Text, nullable=False)
    sort_order = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    is_hot = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)

    category = relationship("FaqCategory", back_populates="faqs")

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    doc_type = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    version = Column(String(20), nullable=False)
    is_current = Column(Boolean, default=False)
    created_by = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

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

