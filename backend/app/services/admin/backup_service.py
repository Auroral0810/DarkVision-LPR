import os
import subprocess
import logging
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.config import settings
from app.models.backup import BackupRecord
from app.schemas.admin.backup import BackupCreate, BackupQuery
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class BackupService:
    BACKUP_DIR = os.path.join(os.getcwd(), "backups")

    def __init__(self):
        if not os.path.exists(self.BACKUP_DIR):
            os.makedirs(self.BACKUP_DIR)

    def get_list(self, db: Session, query: BackupQuery):
        q = db.query(BackupRecord).filter(BackupRecord.is_deleted == False)
        
        if query.start_time:
            q = q.filter(BackupRecord.created_at >= query.start_time)
        if query.end_time:
            if len(query.end_time) == 10:
                 query.end_time += " 23:59:59"
            q = q.filter(BackupRecord.created_at <= query.end_time)
            
        total = q.count()
        records = q.order_by(desc(BackupRecord.created_at))\
            .offset((query.page_num - 1) * query.page_size)\
            .limit(query.page_size)\
            .all()
            
        return records, total

    def get_by_id(self, db: Session, id: int) -> Optional[BackupRecord]:
        return db.query(BackupRecord).get(id)

    def create_backup(self, db: Session, creator_id: int, description: str = None) -> BackupRecord:
        filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
        filepath = os.path.join(self.BACKUP_DIR, filename)
        
        # Prepare command
        # mysqldump -h host -P port -u user -p password db > file
        # Using env for password to avoid command line leak
        env = os.environ.copy()
        env['MYSQL_PWD'] = settings.MYSQL_PASSWORD
        
        cmd = [
            "mysqldump",
            "-h", settings.MYSQL_HOST,
            "-P", str(settings.MYSQL_PORT),
            "-u", settings.MYSQL_USER,
            settings.MYSQL_DATABASE
        ]
        
        try:
            with open(filepath, 'w') as f:
                process = subprocess.run(cmd, env=env, stdout=f, stderr=subprocess.PIPE, text=True)
                
            if process.returncode != 0:
                logger.error(f"Backup failed: {process.stderr}")
                raise Exception(f"mysqldump failed: {process.stderr}")
                
            # Get file size
            file_size = os.path.getsize(filepath)
            
            record = BackupRecord(
                filename=filename,
                file_path=filepath,
                file_size=file_size,
                created_by=creator_id,
                description=description,
                status="success"
            )
            db.add(record)
            db.commit()
            db.refresh(record)
            return record
            
        except Exception as e:
            logger.error(f"Backup error: {str(e)}")
            # Record failed attempt if desired, or just raise
            raise HTTPException(status_code=500, detail=str(e))

    def restore_backup(self, db: Session, backup_id: int):
        record = db.query(BackupRecord).get(backup_id)
        if not record or not os.path.exists(record.file_path):
            raise HTTPException(status_code=404, detail="Backup file not found")
            
        env = os.environ.copy()
        env['MYSQL_PWD'] = settings.MYSQL_PASSWORD
        
        # mysql -h host -P port -u user db < file
        cmd = [
            "mysql",
            "-h", settings.MYSQL_HOST,
            "-P", str(settings.MYSQL_PORT),
            "-u", settings.MYSQL_USER,
            settings.MYSQL_DATABASE
        ]
        
        try:
            with open(record.file_path, 'r') as f:
                process = subprocess.run(cmd, env=env, stdin=f, stderr=subprocess.PIPE, text=True)
                
            if process.returncode != 0:
                raise Exception(f"mysql restore failed: {process.stderr}")
                
            return {"message": "Restore successful"}
            
        except Exception as e:
            logger.error(f"Restore error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Restore failed: {str(e)}")

    def delete_backup(self, db: Session, backup_id: int):
        record = db.query(BackupRecord).get(backup_id)
        if not record:
             raise HTTPException(status_code=404, detail="Record not found")
             
        # Remove file
        if os.path.exists(record.file_path):
            try:
                os.remove(record.file_path)
            except OSError as e:
                logger.warning(f"Failed to remove file {record.file_path}: {e}")
        
        db.delete(record)
        db.commit()

backup_service = BackupService()
