from app.core.redis import redis_client
from typing import Optional
import redis

def get_redis() -> Optional[redis.Redis]:
    return redis_client

def init_redis():
    # redis_client is already initialized in app.core.redis
    pass