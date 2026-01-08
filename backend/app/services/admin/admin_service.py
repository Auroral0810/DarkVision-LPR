from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import json
from datetime import datetime

from app.models.permission import Permission, RolePermission
from app.models.role import Role, AdminRole
from app.models.user import User, UserType
from app.schemas.admin.admin_user import (
    PermissionCreate, PermissionUpdate, PermissionOut,
    RoleCreate, RoleUpdate, RoleOut,
    AdminUserCreate, AdminUserUpdate, AdminUserOut
)
from app.core.redis import redis_client
from app.core.security import get_password_hash

CACHE_KEY_PERMISSIONS = "admin:permissions:tree"
CACHE_KEY_ROLES = "admin:roles:list"
CACHE_KEY_ADMIN_USERS = "admin:users:list"

class AdminService:
    def _clear_cache(self, key: str):
        if redis_client: redis_client.delete(key)
    
    # --- Permissions ---
    def get_permission_tree(self, db: Session) -> List[PermissionOut]:
        cache_key = CACHE_KEY_PERMISSIONS
        if redis_client:
            try:
                cached = redis_client.get(cache_key)
                if cached: return json.loads(cached)
            except Exception: pass
        
        all_perms = db.query(Permission).order_by(Permission.sort_order.asc()).all()
        # Build Tree
        perm_map = {p.id: PermissionOut.model_validate(p) for p in all_perms}
        roots = []
        for p in all_perms:
            p_out = perm_map[p.id]
            p_out.children = [] # Init children
            
        for p in all_perms:
            p_out = perm_map[p.id]
            if p.parent_id:
                parent = perm_map.get(p.parent_id)
                if parent:
                    parent.children.append(p_out)
            else:
                roots.append(p_out)
        
        # Serialize roots (which contain children recursively)
        serialized = [r.model_dump(mode='json') for r in roots]
        
        if redis_client:
            try:
                redis_client.setex(cache_key, 3600, json.dumps(serialized))
            except Exception: pass
            
        return roots

    def create_permission(self, db: Session, data: PermissionCreate) -> Permission:
        item = Permission(**data.model_dump())
        db.add(item)
        db.commit()
        db.refresh(item)
        self._clear_cache(CACHE_KEY_PERMISSIONS)
        return item

    def update_permission(self, db: Session, id: int, data: PermissionUpdate) -> Optional[Permission]:
        item = db.query(Permission).filter(Permission.id == id).first()
        if not item: return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
        self._clear_cache(CACHE_KEY_PERMISSIONS)
        return item

    def delete_permission(self, db: Session, id: int) -> bool:
        item = db.query(Permission).filter(Permission.id == id).first()
        if not item: return False
        db.delete(item)
        db.commit()
        self._clear_cache(CACHE_KEY_PERMISSIONS)
        return True

    # --- Roles ---
    def get_roles(self, db: Session) -> List[Role]:
        cache_key = CACHE_KEY_ROLES
        if redis_client:
             try:
                cached = redis_client.get(cache_key)
                if cached: 
                    # For roles, we usually need permission_ids too.
                    # This simple caching might need to ensure RoleOut serialization includes them.
                    return json.loads(cached)
             except Exception: pass

        roles = db.query(Role).all()
        
        if redis_client and roles:
            try:
                # Custom serialization to include permission_ids
                serialized = []
                for r in roles:
                    r_out = RoleOut.model_validate(r)
                    # Manually populate permission_ids if not auto-fetched
                    # SQLAlchemy relationship 'role_permissions'
                    r_out.permission_ids = [rp.permission_id for rp in r.role_permissions]
                    serialized.append(r_out.model_dump(mode='json'))
                
                redis_client.setex(cache_key, 3600, json.dumps(serialized))
            except Exception: pass
            
        return roles

    def create_role(self, db: Session, data: RoleCreate) -> Role:
        role = Role(
            name=data.name,
            description=data.description,
            is_system=data.is_system
        )
        db.add(role)
        db.commit()
        db.flush() # get ID
        
        for pid in data.permission_ids:
            rp = RolePermission(role_id=role.id, permission_id=pid)
            db.add(rp)
        
        db.commit()
        db.refresh(role)
        self._clear_cache(CACHE_KEY_ROLES)
        return role

    def update_role(self, db: Session, id: int, data: RoleUpdate) -> Optional[Role]:
        role = db.query(Role).filter(Role.id == id).first()
        if not role: return None
        
        if data.name: role.name = data.name
        if data.description: role.description = data.description
        
        if data.permission_ids is not None:
            # Update permissions
            db.query(RolePermission).filter(RolePermission.role_id == id).delete()
            for pid in data.permission_ids:
                rp = RolePermission(role_id=id, permission_id=pid)
                db.add(rp)
        
        db.commit()
        db.refresh(role)
        self._clear_cache(CACHE_KEY_ROLES)
        return role

    def delete_role(self, db: Session, id: int) -> bool:
        role = db.query(Role).filter(Role.id == id).first()
        if not role: return False
        if role.is_system: return False # Prevent system role deletion
        
        db.delete(role)
        db.commit()
        self._clear_cache(CACHE_KEY_ROLES)
        return True

    # --- Admin Users ---
    def get_admin_users(self, db: Session) -> List[User]:
        # Filter users with type 'admin'
        users = db.query(User).filter(User.user_type == UserType.ADMIN).all()
        return users

    def create_admin_user(self, db: Session, data: AdminUserCreate) -> User:
        # Check nickname/phone
        if db.query(User).filter(User.nickname == data.nickname).first():
            raise ValueError("昵称已存在")
        if db.query(User).filter(User.phone == data.phone).first():
            raise ValueError("手机号已存在")
            
        user = User(
            nickname=data.nickname,
            phone=data.phone,
            password_hash=get_password_hash(data.password),
            user_type=UserType.ADMIN,
            status="active"
        )
        db.add(user)
        db.flush()
        
        # Add profile roughly if needed, for real_name
        from app.models.user import UserProfile
        profile = UserProfile(user_id=user.id, real_name=data.real_name)
        db.add(profile)
        
        # Add roles
        for rid in data.role_ids:
            ar = AdminRole(admin_user_id=user.id, role_id=rid)
            db.add(ar)
            
        db.commit()
        db.refresh(user)
        return user

    def update_admin_user(self, db: Session, id: int, data: AdminUserUpdate) -> Optional[User]:
        user = db.query(User).filter(User.id == id, User.user_type == UserType.ADMIN).first()
        if not user: return None
        
        if data.nickname: user.nickname = data.nickname
        if data.phone: user.phone = data.phone
        if data.email: user.email = data.email
        if data.password: user.password_hash = get_password_hash(data.password)
        if data.is_active is not None:
             user.status = "active" if data.is_active else "inactive"
             
        if data.role_ids is not None:
            db.query(AdminRole).filter(AdminRole.admin_user_id == id).delete()
            for rid in data.role_ids:
                ar = AdminRole(admin_user_id=id, role_id=rid)
                db.add(ar)
                
        db.commit()
        db.refresh(user)
        return user

admin_service = AdminService()
