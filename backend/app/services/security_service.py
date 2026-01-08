from sqlalchemy.orm import Session
from app.models.system import SystemIpRule
from app.models.website import SystemConfig
from app.schemas.admin import system as schemas
from typing import List, Optional
from datetime import datetime
import json

def get_ip_rules(db: Session, rule_type: Optional[str] = None) -> List[SystemIpRule]:
    query = db.query(SystemIpRule)
    if rule_type:
        query = query.filter(SystemIpRule.type == rule_type)
    return query.all()

def add_ip_rule(db: Session, rule_in: schemas.IpRuleCreate) -> SystemIpRule:
    rule = SystemIpRule(
        ip_address=rule_in.ip_address,
        type=rule_in.type,
        remark=rule_in.remark
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule

def delete_ip_rule(db: Session, rule_id: int) -> bool:
    rule = db.query(SystemIpRule).filter(SystemIpRule.id == rule_id).first()
    if not rule:
        return False
    db.delete(rule)
    db.commit()
    return True

def get_security_config(db: Session) -> schemas.SecurityConfigOut:
    # 从 system_configs 表读取相关配置
    keys = {
        "security.login_fail_limit": 5,
        "security.login_lock_duration": 30,
        "security.api_rate_limit": 100,
        "security.enable_ip_whitelist": False
    }
    
    result = {}
    for key, default in keys.items():
        config = db.query(SystemConfig).filter(SystemConfig.config_key == key).first()
        if config:
            # 简单类型转换
            val = config.config_value
            if isinstance(default, bool):
                val = val.lower() == "true"
            elif isinstance(default, int):
                val = int(val)
            result[key.split(".")[-1]] = val
        else:
            result[key.split(".")[-1]] = default
            
    return schemas.SecurityConfigOut(**result)

def update_security_config(db: Session, config_in: schemas.SecurityConfigUpdate):
    updates = config_in.model_dump(exclude_unset=True)
    for k, v in updates.items():
        key = f"security.{k}"
        config = db.query(SystemConfig).filter(SystemConfig.config_key == key).first()
        if not config:
            config = SystemConfig(config_key=key, config_value=str(v).lower() if isinstance(v, bool) else str(v))
            db.add(config)
        else:
            config.config_value = str(v).lower() if isinstance(v, bool) else str(v)
            config.updated_at = datetime.now()
    
    db.commit()
    return get_security_config(db)
