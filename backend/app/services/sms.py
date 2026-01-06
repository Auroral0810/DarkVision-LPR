"""
短信发送服务（短信宝）
"""
import urllib.request
import urllib.parse
import hashlib
from typing import Optional
from app.core.logger import logger
from app.core.exceptions import ThirdPartyException
from app.config import settings


class SMSService:
    """短信服务类"""
    
    # 短信宝状态码映射
    STATUS_MESSAGES = {
        '0': '短信发送成功',
        '-1': '参数不全',
        '-2': '服务器空间不支持,请确认支持curl或者fsocket',
        '30': '密码错误',
        '40': '账号不存在',
        '41': '余额不足',
        '42': '账户已过期',
        '43': 'IP地址限制',
        '50': '内容含有敏感词'
    }
    
    @staticmethod
    def md5(text: str) -> str:
        """
        MD5加密
        
        Args:
            text: 待加密字符串
            
        Returns:
            str: MD5加密后的字符串
        """
        m = hashlib.md5()
        m.update(text.encode("utf8"))
        return m.hexdigest()
    
    @classmethod
    def send_verification_code(cls, phone: str, code: str, scene: str = "login") -> bool:
        """
        发送验证码短信
        
        Args:
            phone: 手机号
            code: 验证码
            scene: 使用场景 (login/register/reset_password)
            
        Returns:
            bool: 是否发送成功
            
        Raises:
            ThirdPartyException: 短信发送失败
        """
        # 检查配置
        if not settings.SMS_USER or not settings.SMS_PASSWORD:
            logger.error("SMS configuration is missing")
            raise ThirdPartyException("短信服务配置不完整")
        
        # 根据场景构建短信内容
        scene_text = {
            "login": "登录",
            "register": "注册",
            "reset_password": "重置密码"
        }.get(scene, "验证")
        
        content = f"【{settings.SMS_SIGN_NAME}】您的{scene_text}验证码是{code}。如非本人操作，请忽略本短信"
        
        try:
            # 密码MD5加密
            password_md5 = cls.md5(settings.SMS_PASSWORD)
            
            # 准备请求参数（注意：content 需要 URL 编码）
            params = {
                'u': settings.SMS_USER,
                'p': password_md5,
                'm': phone,
                'c': content
            }
            
            # 构建请求URL
            data = urllib.parse.urlencode(params, encoding='utf-8')
            send_url = f"{settings.SMS_API_URL}?{data}"
            
            logger.info(f"Sending SMS to {phone}, scene: {scene}, content: {content}")
            logger.debug(f"SMS API URL: {send_url[:80]}...")  # 只显示前80个字符，避免泄露密码
            
            # 发送请求
            response = urllib.request.urlopen(send_url, timeout=10)
            result = response.read().decode('utf-8').strip()
            
            logger.info(f"SMS API response: {result}")
            
            # 处理响应
            status_message = cls.STATUS_MESSAGES.get(result, f"未知错误代码: {result}")
            
            if result == '0':
                logger.info(f"SMS sent successfully to {phone}")
                return True
            else:
                logger.error(f"SMS send failed: {status_message} (code: {result})")
                raise ThirdPartyException(f"短信发送失败: {status_message}")
                
        except ThirdPartyException:
            # 重新抛出业务异常
            raise
        except urllib.error.URLError as e:
            logger.error(f"SMS API request failed: {e}")
            raise ThirdPartyException("短信服务连接失败，请稍后重试")
        except Exception as e:
            logger.error(f"SMS send error: {type(e).__name__}: {e}")
            raise ThirdPartyException(f"短信发送异常: {str(e)}")
    
    @classmethod
    def send_custom_message(cls, phone: str, content: str) -> bool:
        """
        发送自定义短信内容
        
        Args:
            phone: 手机号
            content: 短信内容（需包含签名）
            
        Returns:
            bool: 是否发送成功
            
        Raises:
            ThirdPartyException: 短信发送失败
        """
        # 检查配置
        if not settings.SMS_USER or not settings.SMS_PASSWORD:
            logger.error("SMS configuration is missing")
            raise ThirdPartyException("短信服务配置不完整")
        
        try:
            # 准备请求参数
            password_md5 = cls.md5(settings.SMS_PASSWORD)
            params = {
                'u': settings.SMS_USER,
                'p': password_md5,
                'm': phone,
                'c': content
            }
            
            # 构建请求URL
            data = urllib.parse.urlencode(params)
            send_url = f"{settings.SMS_API_URL}?{data}"
            
            logger.info(f"Sending custom SMS to {phone}")
            
            # 发送请求
            response = urllib.request.urlopen(send_url, timeout=10)
            result = response.read().decode('utf-8')
            
            # 处理响应
            status_message = cls.STATUS_MESSAGES.get(result, f"未知错误代码: {result}")
            
            if result == '0':
                logger.info(f"Custom SMS sent successfully to {phone}")
                return True
            else:
                logger.error(f"Custom SMS send failed: {status_message} (code: {result})")
                raise ThirdPartyException(f"短信发送失败: {status_message}")
                
        except urllib.error.URLError as e:
            logger.error(f"SMS API request failed: {e}")
            raise ThirdPartyException("短信服务连接失败，请稍后重试")
        except Exception as e:
            logger.error(f"Custom SMS send error: {e}")
            raise ThirdPartyException(f"短信发送异常: {str(e)}")


# 导出单例
sms_service = SMSService()

