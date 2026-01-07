import redis
from app.config import settings
from app.core.logger import logger

# 创建 Redis 连接池
pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    db=settings.REDIS_DB,
    decode_responses=True,  # 自动解码为字符串
    encoding='utf-8',
)

# 创建 Redis 客户端
try:
    redis_client = redis.Redis(connection_pool=pool)
    # 测试连接
    redis_client.ping()
    logger.info("Redis connected successfully")
except redis.ConnectionError as e:
    logger.error(f"Redis connection failed: {e}")
    redis_client = None
