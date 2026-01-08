from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Carousel(Base):
    __tablename__ = "carousels"

    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    image_url = Column(String(255), nullable=False)
    link_url = Column(String(255), nullable=True)
    sort_order = Column(Integer, default=0)
    is_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)

class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    display_position = Column(Enum('popup','banner','message_center'), nullable=False)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    is_enabled = Column(Boolean, default=True)
    created_by = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    creator = relationship("User", backref="created_announcements")

class Document(Base):
    __tablename__ = "documents"

    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    doc_type = Column(Enum('tech','service_agreement','privacy_policy'), nullable=False)
    content = Column(Text, nullable=False) # longtext in mysql, Text in sqlalchemy is fine
    version = Column(String(20), nullable=False)
    is_current = Column(Boolean, default=False)
    created_by = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    creator = relationship("User", backref="created_documents")

class FaqCategory(Base):
    __tablename__ = "faq_categories"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    sort_order = Column(Integer, default=0)

    faqs = relationship("Faq", back_populates="category")

class Faq(Base):
    __tablename__ = "faqs"

    id = Column(BigInteger, primary_key=True, index=True)
    category_id = Column(BigInteger, ForeignKey("faq_categories.id"), nullable=True)
    question = Column(String(255), nullable=False)
    answer = Column(Text, nullable=False)
    sort_order = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    is_hot = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    category = relationship("FaqCategory", back_populates="faqs")
