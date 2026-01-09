from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Tuple, Optional
from app.models.system import SystemVersion
from app.schemas.admin.maintenance import SystemVersionCreate, SystemVersionUpdate

class VersionService:
    @staticmethod
    def list_versions(
        db: Session, 
        page: int = 1, 
        page_size: int = 20,
        version_type: Optional[str] = None
    ) -> Tuple[List[SystemVersion], int]:
        """列表查询版本历史"""
        query = db.query(SystemVersion)
        
        if version_type:
            query = query.filter(SystemVersion.type == version_type)
            
        total = query.count()
        versions = query.order_by(desc(SystemVersion.created_at))\
                        .offset((page - 1) * page_size)\
                        .limit(page_size).all()
                        
        return versions, total

    @staticmethod
    def create_version(db: Session, version_in: SystemVersionCreate) -> SystemVersion:
        """记录新版本更新"""
        version = SystemVersion(**version_in.model_dump())
        db.add(version)
        db.commit()
        db.refresh(version)
        return version

    @staticmethod
    def update_version(db: Session, id: int, version_in: SystemVersionUpdate) -> Optional[SystemVersion]:
        """更新版本记录信息"""
        version = db.query(SystemVersion).filter(SystemVersion.id == id).first()
        if not version:
            return None
            
        update_data = version_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(version, field, value)
            
        db.commit()
        db.refresh(version)
        return version

    @staticmethod
    def delete_version(db: Session, id: int) -> bool:
        """删除版本记录"""
        version = db.query(SystemVersion).filter(SystemVersion.id == id).first()
        if version:
            db.delete(version)
            db.commit()
            return True
        return False

    @staticmethod
    def get_latest_version(db: Session, version_type: str = "system") -> Optional[SystemVersion]:
        """获取最新版本"""
        return db.query(SystemVersion)\
                 .filter(SystemVersion.type == version_type)\
                 .order_by(desc(SystemVersion.created_at)).first()

version_service = VersionService()
