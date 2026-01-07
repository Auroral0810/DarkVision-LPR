from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.core.cache import init_redis
from app.core.database import engine, Base
# 导入模型以确保注册到Base
import app.models  # noqa
from app.api.v1 import router as api_router
from app.api.admin import admin_router
from app.middleware.error_handler import register_exception_handlers
from app.services.scheduler import start_scheduler

# 创建数据库表（包括新添加的 page_view_logs 和 visit_statistics）
Base.metadata.create_all(bind=engine)

# 初始化Redis
init_redis()

# 启动定时任务调度器
start_scheduler()

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

# 挂载静态文件目录
import os
if not os.path.exists(settings.UPLOAD_DIR):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return {"message": "DarkVision-LPR API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}