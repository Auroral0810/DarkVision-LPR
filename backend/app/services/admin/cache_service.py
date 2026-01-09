from typing import List, Dict, Any, Optional
from app.core.redis import redis_client
from app.schemas.admin.maintenance import CacheStats, CacheKeyInfo
import time

class CacheService:
    @staticmethod
    def get_stats() -> CacheStats:
        """获取 Redis 统计信息"""
        info = redis_client.info()
        # 获取键的总数
        db_size = redis_client.dbsize()
        
        return CacheStats(
            redis_version=info.get("redis_version", "unknown"),
            uptime_in_seconds=info.get("uptime_in_seconds", 0),
            used_memory_human=info.get("used_memory_human", "0B"),
            connected_clients=info.get("connected_clients", 0),
            keys_count=db_size
        )

    @staticmethod
    def list_keys(pattern: str = "*", limit: int = 100) -> List[CacheKeyInfo]:
        """获取 Redis 键列表 (带元数据)"""
        keys = redis_client.keys(pattern)
        # 限制数量
        keys = keys[:limit]
        
        result = []
        for key in keys:
            k_type = redis_client.type(key)
            ttl = redis_client.ttl(key)
            
            # 粗略估计大小 (如果是字符串则直接获取长度，其它复杂类型简单处理)
            size = 0
            try:
                if k_type == "string":
                    size = redis_client.strlen(key)
                elif k_type == "list":
                    size = redis_client.llen(key)
                elif k_type == "set":
                    size = redis_client.scard(key)
                elif k_type == "zset":
                    size = redis_client.zcard(key)
                elif k_type == "hash":
                    size = redis_client.hlen(key)
            except:
                pass
                
            result.append(CacheKeyInfo(
                key=key,
                type=k_type,
                ttl=ttl,
                size=size
            ))
        return result

    @staticmethod
    def clear_cache(prefix: Optional[str] = None, keys: Optional[List[str]] = None) -> int:
        """清理缓存"""
        if keys:
            return redis_client.delete(*keys)
        
        if prefix:
            target_keys = redis_client.keys(f"{prefix}*")
            if target_keys:
                return redis_client.delete(*target_keys)
            return 0
            
        # 危险操作：清空当前库
        # redis_client.flushdb() 
        # 为了安全，我们通常只通过前缀清除相关缓存
        # 这里默认清除所有，但实际应用中可能需要更谨慎
        all_keys = redis_client.keys("*")
        if all_keys:
            return redis_client.delete(*all_keys)
        return 0

cache_service = CacheService()
