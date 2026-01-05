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
        """发送验证码邮件"""
        subject = "【DarkVision-LPR】您的验证码"
        content = self._get_verification_code_template(code)
        return self.send_email([email], subject, content)
    
    def send_welcome_email(self, email: str, nickname: str) -> bool:
        """发送欢迎邮件"""
        subject = "欢迎加入 DarkVision-LPR 智能识别平台"
        content = self._get_welcome_template(nickname)
        return self.send_email([email], subject, content)
    
    def send_password_reset_email(self, email: str, reset_link: str) -> bool:
        """发送密码重置邮件"""
        subject = "【DarkVision-LPR】重置您的密码"
        content = self._get_password_reset_template(reset_link)
        return self.send_email([email], subject, content)
    
    @staticmethod
    def _get_base_style() -> str:
        """获取基础样式"""
        return """
        body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f4f7f6; }
        .container { max-width: 600px; margin: 40px auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); }
        .header { background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); padding: 40px 20px; text-align: center; }
        .logo { font-size: 24px; font-weight: 800; color: #ffffff; letter-spacing: 1px; margin: 0; }
        .logo span { background: rgba(255, 255, 255, 0.2); padding: 5px 10px; border-radius: 6px; margin-right: 8px; }
        .content { padding: 40px 30px; }
        .title { font-size: 22px; color: #1e293b; margin-bottom: 20px; font-weight: 600; }
        .text { font-size: 16px; color: #475569; margin-bottom: 20px; }
        .code-box { background-color: #f1f5f9; border-left: 4px solid #3b82f6; padding: 20px; margin: 30px 0; border-radius: 4px; text-align: center; }
        .code { font-size: 32px; font-weight: 700; color: #1e3a8a; letter-spacing: 6px; font-family: monospace; }
        .btn-primary { display: inline-block; background: #2563eb; color: #ffffff !important; text-decoration: none; padding: 14px 32px; border-radius: 50px; font-weight: 600; font-size: 16px; margin: 20px 0; box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2); transition: background 0.3s; }
        .btn-primary:hover { background: #1d4ed8; }
        .features { margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 20px; }
        .feature-item { display: flex; align-items: center; margin-bottom: 12px; color: #64748b; font-size: 14px; }
        .check-icon { color: #10b981; margin-right: 8px; font-weight: bold; }
        .footer { background-color: #f8fafc; padding: 30px 20px; text-align: center; border-top: 1px solid #e2e8f0; }
        .footer-text { font-size: 12px; color: #94a3b8; margin-bottom: 8px; }
        .footer-link { color: #3b82f6; text-decoration: none; font-size: 12px; margin: 0 5px; }
        .warning-text { font-size: 13px; color: #ef4444; margin-top: 10px; }
        """

    @staticmethod
    def _get_verification_code_template(code: str) -> str:
        """验证码邮件模板"""
        style = EmailService._get_base_style()
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>{style}</style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo"><span>DV</span>DarkVision LPR</div>
                </div>
                <div class="content">
                    <h2 class="title">🔐 安全验证</h2>
                    <p class="text">尊敬的用户，您好：</p>
                    <p class="text">您正在进行身份验证操作，请使用以下验证码完成验证。为保障账户安全，请勿将此验证码告知他人。</p>
                    
                    <div class="code-box">
                        <div class="code">{code}</div>
                    </div>
                    
                    <p class="text" style="font-size: 14px; color: #64748b; text-align: center;">
                        验证码有效时间为 <strong>5分钟</strong>
                    </p>
                    
                    <p class="warning-text" style="text-align: center;">如果您没有进行此操作，请忽略此邮件，这可能是系统误发。</p>
                </div>
                <div class="footer">
                    <p class="footer-text">此邮件由系统自动发送，请勿直接回复</p>
                    <p class="footer-text">© 2026 DarkVision-LPR. All rights reserved.</p>
                    <div style="margin-top: 10px;">
                        <a href="#" class="footer-link">隐私政策</a> • 
                        <a href="#" class="footer-link">服务条款</a> • 
                        <a href="#" class="footer-link">联系支持</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def _get_welcome_template(nickname: str) -> str:
        """欢迎邮件模板"""
        style = EmailService._get_base_style()
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>{style}</style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo"><span>DV</span>DarkVision LPR</div>
                </div>
                <div class="content">
                    <h2 class="title" style="text-align: center;">🚀 欢迎加入 DarkVision！</h2>
                    <p class="text">亲爱的 <strong>{nickname}</strong>，</p>
                    <p class="text">感谢您选择 DarkVision-LPR 车牌识别系统。我们致力于提供最精准、高效的 AI 识别服务。</p>
                    
                    <div class="features">
                        <p class="text" style="font-weight: 600;">作为免费会员，您已拥有：</p>
                        <div class="feature-item"><span class="check-icon">✓</span> 每日 10 次免费高精度识别额度</div>
                        <div class="feature-item"><span class="check-icon">✓</span> 支持复杂光照环境（夜间/逆光）</div>
                        <div class="feature-item"><span class="check-icon">✓</span> API 接口调用权限</div>
                        <div class="feature-item"><span class="check-icon">✓</span> 识别历史记录云端存储</div>
                    </div>
                    
                    <div style="text-align: center; margin-top: 30px;">
                        <a href="http://localhost:3001/dashboard" class="btn-primary">进入控制台</a>
                    </div>
                    
                    <p class="text" style="font-size: 14px; text-align: center; margin-top: 20px;">
                        提示：完善企业认证可解锁每日 1000+ 次识别额度
                    </p>
                </div>
                <div class="footer">
                    <p class="footer-text">© 2026 DarkVision-LPR. 让识别更简单。</p>
                    <div style="margin-top: 10px;">
                        <a href="#" class="footer-link">帮助文档</a> • 
                        <a href="#" class="footer-link">API指南</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def _get_password_reset_template(reset_link: str) -> str:
        """密码重置邮件模板"""
        style = EmailService._get_base_style()
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>{style}</style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo"><span>DV</span>DarkVision LPR</div>
                </div>
                <div class="content">
                    <h2 class="title">🔒 重置您的密码</h2>
                    <p class="text">尊敬的用户：</p>
                    <p class="text">我们收到了重置您账户密码的请求。如果您确定是本人操作，请点击下方按钮完成重置：</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{reset_link}" class="btn-primary">重置密码</a>
                    </div>
                    
                    <p class="text" style="font-size: 14px; color: #64748b;">
                        或者复制以下链接到浏览器打开：<br>
                        <a href="{reset_link}" style="color: #3b82f6; word-break: break-all;">{reset_link}</a>
                    </p>
                    
                    <div style="background: #fff1f2; border-radius: 8px; padding: 15px; margin-top: 20px; border: 1px solid #fecdd3;">
                        <p class="text" style="color: #be123c; margin: 0; font-size: 13px;">
                            ⚠️ 链接有效时间为 <strong>30分钟</strong>。如果这不是您的操作，请忽略此邮件，您的账户依然安全。
                        </p>
                    </div>
                </div>
                <div class="footer">
                    <p class="footer-text">© 2026 DarkVision-LPR. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """


# 创建邮件服务单例
email_service = EmailService()
