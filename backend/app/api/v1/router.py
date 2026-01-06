from fastapi import APIRouter
from app.api.v1 import auth, captcha, contact, website, recognition, upload, users, websocket

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["认证"])
router.include_router(captcha.router, tags=["验证码"])
router.include_router(contact.router, prefix="/contact", tags=["联系我们"])
router.include_router(website.router, tags=["官网内容"])
router.include_router(recognition.router, prefix="/recognition", tags=["车牌识别"])
router.include_router(websocket.router, prefix="/recognition", tags=["实时通信"]) # Mount under /recognition so URL is /api/v1/recognition/ws/{task_id}
router.include_router(upload.router, prefix="/upload", tags=["文件上传"])
router.include_router(users.router, prefix="/users", tags=["用户"])