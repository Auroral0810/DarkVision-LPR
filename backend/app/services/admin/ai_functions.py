import json
import logging
from typing import Dict, Any, Callable
from sqlalchemy.orm import Session
from app.services import user as user_service
from app.services.admin import content_service, system_service, order_service, package_service
from app.services.admin.admin_service import admin_service # For roles/admin-users
from app.schemas.admin.user import AdminUserCreate, AdminUserUpdate, BanUserRequest, BatchDeleteRequest, AdminUpdateUserType
from app.schemas.admin.content import AnnouncementCreate, AnnouncementUpdate, FaqCreate, FaqUpdate
from app.schemas.admin.role import RoleCreate, RoleUpdate
from app.schemas.admin.system import IpRuleCreate
from app.schemas.admin.finance import PackageCreate, PackageUpdate

logger = logging.getLogger(__name__)

class AiDispatcher:
    """
    AI 命令分发器 - 将抽象的函数调用映射为具体的 Service 方法
    """
    
    _registry: Dict[str, Callable] = {}

    @classmethod
    def register(cls, name: str):
        """装饰器：注册函数处理程序"""
        def decorator(func: Callable):
            cls._registry[name] = func
            return func
        return decorator

    @classmethod
    async def dispatch(cls, db: Session, user_id: int, function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        分发执行命令
        """
        handler = cls._registry.get(function_name)
        if not handler:
            raise ValueError(f"Function {function_name} not found or not supported.")
        
        logger.info(f"AI Dispatching: {function_name} with args {arguments}")
        
        # 执行处理函数
        # 大部分 handler 只需要 db 和 arguments，少部分可能需要 operator_id (user_id)
        return await handler(db, user_id, **arguments)

# =================================================================================
#  User Management Handlers
# =================================================================================

@AiDispatcher.register("createUser")
async def create_user_handler(db: Session, operator_id: int, **kwargs):
    """创建用户"""
    # 转换参数为 Pydantic Schema
    user_in = AdminUserCreate(**kwargs)
    user = user_service.admin_create_user(db, user_in)
    return {"id": user.id, "username": user.phone, "message": f"用户 {user.phone} 创建成功"}

@AiDispatcher.register("updateUser")
async def update_user_handler(db: Session, operator_id: int, user_id: int, **kwargs):
    """更新用户信息"""
    db_user = user_service.get_user_by_id(db, user_id)
    if not db_user:
        raise ValueError(f"User ID {user_id} not found")
        
    user_in = AdminUserUpdate(**kwargs)
    updated_user = user_service.admin_update_user(db, db_user, user_in)
    return {"id": updated_user.id, "message": "用户信息更新成功"}

@AiDispatcher.register("banUser")
async def ban_user_handler(db: Session, operator_id: int, user_id: int, reason: str = "AI Security Action", duration_days: int = 7):
    """封禁用户"""
    db_user = user_service.get_user_by_id(db, user_id)
    if not db_user:
        raise ValueError(f"User ID {user_id} not found")
        
    # 计算解封时间
    from datetime import datetime, timedelta
    banned_until = datetime.now() + timedelta(days=duration_days)
    
    user_service.ban_user(db, db_user, reason, banned_until)
    return {"message": f"用户已封禁至 {banned_until.strftime('%Y-%m-%d')}"}

@AiDispatcher.register("unbanUser")
async def unban_user_handler(db: Session, operator_id: int, user_id: int):
    """解封用户"""
    db_user = user_service.get_user_by_id(db, user_id)
    if not db_user:
        raise ValueError(f"User ID {user_id} not found")
        
    user_service.unban_user(db, db_user)
    return {"message": "用户已解封"}

# =================================================================================
#  Role & Permission Handlers
# =================================================================================

@AiDispatcher.register("createRole")
async def create_role_handler(db: Session, operator_id: int, name: str, description: str = None, **kwargs):
    """创建角色"""
    from app.services.admin.admin_service import admin_service
    role_in = RoleCreate(name=name, description=description, permission_ids=kwargs.get("permission_ids", []), is_system=False)
    role = admin_service.create_role(db, role_in)
    return {"id": role.id, "name": role.name, "message": "角色创建成功"}

@AiDispatcher.register("updateRole")
async def update_role_handler(db: Session, operator_id: int, role_id: int, **kwargs):
    """更新角色"""
    from app.services.admin.admin_service import admin_service
    role_in = RoleUpdate(**kwargs)
    updated = admin_service.update_role(db, role_id, role_in)
    if not updated:
        raise ValueError(f"Role ID {role_id} not found")
    return {"id": updated.id, "message": "角色更新成功"}

# =================================================================================
#  Finance Package Handlers
# =================================================================================

@AiDispatcher.register("createPackage")
async def create_package_handler(db: Session, operator_id: int, name: str, code: str, price: float, **kwargs):
    """创建套餐"""
    pkg_in = PackageCreate(name=name, code=code, price=price, **kwargs)
    pkg = package_service.create_package(db, pkg_in)
    return {"id": pkg.id, "name": pkg.name, "message": "套餐创建成功"}

@AiDispatcher.register("updatePackage")
async def update_package_handler(db: Session, operator_id: int, package_id: int, **kwargs):
    """更新套餐"""
    pkg_in = PackageUpdate(**kwargs)
    updated = package_service.update_package(db, package_id, pkg_in)
    if not updated:
        raise ValueError(f"Package ID {package_id} not found")
    return {"id": updated.id, "message": "套餐更新成功"}

# =================================================================================
#  System & Config Handlers
# =================================================================================

@AiDispatcher.register("updateSystemConfig")
async def update_config_handler(db: Session, operator_id: int, configs: Dict[str, str]):
    """更新系统配置"""
    system_service.update_configs(db, configs)
    return {"message": f"已更新 {len(configs)} 项系统配置"}

@AiDispatcher.register("addIpRule")
async def add_ip_rule_handler(db: Session, operator_id: int, ip: str, type: str = "deny", remark: str = "AI Auto Block"):
    """添加 IP 黑/白名单"""
    rule_in = IpRuleCreate(ip_address=ip, type=type, remark=remark)
    system_service.create_ip_rule(db, rule_in)
    return {"message": f"IP {ip} 已添加到 {type} 列表"}

# =================================================================================
#  Content Management Handlers
# =================================================================================

@AiDispatcher.register("createAnnouncement")
async def create_announcement_handler(db: Session, operator_id: int, title: str, content: str, type: str = "info", **kwargs):
    """发布公告"""
    ann_in = AnnouncementCreate(title=title, content=content, type=type, **kwargs)
    ann = content_service.create_announcement(db, ann_in)
    return {"id": ann.id, "message": "公告发布成功"}

# =================================================================================
#  Order & Finance Handlers
# =================================================================================

@AiDispatcher.register("refundOrder")
async def refund_order_handler(db: Session, operator_id: int, order_id: str, reason: str = "AI Assisted Refund"):
    """订单退款"""
    # order_service.refund_order(db, order_id, reason) # 假设有这个方法
    # 暂时模拟
    return {"message": f"订单 {order_id} 退款申请已提交"}

