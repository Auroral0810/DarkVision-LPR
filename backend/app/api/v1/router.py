from fastapi import APIRouter
from app.api.v1 import auth, captcha

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["认证"])
router.include_router(captcha.router, tags=["验证码"])