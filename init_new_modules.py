import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.permission import Permission

def init_permissions(db: Session):
    # 1. System Management (Check existence)
    sys_perm = db.query(Permission).filter(Permission.code == 'system').first()
    if not sys_perm:
        print("Creating 'system' permission...")
        sys_perm = Permission(
            name='系统管理', code='system', type='menu', path='/system', 
            component='Layout', icon='setting', sort_order=1
        )
        db.add(sys_perm)
        db.commit()
        db.refresh(sys_perm)
    
    # 2. Admin Users (under System)
    if sys_perm:
        admin_perm = db.query(Permission).filter(Permission.code == 'system:admin:list').first()
        if not admin_perm:
            print("Creating 'system:admin:list' permission...")
            admin_perm = Permission(
                name='管理员管理', code='system:admin:list', type='menu', 
                parent_id=sys_perm.id, path='admin-users', 
                component='system/admin-user/index', icon='user-filled', sort_order=10
            )
            db.add(admin_perm)
            db.commit()

    # 3. Content Management
    content_perm = db.query(Permission).filter(Permission.code == 'content').first()
    if not content_perm:
        print("Creating 'content' permission...")
        content_perm = Permission(
            name='内容管理', code='content', type='menu', path='/content', 
            component='Layout', icon='document', sort_order=2
        )
        db.add(content_perm)
        db.commit()
        db.refresh(content_perm)

    if content_perm:
        # Announcements
        if not db.query(Permission).filter(Permission.code == 'content:announcement:list').first():
            print("Creating 'content:announcement:list' permission...")
            db.add(Permission(
                name='公告管理', code='content:announcement:list', type='menu',
                parent_id=content_perm.id, path='announcements',
                component='content/AnnouncementMgmt', icon='bell', sort_order=1
            ))
        
        # Carousels
        if not db.query(Permission).filter(Permission.code == 'content:carousel:list').first():
            print("Creating 'content:carousel:list' permission...")
            db.add(Permission(
                name='轮播图管理', code='content:carousel:list', type='menu',
                parent_id=content_perm.id, path='carousels',
                component='content/CarouselMgmt', icon='picture', sort_order=2
            ))
            
        # Documents
        if not db.query(Permission).filter(Permission.code == 'content:document:list').first():
            print("Creating 'content:document:list' permission...")
            db.add(Permission(
                name='文档管理', code='content:document:list', type='menu',
                parent_id=content_perm.id, path='documents',
                component='content/DocumentMgmt', icon='reading', sort_order=3
            ))
            
        # FAQs
        if not db.query(Permission).filter(Permission.code == 'content:faq:list').first():
            print("Creating 'content:faq:list' permission...")
            db.add(Permission(
                name='FAQ管理', code='content:faq:list', type='menu',
                parent_id=content_perm.id, path='faqs',
                component='content/FaqMgmt', icon='question-filled', sort_order=4
            ))
        
        db.commit()

    # 4. System Settings
    setting_perm = db.query(Permission).filter(Permission.code == 'setting').first()
    if not setting_perm:
        print("Creating 'setting' permission...")
        setting_perm = Permission(
            name='系统配置', code='setting', type='menu', path='/setting',
            component='Layout', icon='setting', sort_order=8
        )
        db.add(setting_perm)
        db.commit()
        db.refresh(setting_perm)

    if setting_perm:
        sub_modules = [
            ('基础配置', 'setting:base', 'base', 'setting', 1),
            ('识别参数', 'setting:params', 'params', 'operation', 2),
            ('限额配置', 'setting:quota', 'quotas', 'histogram', 3),
            ('邮件 & 短信', 'setting:notice', 'email-sms', 'postcard', 4),
        ]
        for name, code, path, icon, sort in sub_modules:
            if not db.query(Permission).filter(Permission.code == code).first():
                print(f"Creating '{code}' permission...")
                db.add(Permission(
                    name=name, code=code, type='menu',
                    parent_id=setting_perm.id, path=path,
                    component='config/SystemConfig', icon=icon, sort_order=sort
                ))
        db.commit()

    print("Permissions initialized successfully.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        init_permissions(db)
    finally:
        db.close()
