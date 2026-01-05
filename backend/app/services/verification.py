"""
验证码服务（短信和邮箱）
"""
import random
import string
from typing import Optional
from app.core.cache import get_redis
from app.core.logger import logger
from app.core.exceptions import ParameterException


class VerificationCodeService:
    """验证码服务"""
    
    # 验证码有效期（秒）
    CODE_EXPIRE_TIME = 300  # 5分钟
    
    # 发送频率限制（秒）
    SEND_INTERVAL = 60  # 1分钟内只能发送一次
    
    # 验证码长度
    CODE_LENGTH = 6
    
    @staticmethod
    def generate_code(length: int = CODE_LENGTH) -> str:
        """
        生成随机验证码
        
        Args:
            length: 验证码长度
            
        Returns:
            str: 数字验证码
        """
        return ''.join(random.choices(string.digits, k=length))
    
    @staticmethod
    def get_redis_key(scene: str, target: str) -> str:
        """
        生成 Redis 键
        
        Args:
            scene: 场景 (login/register/reset_password)
            target: 目标 (手机号或邮箱)
            
        Returns:
            str: Redis键
        """
        return f"verification_code:{scene}:{target}"
    
    @staticmethod
    def get_rate_limit_key(target: str) -> str:
        """生成频率限制 Redis 键"""
        return f"code_rate_limit:{target}"
    
    @classmethod
    def check_send_frequency(cls, target: str) -> bool:
        """
        检查发送频率
        
        Args:
            target: 手机号或邮箱
            
        Returns:
            bool: 是否可以发送
        """
        redis_client = get_redis()
        if not redis_client:
            return True
        
        key = cls.get_rate_limit_key(target)
        if redis_client.exists(key):
            return False
        
        return True
    
    @classmethod
    def set_send_frequency_limit(cls, target: str):
        """设置发送频率限制"""
        redis_client = get_redis()
        if redis_client:
            key = cls.get_rate_limit_key(target)
            redis_client.setex(key, cls.SEND_INTERVAL, "1")
    
    @classmethod
    def store_code(cls, scene: str, target: str, code: str) -> bool:
        """
        存储验证码到 Redis
        
        Args:
            scene: 使用场景
            target: 手机号或邮箱
            code: 验证码
            
        Returns:
            bool: 是否成功
        """
        redis_client = get_redis()
        if not redis_client:
            logger.error("Redis not available")
            return False
        
        key = cls.get_redis_key(scene, target)
        redis_client.setex(key, cls.CODE_EXPIRE_TIME, code)
        logger.info(f"Stored verification code for {target}, scene: {scene}")
        return True
    
    @classmethod
    def verify_code(cls, scene: str, target: str, code: str) -> bool:
        """
        验证验证码
        
        Args:
            scene: 使用场景
            target: 手机号或邮箱
            code: 用户输入的验证码
            
        Returns:
            bool: 是否验证成功
        """
        redis_client = get_redis()
        if not redis_client:
            logger.error("Redis not available for code verification")
            return False
        
        key = cls.get_redis_key(scene, target)
        stored_code = redis_client.get(key)
        
        if not stored_code:
            logger.warning(f"Verification code expired or not found for {target}")
            return False
        
        # 处理 Redis 返回类型（bytes 或 str）
        if isinstance(stored_code, bytes):
            stored_code_str = stored_code.decode('utf-8')
        else:
            stored_code_str = str(stored_code)
        
        if stored_code_str == code:
            # 验证成功后删除验证码
            redis_client.delete(key)
            logger.info(f"Verification code verified successfully for {target}")
            return True
        
        logger.warning(f"Invalid verification code for {target}")
        return False
    
    @classmethod
    def send_sms_code(cls, phone: str, scene: str) -> str:
        """
        发送短信验证码
        
        Args:
            phone: 手机号
            scene: 使用场景
            
        Returns:
            str: 验证码（开发环境返回，生产环境不返回）
            
        Raises:
            ParameterException: 发送频率过高
        """
        # 检查发送频率
        if not cls.check_send_frequency(phone):
            raise ParameterException(f"发送过于频繁，请{cls.SEND_INTERVAL}秒后再试")
        
        # 生成验证码
        code = cls.generate_code()
        
        # 存储到 Redis
        cls.store_code(scene, phone, code)
        
        # 设置频率限制
        cls.set_send_frequency_limit(phone)
        
        # TODO: 实际发送短信（对接短信服务商）
        logger.info(f"SMS code sent to {phone}: {code} (scene: {scene})")
        
        # 开发环境返回验证码，生产环境不返回
        from app.config import settings
        if settings.RETURN_VERIFICATION_CODE:
            return code
        return ""
    
    @classmethod
    def send_email_code(cls, email: str, scene: str) -> str:
        """
        发送邮箱验证码
        
        Args:
            email: 邮箱
            scene: 使用场景
            
        Returns:
            str: 验证码（开发环境返回，生产环境不返回）
            
        Raises:
            ParameterException: 发送频率过高
        """
        # 检查发送频率
        if not cls.check_send_frequency(email):
            raise ParameterException(f"发送过于频繁，请{cls.SEND_INTERVAL}秒后再试")
        
        # 生成验证码
        code = cls.generate_code()
        
        # 存储到 Redis
        cls.store_code(scene, email, code)
        
        # 设置频率限制
        cls.set_send_frequency_limit(email)
        
        # 实际发送邮件
        try:
            from app.services.email import email_service
            email_service.send_verification_code(email, code)
            logger.info(f"Email code sent to {email}: {code} (scene: {scene})")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            # 即使邮件发送失败，验证码也已存储，开发环境可以使用返回的验证码
        
        # 开发环境返回验证码，生产环境不返回
        from app.config import settings
        if settings.RETURN_VERIFICATION_CODE:
            return code
        return ""


# 导出单例
verification_service = VerificationCodeService()

