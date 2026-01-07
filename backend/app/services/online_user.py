from app.core.redis import redis_client
from app.config import settings

class OnlineUserService:
    """在线用户服务"""
    
    # Redis Key 前缀
    ONLINE_USER_KEY_PREFIX = "online_users:"
    # 过期时间（秒），默认 5 分钟
    ONLINE_USER_EXPIRE = 300
    
    @classmethod
    def set_online(cls, user_id: int):
        """
        设置用户为在线状态
        """
        if not redis_client:
            return
            
        key = f"{cls.ONLINE_USER_KEY_PREFIX}{user_id}"
        # 设置 key，值为当前时间戳，过期时间 5 分钟
        import time
        redis_client.set(key, int(time.time()), ex=cls.ONLINE_USER_EXPIRE)
        
    @classmethod
    def get_online_count(cls) -> int:
        """
        获取当前在线用户数
        """
        if not redis_client:
            return 0
            
        # 扫描所有 online_users:* 的 key
        # 注意：keys 命令在生产环境大量数据时可能会阻塞，但在管理后台场景下通常没问题
        # 更优方案是维护一个 set，但这里为了简单直接用 pattern match
        keys = redis_client.keys(f"{cls.ONLINE_USER_KEY_PREFIX}*")
        return len(keys)
        
    @classmethod
    def remove_online(cls, user_id: int):
        """
        移除用户的在线状态（登出时调用）
        """
        if not redis_client:
            return 
            
        key = f"{cls.ONLINE_USER_KEY_PREFIX}{user_id}"
        redis_client.delete(key)
