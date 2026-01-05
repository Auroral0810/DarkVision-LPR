import redis
from app.config import settings
from typing import Optional

redis_client: Optional[redis.Redis] = None

def init_redis():
    global redis_client
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        db=settings.REDIS_DB,
        decode_responses=True,
        socket_connect_timeout=5,
    )
    try:
        redis_client.ping()
        print("Redis connection established")
    except Exception as e:
        print(f"Redis connection failed: {e}")
        redis_client = None

def get_redis() -> Optional[redis.Redis]:
    return redis_client