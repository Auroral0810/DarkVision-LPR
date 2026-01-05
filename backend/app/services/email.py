"""
邮件服务
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import List, Optional
from app.config import settings
from app.core.logger import logger


class EmailService:
    """邮件服务类"""
    
    def __init__(self):
        self.host = settings.MAIL_HOST
        self.port = settings.MAIL_PORT
        self.username = settings.MAIL_USERNAME
        self.password = settings.MAIL_PASSWORD
        self.from_addr = settings.MAIL_FROM
        self.from_name = settings.MAIL_FROM_NAME
        self.use_ssl = settings.MAIL_USE_SSL
    
    def send_email(
        self,
        to_addrs: List[str],
        subject: str,
        content: str,
        content_type: str = "html"
    ) -> bool:
        """
        发送邮件
        
        Args:
            to_addrs: 收件人列表
            subject: 邮件主题
            content: 邮件内容
            content_type: 内容类型 (html/plain)
            
        Returns:
            bool: 是否发送成功
        """
        try:
            # 创建邮件对象
            message = MIMEMultipart()
            message['From'] = Header(f"{self.from_name} <{self.from_addr}>", 'utf-8')
            message['To'] = Header(", ".join(to_addrs), 'utf-8')
            message['Subject'] = Header(subject, 'utf-8')
            
            # 邮件正文
            message.attach(MIMEText(content, content_type, 'utf-8'))
            
            # 连接SMTP服务器
            if self.use_ssl:
                server = smtplib.SMTP_SSL(self.host, self.port)
            else:
                server = smtplib.SMTP(self.host, self.port)
                server.starttls()
            
            # 登录
            server.login(self.username, self.password)
            
            # 发送邮件
            server.sendmail(self.from_addr, to_addrs, message.as_string())
            server.quit()
            
            logger.info(f"Email sent successfully to {', '.join(to_addrs)}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def send_verification_code(self, email: str, code: str) -> bool:
        """
        发送验证码邮件
        
        Args:
            email: 邮箱地址
            code: 验证码
            
        Returns:
            bool: 是否发送成功
        """
        subject = "【DarkVision-LPR】验证码"
        content = self._get_verification_code_template(code)
        return self.send_email([email], subject, content)
    
    def send_welcome_email(self, email: str, nickname: str) -> bool:
        """
        发送欢迎邮件
        
        Args:
            email: 邮箱地址
            nickname: 用户昵称
            
        Returns:
            bool: 是否发送成功
        """
        subject = "欢迎使用 DarkVision-LPR 车牌识别系统"
        content = self._get_welcome_template(nickname)
        return self.send_email([email], subject, content)
    
    def send_password_reset_email(self, email: str, reset_link: str) -> bool:
        """
        发送密码重置邮件
        
        Args:
            email: 邮箱地址
            reset_link: 重置链接
            
        Returns:
            bool: 是否发送成功
        """
        subject = "【DarkVision-LPR】密码重置"
        content = self._get_password_reset_template(reset_link)
        return self.send_email([email], subject, content)
    
    @staticmethod
    def _get_verification_code_template(code: str) -> str:
        """验证码邮件模板"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
        .code {{ font-size: 32px; font-weight: bold; color: #667eea; text-align: center; padding: 20px; background: white; border-radius: 8px; margin: 20px 0; letter-spacing: 5px; }}
        .footer {{ text-align: center; margin-top: 30px; color: #999; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>DarkVision-LPR</h1>
            <p>车牌识别系统</p>
        </div>
        <div class="content">
            <h2>验证码</h2>
            <p>您好！</p>
            <p>您正在进行身份验证，您的验证码是：</p>
            <div class="code">{code}</div>
            <p><strong>验证码有效期为5分钟</strong>，请尽快使用。</p>
            <p>如果这不是您本人的操作，请忽略此邮件。</p>
        </div>
        <div class="footer">
            <p>此邮件由系统自动发送，请勿直接回复</p>
            <p>© 2026 DarkVision-LPR. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
        """
    
    @staticmethod
    def _get_welcome_template(nickname: str) -> str:
        """欢迎邮件模板"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
        .features {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .feature-item {{ padding: 10px 0; border-bottom: 1px solid #eee; }}
        .footer {{ text-align: center; margin-top: 30px; color: #999; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 欢迎加入 DarkVision-LPR！</h1>
        </div>
        <div class="content">
            <h2>你好，{nickname}！</h2>
            <p>感谢您注册 DarkVision-LPR 车牌识别系统！</p>
            <p>作为免费用户，您可以享受以下功能：</p>
            <div class="features">
                <div class="feature-item">✓ 每日10次车牌识别额度</div>
                <div class="feature-item">✓ 高精度车牌识别</div>
                <div class="feature-item">✓ 识别历史记录查询</div>
                <div class="feature-item">✓ 多平台支持（Web、桌面、移动端）</div>
            </div>
            <p>如需更多额度和功能，请考虑升级为VIP会员或企业用户！</p>
            <p style="text-align: center; margin-top: 30px;">
                <a href="http://localhost:3001" style="background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">立即开始使用</a>
            </p>
        </div>
        <div class="footer">
            <p>此邮件由系统自动发送，请勿直接回复</p>
            <p>© 2026 DarkVision-LPR. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
        """
    
    @staticmethod
    def _get_password_reset_template(reset_link: str) -> str:
        """密码重置邮件模板"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
        .button {{ background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }}
        .footer {{ text-align: center; margin-top: 30px; color: #999; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>DarkVision-LPR</h1>
            <p>密码重置</p>
        </div>
        <div class="content">
            <h2>重置您的密码</h2>
            <p>您好！</p>
            <p>我们收到了重置您账户密码的请求。</p>
            <p>请点击下方按钮重置密码：</p>
            <p style="text-align: center;">
                <a href="{reset_link}" class="button">重置密码</a>
            </p>
            <p>或复制以下链接到浏览器：</p>
            <p style="word-break: break-all; color: #667eea;">{reset_link}</p>
            <p><strong>此链接30分钟内有效</strong></p>
            <p>如果这不是您本人的操作，请忽略此邮件，您的密码不会被改变。</p>
        </div>
        <div class="footer">
            <p>此邮件由系统自动发送，请勿直接回复</p>
            <p>© 2026 DarkVision-LPR. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
        """


# 创建邮件服务单例
email_service = EmailService()

