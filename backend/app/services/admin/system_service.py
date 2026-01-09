from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import json
import logging
from datetime import datetime
from app.models.website import SystemConfig
from app.schemas.admin.system import SystemConfigOut, SystemConfigUpdate
from app.core.redis import redis_client

logger = logging.getLogger(__name__)

CACHE_KEY_SYSTEM_CONFIGS = "system:configs:all"
CACHE_EXPIRE_SECONDS = 3600

class SystemService:
    def get_all_configs(self, db: Session) -> List[Dict[str, Any]]:
        """获取所有配置，优先从缓存获取"""
        cache_key = CACHE_KEY_SYSTEM_CONFIGS
        if redis_client:
            try:
                cached = redis_client.get(cache_key)
                if cached:
                    logger.info("System configs fetched from Redis cache")
                    return json.loads(cached)
            except Exception as e:
                logger.error(f"Error reading from Redis: {e}")

        configs = db.query(SystemConfig).all()
        # 使用 Pydantic 进行序列化
        serialized = [SystemConfigOut.model_validate(c).model_dump(mode='json') for c in configs]

        if redis_client:
            try:
                redis_client.setex(cache_key, CACHE_EXPIRE_SECONDS, json.dumps(serialized))
                logger.info("System configs cached to Redis")
            except Exception as e:
                logger.error(f"Error writing to Redis: {e}")

        return serialized

    def get_configs_by_prefix(self, db: Session, prefix: str) -> Dict[str, Any]:
        """按前缀获取配置，返回 Dict"""
        all_configs = self.get_all_configs(db)
        result = {}
        for c in all_configs:
            if c['config_key'].startswith(prefix):
                # 去掉前缀作为 key
                key = c['config_key'][len(prefix):].lstrip('.')
                result[key] = c['config_value']
        return result

    def update_configs(self, db: Session, configs_dict: Dict[str, Any]) -> bool:
        """批量更新配置"""
        try:
            for key, value in configs_dict.items():
                config = db.query(SystemConfig).filter(SystemConfig.config_key == key).first()
                # 转换值为字符串存储
                val_str = str(value).lower() if isinstance(value, bool) else str(value)
                
                if config:
                    config.config_value = val_str
                    config.updated_at = datetime.now()
                else:
                    # 如果不存在则创建
                    new_config = SystemConfig(
                        config_key=key, 
                        config_value=val_str,
                        is_public=False # 默认非公开
                    )
                    db.add(new_config)
            
            db.commit()
            self._clear_cache()
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating system configs: {e}")
            return False

    def update_config_item(self, db: Session, key: str, value: Any, is_public: Optional[bool] = None, description: Optional[str] = None):
        """更新单个配置项，支持修改元数据"""
        config = db.query(SystemConfig).filter(SystemConfig.config_key == key).first()
        val_str = str(value).lower() if isinstance(value, bool) else str(value)
        
        if config:
            config.config_value = val_str
            if is_public is not None:
                config.is_public = is_public
            if description is not None:
                config.description = description
            config.updated_at = datetime.now()
        else:
            config = SystemConfig(
                config_key=key,
                config_value=val_str,
                is_public=is_public if is_public is not None else False,
                description=description
            )
            db.add(config)
        
        db.commit()
        db.refresh(config)
        self._clear_cache()
        return config

    def get_public_configs(self, db: Session) -> Dict[str, Any]:
        """获取所有公开的配置（前端展示用）"""
        configs = self.get_all_configs(db)
        return {c['config_key']: c['config_value'] for c in configs if c.get('is_public')}

    def get_grouped_configs(self, db: Session) -> Dict[str, Any]:
        """按类别分组获取配置"""
        all_configs = self.get_all_configs(db)
        groups = {
            "base": {},
            "recognition": {},
            "quota": {},
            "notice": {},
            "security": {},
            "oss": {},
            "payment": {},
            "login": {},
            "ai": {},
            "other": {}
        }
        
        for c in all_configs:
            key = c['config_key']
            val = c['config_value']
            
            if key.startswith('base.'):
                groups['base'][key.split('.', 1)[1]] = val
            elif key.startswith('recognition.'):
                groups['recognition'][key.split('.', 1)[1]] = val
            elif key.startswith('quota.'):
                groups['quota'][key.split('.', 1)[1]] = val
            elif key.startswith('notice.'):
                groups['notice'][key.split('.', 1)[1]] = val
            elif key.startswith('security.'):
                groups['security'][key.split('.', 1)[1]] = val
            elif key.startswith('oss.'):
                groups['oss'][key.split('.', 1)[1]] = val
            elif key.startswith('payment.'):
                groups['payment'][key.split('.', 1)[1]] = val
            elif key.startswith('login.'):
                groups['login'][key.split('.', 1)[1]] = val
            elif key.startswith('ai.'):
                groups['ai'][key.split('.', 1)[1]] = val
            else:
                # 处理没有前缀的老数据
                if 'limit' in key:
                    groups['quota'][key] = val
                elif 'smtp' in key:
                    groups['notice'][key] = val
                elif 'oss' in key:
                    groups['oss'][key] = val
                elif 'seo' in key or 'availability' in key or 'client' in key:
                    groups['base'][key] = val
                elif 'pay' in key or 'alipay' in key or 'wechat' in key:
                    groups['payment'][key] = val
                elif 'ai.' in key:
                    groups['ai'][key.replace('ai.', '')] = val
                else:
                    groups['other'][key] = val
                    
        return groups

    def _clear_cache(self):
        if redis_client:
            try:
                redis_client.delete(CACHE_KEY_SYSTEM_CONFIGS)
                logger.info("System configs cache cleared")
            except Exception as e:
                logger.error(f"Error clearing system configs cache: {e}")

system_service = SystemService()
