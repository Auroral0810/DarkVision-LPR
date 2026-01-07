from sqlalchemy.orm import Session
from app.models.permission import Permission
from app.schemas.admin.permission import PermissionCreate, PermissionUpdate
from typing import List, Optional

def get_all_permissions(db: Session) -> List[Permission]:
    """获取所有权限（扁平列表），按sort_order排序"""
    return db.query(Permission).order_by(Permission.sort_order).all()

def get_permission_tree(db: Session) -> List[dict]:
    """获取权限树"""
    perms = get_all_permissions(db)
    # 简单的树构建逻辑
    perm_map = {p.id: p for p in perms}
    tree = []
    for p in perms:
        if p.parent_id is None:
            tree.append(p)
        # SQLAlchemy relationship 'children' handles the rest if properly joined/loaded, 
        # but since we fetched all, we rely on lazy loading or eager loading?
        # Actually, for a simple implementation, getting root nodes is enough if we trust the 'children' relationship.
        # However, to be recursive, we might need a serializer.
    return tree

def create_permission(db: Session, perm_in: PermissionCreate) -> Permission:
    db_perm = Permission(
        name=perm_in.name,
        code=perm_in.code,
        description=perm_in.description,
        type=perm_in.type,
        parent_id=perm_in.parent_id,
        path=perm_in.path,
        component=perm_in.component,
        icon=perm_in.icon,
        sort_order=perm_in.sort_order
    )
    db.add(db_perm)
    db.commit()
    db.refresh(db_perm)
    return db_perm

def update_permission(db: Session, perm_id: int, perm_in: PermissionUpdate) -> Optional[Permission]:
    db_perm = db.query(Permission).filter(Permission.id == perm_id).first()
    if not db_perm:
        return None
    
    update_data = perm_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_perm, field, value)
    
    db.commit()
    db.refresh(db_perm)
    return db_perm

def delete_permission(db: Session, perm_id: int) -> bool:
    db_perm = db.query(Permission).filter(Permission.id == perm_id).first()
    if not db_perm:
        return False
    
    db.delete(db_perm)
    db.commit()
    return True
