from sqlalchemy import Column, BigInteger, String, DateTime, Text, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from app.core.database import Base

class Permission(Base):
    """权限表"""
    __tablename__ = "permissions"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(50), nullable=False, comment="权限名称")
    code = Column(String(50), unique=True, nullable=False, comment="权限标识(如 user:list)")
    description = Column(String(255), nullable=True, comment="描述")
    type = Column(String(20), default="menu", comment="类型: menu/button/api")
    parent_id = Column(BigInteger, ForeignKey("permissions.id"), nullable=True, comment="父权限ID")
    path = Column(String(255), nullable=True, comment="前端路由路径")
    component = Column(String(255), nullable=True, comment="前端组件路径")
    icon = Column(String(50), nullable=True, comment="图标")
    sort_order = Column(Integer, default=0, comment="排序")
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # 关系
    parent = relationship("Permission", remote_side=[id], backref=backref("children", order_by=sort_order))
    roles = relationship("RolePermission", back_populates="permission")


class RolePermission(Base):
    """角色-权限关联表"""
    __tablename__ = "role_permissions"

    role_id = Column(BigInteger, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    permission_id = Column(BigInteger, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)

    # 关系
    role = relationship("Role", back_populates="role_permissions")
    permission = relationship("Permission", back_populates="roles")
