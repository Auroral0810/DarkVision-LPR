from sqlalchemy.orm import Session, joinedload
from app.models.role import Role
from app.models.permission import RolePermission, Permission
from app.schemas.admin.role import RoleCreate, RoleUpdate
from typing import List, Optional, Tuple

def get_role_by_id(db: Session, role_id: int) -> Optional[Role]:
    role = db.query(Role).options(joinedload(Role.permissions)).filter(Role.id == role_id).first()
    if role:
        role.permission_ids = [p.id for p in role.permissions]
    return role

def get_role_by_name(db: Session, name: str) -> Optional[Role]:
    return db.query(Role).filter(Role.name == name).first()

def list_roles(db: Session, skip: int = 0, limit: int = 100) -> Tuple[List[Role], int]:
    total = db.query(Role).count()
    roles = db.query(Role).options(joinedload(Role.permissions)).order_by(Role.created_at.desc()).offset(skip).limit(limit).all()
    
    # Handle permission_ids population for Pydantic
    for role in roles:
        role.permission_ids = [p.id for p in role.permissions]
        
    return roles, total

def get_all_roles(db: Session) -> List[Role]:
    return db.query(Role).all()

def create_role(db: Session, role_in: RoleCreate) -> Role:
    db_role = Role(
        name=role_in.name,
        description=role_in.description
    )
    db.add(db_role)
    db.flush() # Get ID

    if role_in.permission_ids:
        for pid in role_in.permission_ids:
            rp = RolePermission(role_id=db_role.id, permission_id=pid)
            db.add(rp)
    
    db.commit()
    # db.refresh(db_role)
    return get_role_by_id(db, db_role.id)

def update_role(db: Session, role_id: int, role_in: RoleUpdate) -> Optional[Role]:
    db_role = get_role_by_id(db, role_id)
    if not db_role:
        return None
    
    if role_in.name is not None:
        db_role.name = role_in.name
    if role_in.description is not None:
        db_role.description = role_in.description
    
    if role_in.permission_ids is not None:
        # Clear existing
        db.query(RolePermission).filter(RolePermission.role_id == role_id).delete()
        # Add new
        for pid in role_in.permission_ids:
            rp = RolePermission(role_id=role_id, permission_id=pid)
            db.add(rp)
            
    db.commit()
    # db.refresh(db_role)
    return get_role_by_id(db, role_id)

def delete_role(db: Session, role_id: int) -> bool:
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        return False
    # Cascade delete should handle role_permissions if configured, but explicit is safer or reliant on schema
    db.delete(db_role)
    db.commit()
    return True
