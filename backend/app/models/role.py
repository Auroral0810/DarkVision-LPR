from sqlalchemy import Column, BigInteger, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Role(Base):
    """角色表"""
    __tablename__ = "roles"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, comment="角色名称(唯一标识)")
    description = Column(String(255), nullable=True, comment="角色描述")
    is_system = Column(Boolean, default=False, comment="是否系统内置")
    created_at = Column(DateTime, server_default=func.now())
    # created_at = Column(DateTime, server_default=func.now())
    # updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now()) # Removed as column does not exist in DB

    # 关系
    # permissions = relationship("RolePermission", back_populates="role")
    admins = relationship("AdminRole", back_populates="role")
    role_permissions = relationship("RolePermission", back_populates="role", cascade="all, delete-orphan")
    permissions = relationship("Permission", secondary="role_permissions", viewonly=True, overlaps="role_permissions,roles")

class AdminRole(Base):
    """管理员-角色关联表"""
    __tablename__ = "admin_roles"

    admin_user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id = Column(BigInteger, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)

    # 关系
    user = relationship("User", back_populates="admin_roles")
    role = relationship("Role", back_populates="admins")
