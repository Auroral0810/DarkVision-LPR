"""
在线用户管理服务
使用 Redis 存储在线用户状态
"""
from typing import Optional
from app.core.cache import get_redis
from app.core.logger import logger
from datetime import datetime

# Redis Key 前缀
ONLINE_USER_KEY_PREFIX = "online_users:"
# 在线用户过期时间（秒）- 5分钟
ONLINE_USER_EXPIRE_SECONDS = 300


def set_user_online(user_id: int) -> bool:
    """
    设置用户在线状态
    
    Args:
        user_id: 用户ID
        
    Returns:
        bool: 是否成功
    """
    redis_client = get_redis()
    if not redis_client:
        logger.warning("Redis not available, cannot set user online")
        return False
    
    key = f"{ONLINE_USER_KEY_PREFIX}{user_id}"
    timestamp = int(datetime.now().timestamp())
    
    try:
        redis_client.setex(key, ONLINE_USER_EXPIRE_SECONDS, timestamp)
        logger.debug(f"User {user_id} set online, expires in {ONLINE_USER_EXPIRE_SECONDS}s")
        return True
    except Exception as e:
        logger.error(f"Failed to set user online: {e}")
        return False


def refresh_user_online(user_id: int) -> bool:
    """
    刷新用户在线状态（心跳机制）
    延长过期时间
    
    Args:
        user_id: 用户ID
        
    Returns:
        bool: 是否成功
    """
    redis_client = get_redis()
    if not redis_client:
        return False
    
    key = f"{ONLINE_USER_KEY_PREFIX}{user_id}"
    
    # 检查 key 是否存在
    if not redis_client.exists(key):
        # 如果不存在，创建新的
        return set_user_online(user_id)
    
    try:
        # 刷新过期时间
        redis_client.expire(key, ONLINE_USER_EXPIRE_SECONDS)
        logger.debug(f"User {user_id} online status refreshed")
        return True
    except Exception as e:
        logger.error(f"Failed to refresh user online status: {e}")
        return False


def set_user_offline(user_id: int) -> bool:
    """
    设置用户离线状态（删除 Redis key）
    
    Args:
        user_id: 用户ID
        
    Returns:
        bool: 是否成功
    """
    redis_client = get_redis()
    if not redis_client:
        return False
    
    key = f"{ONLINE_USER_KEY_PREFIX}{user_id}"
    
    try:
        redis_client.delete(key)
        logger.debug(f"User {user_id} set offline")
        return True
    except Exception as e:
        logger.error(f"Failed to set user offline: {e}")
        return False


def is_user_online(user_id: int) -> bool:
    """
    检查用户是否在线
    
    Args:
        user_id: 用户ID
        
    Returns:
        bool: 是否在线
    """
    redis_client = get_redis()
    if not redis_client:
        return False
    
    key = f"{ONLINE_USER_KEY_PREFIX}{user_id}"
    return bool(redis_client.exists(key))


def get_online_user_count() -> int:
    """
    获取当前在线用户数
    
    Returns:
        int: 在线用户数
    """
    redis_client = get_redis()
    if not redis_client:
        logger.warning("Redis not available, cannot get online user count")
        return 0
    
    try:
        # 使用 SCAN 代替 KEYS（生产环境推荐）
        pattern = f"{ONLINE_USER_KEY_PREFIX}*"
        count = 0
        
        # 使用 SCAN 迭代所有匹配的 key
        cursor = 0
        while True:
            cursor, keys = redis_client.scan(cursor, match=pattern, count=100)
            count += len(keys)
            if cursor == 0:
                break
        
        return count
    except Exception as e:
        logger.error(f"Failed to get online user count: {e}")
        return 0


def get_online_user_ids() -> list[int]:
    """
    获取所有在线用户的ID列表
    
    Returns:
        list[int]: 在线用户ID列表
    """
    redis_client = get_redis()
    if not redis_client:
        return []
    
    try:
        pattern = f"{ONLINE_USER_KEY_PREFIX}*"
        user_ids = []
        
        cursor = 0
        while True:
            cursor, keys = redis_client.scan(cursor, match=pattern, count=100)
            for key in keys:
                # 从 key 中提取 user_id
                # Redis decode_responses=True 时，key 已经是字符串
                key_str = key if isinstance(key, str) else key.decode('utf-8')
                user_id_str = key_str.replace(ONLINE_USER_KEY_PREFIX, '')
                try:
                    user_ids.append(int(user_id_str))
                except ValueError:
                    continue
            if cursor == 0:
                break
        
        return user_ids
    except Exception as e:
        logger.error(f"Failed to get online user IDs: {e}")
        return []

