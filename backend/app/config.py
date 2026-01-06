from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    # 项目基础配置
    PROJECT_NAME: str = "DarkVision-LPR"
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "Lucky_ff0810"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天
    
    # 数据库配置
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "123456"
    MYSQL_DATABASE: str = "darkvision_lpr"
    
    # Redis配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # 官网
        "http://localhost:3001",  # 用户端
        "http://localhost:3002",  # 管理端
        "http://localhost:5173"   # Vite开发服务器
    ]
    
    # 邮件配置
    MAIL_HOST: str = "smtp.163.com"
    MAIL_PORT: int = 465
    MAIL_USERNAME: str = "15968588744@163.com"
    MAIL_PASSWORD: str = "QSwPWYUaYmh32ggs"
    MAIL_FROM: str = "15968588744@163.com"
    MAIL_FROM_NAME: str = "DarkVision-LPR"
    MAIL_USE_TLS: bool = False
    MAIL_USE_SSL: bool = True
    
    # 短信配置（腾讯云）
    SMS_SECRET_ID: Optional[str] = None
    SMS_SECRET_KEY: Optional[str] = None
    SMS_SDK_APP_ID: Optional[str] = None
    SMS_SIGN_NAME: Optional[str] = None
    SMS_TEMPLATE_ID: Optional[str] = None
    
    # OSS配置（阿里云）
    OSS_ENDPOINT: Optional[str] = None
    OSS_ACCESS_KEY_ID: Optional[str] = None
    OSS_ACCESS_KEY_SECRET: Optional[str] = None
    OSS_BUCKET_NAME: Optional[str] = None
    
    # LPR模型配置
    YOLO_MODEL_PATH: str = "weights/best.pt"
    LPRNET_MODEL_PATH: str = "weights/Final_LPRNet_model.pth"
    UPLOAD_DIR: str = "static/uploads"

    # 开发模式
    DEBUG: bool = True
    RETURN_VERIFICATION_CODE: bool = True  # 开发环境返回验证码
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()