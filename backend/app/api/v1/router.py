from app.api.v1 import (
    auth, captcha, contact, website, recognition, upload, 
    users, websocket, history, analysis, tracking, logs
)
from app.api.v1.admin import orders, packages, finance

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["认证"])
router.include_router(captcha.router, tags=["验证码"])
router.include_router(contact.router, prefix="/contact", tags=["联系我们"])
router.include_router(website.router, tags=["官网内容"])
router.include_router(recognition.router, prefix="/recognition", tags=["车牌识别"])
router.include_router(websocket.router, tags=["实时通信"]) # URL becomes /api/v1/ws/{task_id} or /api/v1/ws/user/{user_id}
router.include_router(upload.router, prefix="/upload", tags=["文件上传"])
router.include_router(users.router, prefix="/users", tags=["用户"])
router.include_router(history.router, prefix="/history", tags=["识别历史"])
router.include_router(analysis.router, prefix="/analysis", tags=["数据分析"])
router.include_router(tracking.router, prefix="/tracking", tags=["数据统计"])
router.include_router(logs.router, prefix="/logs", tags=["日志"])

# Admin routes
router.include_router(orders.router, prefix="/admin/orders", tags=["管理-订单"])
router.include_router(packages.router, prefix="/admin/packages", tags=["管理-套餐"])
router.include_router(finance.router, prefix="/admin/finance", tags=["管理-财务"])