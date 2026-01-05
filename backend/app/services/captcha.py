"""
图形验证码服务
"""
import io
import random
import string
from captcha.image import ImageCaptcha
from PIL import Image
from typing import Tuple
from app.core.cache import get_redis
from app.core.logger import logger


class CaptchaService:
    """图形验证码服务"""
    
    # 验证码有效期（秒）
    CAPTCHA_EXPIRE_TIME = 300  # 5分钟
    
    # 验证码长度
    CAPTCHA_LENGTH = 4
    
    # 图片尺寸
    IMAGE_WIDTH = 160
    IMAGE_HEIGHT = 60
    
    def __init__(self):
        """初始化验证码生成器"""
        self.image_captcha = ImageCaptcha(
            width=self.IMAGE_WIDTH,
            height=self.IMAGE_HEIGHT,
            fonts=None,  # 使用默认字体
            font_sizes=(42, 50, 56)
        )
    
    @staticmethod
    def generate_code(length: int = CAPTCHA_LENGTH) -> str:
        """
        生成随机验证码文本
        
        Args:
            length: 验证码长度
            
        Returns:
            str: 验证码文本
        """
        # 使用数字和大写字母（排除易混淆的字符：0、O、I、1、l）
        chars = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ'
        return ''.join(random.choices(chars, k=length))
    
    @staticmethod
    def get_redis_key(captcha_id: str) -> str:
        """
        生成 Redis 键
        
        Args:
            captcha_id: 验证码ID（UUID）
            
        Returns:
            str: Redis键
        """
        return f"captcha:{captcha_id}"
    
    def generate_captcha(self, captcha_id: str) -> Tuple[bytes, str]:
        """
        生成图形验证码
        
        Args:
            captcha_id: 验证码ID
            
        Returns:
            Tuple[bytes, str]: (图片字节数据, 验证码文本)
        """
        # 生成验证码文本
        code = self.generate_code()
        
        # 生成验证码图片
        image = self.image_captcha.generate_image(code)
        
        # 将PIL Image转换为bytes
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='PNG')
        img_bytes = img_buffer.getvalue()
        
        # 存储到Redis
        self.store_captcha(captcha_id, code)
        
        logger.info(f"Generated captcha: {captcha_id} (code: {code})")
        
        return img_bytes, code
    
    @classmethod
    def store_captcha(cls, captcha_id: str, code: str) -> bool:
        """
        存储验证码到 Redis
        
        Args:
            captcha_id: 验证码ID
            code: 验证码文本
            
        Returns:
            bool: 是否成功
        """
        redis_client = get_redis()
        if not redis_client:
            logger.error("Redis not available")
            return False
        
        key = cls.get_redis_key(captcha_id)
        redis_client.setex(key, cls.CAPTCHA_EXPIRE_TIME, code.upper())
        logger.info(f"Stored captcha: {captcha_id} with {cls.CAPTCHA_EXPIRE_TIME}s expiry")
        return True
    
    @classmethod
    def verify_captcha(cls, captcha_id: str, code: str) -> bool:
        """
        验证图形验证码
        
        Args:
            captcha_id: 验证码ID
            code: 用户输入的验证码
            
        Returns:
            bool: 是否验证成功
        """
        redis_client = get_redis()
        if not redis_client:
            logger.error("Redis not available for captcha verification")
            return False
        
        key = cls.get_redis_key(captcha_id)
        stored_code = redis_client.get(key)
        
        if not stored_code:
            logger.warning(f"Captcha expired or not found: {captcha_id}")
            return False
        
        # 处理 Redis 返回类型（bytes 或 str）
        if isinstance(stored_code, bytes):
            stored_code_str = stored_code.decode('utf-8')
        else:
            stored_code_str = str(stored_code)
            
        # 不区分大小写比较
        if stored_code_str.upper() == code.upper():
            # 验证成功后删除验证码（一次性使用）
            redis_client.delete(key)
            logger.info(f"Captcha verified successfully: {captcha_id}")
            return True
        
        logger.warning(f"Invalid captcha code for: {captcha_id}")
        return False
    
    @classmethod
    def delete_captcha(cls, captcha_id: str) -> bool:
        """
        删除验证码（用于刷新验证码时清理旧的）
        
        Args:
            captcha_id: 验证码ID
            
        Returns:
            bool: 是否成功
        """
        redis_client = get_redis()
        if redis_client:
            key = cls.get_redis_key(captcha_id)
            redis_client.delete(key)
            logger.info(f"Deleted captcha: {captcha_id}")
            return True
        return False


# 创建验证码服务单例
captcha_service = CaptchaService()

