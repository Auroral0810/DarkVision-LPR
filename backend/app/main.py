from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.core.cache import init_redis
from app.core.database import engine, Base
from app.api.v1 import router as api_router
from app.api.admin import admin_router
from app.middleware.error_handler import register_exception_handlers

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 初始化Redis
init_redis()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# 注册全局异常处理器
register_exception_handlers(app)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix=settings.API_V1_PREFIX)
app.include_router(admin_router, prefix="/api/admin")

@app.get("/")
def root():
    return {"message": "DarkVision-LPR API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}