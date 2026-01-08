from fastapi import APIRouter
from app.api.admin import auth, statistics, users, verification, permission, role, system, content, recognition

admin_router = APIRouter()

admin_router.include_router(auth.router, prefix="", tags=["管理员-认证"])
admin_router.include_router(statistics.router, prefix="/statistics", tags=["管理员-数据统计"])
admin_router.include_router(users.router, prefix="/users", tags=["管理员-用户管理"])
admin_router.include_router(verification.router, prefix="/verifications", tags=["管理员-实名认证"])
admin_router.include_router(recognition.router, prefix="/recognition", tags=["管理员-识别记录"])
admin_router.include_router(system.router, prefix="/system", tags=["管理员-系统设置"])
# admin_router.include_router(finance.router, prefix="/finance", tags=["管理员-财务管理"])
admin_router.include_router(content.router, prefix="/content", tags=["管理员-内容管理"])
admin_router.include_router(permission.router, prefix="/permissions", tags=["管理员-权限管理"])
admin_router.include_router(role.router, prefix="/roles", tags=["管理员-角色管理"])
