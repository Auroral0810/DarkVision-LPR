from fastapi import APIRouter, Depends, BackgroundTasks, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.response import success_response
from app.models.contact import ContactMessage
from app.schemas.contact import ContactCreate, ContactResponse
from app.services.email import email_service
from app.core.logger import logger

router = APIRouter()

@router.post("/submit", response_model=ContactResponse, summary="提交在线咨询")
async def submit_contact(
    contact_data: ContactCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    提交在线咨询
    
    - 记录到数据库
    - 发送邮件通知管理员
    """
    # 1. 记录到数据库
    client_ip = request.client.host
    contact_msg = ContactMessage(
        name=contact_data.name,
        email=contact_data.email,
        message=contact_data.message,
        ip_address=client_ip
    )
    db.add(contact_msg)
    db.commit()
    db.refresh(contact_msg)
    
    # 2. 发送邮件通知管理员 (后台任务)
    background_tasks.add_task(
        send_notification_email, 
        contact_data.name, 
        contact_data.email, 
        contact_data.message
    )
    
    return success_response(message="提交成功，我们会尽快回复您！")

def send_notification_email(name: str, email: str, message: str):
    """发送极具科技感的通知邮件给管理员"""
    subject = f"🔔 [DarkVision AI] 新咨询提醒：{name}"
    
    # 模拟当前时间
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = f"""
    <div style="background-color: #0f172a; padding: 40px 20px; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #f8fafc; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #1e293b; border-radius: 12px; overflow: hidden; border: 1px solid #334155; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);">
            
            <!-- 头部装饰条 -->
            <div style="background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%); height: 6px;"></div>
            
            <!-- 主体内容 -->
            <div style="padding: 30px;">
                <h2 style="margin-top: 0; color: #ffffff; font-size: 24px; font-weight: 600; letter-spacing: -0.025em;">
                    🚀 收到新的在线咨询
                </h2>
                <p style="color: #94a3b8; font-size: 14px; margin-bottom: 24px;">
                    系统时间：{now} (UTC+8)
                </p>
                
                <!-- 用户信息卡片 -->
                <div style="background-color: #0f172a; border-radius: 8px; padding: 20px; margin-bottom: 24px; border: 1px solid #334155;">
                    <div style="margin-bottom: 12px;">
                        <span style="color: #64748b; font-size: 12px; text-transform: uppercase; font-weight: 700; display: block; margin-bottom: 4px;">咨询客户</span>
                        <strong style="color: #f8fafc; font-size: 16px;">{name}</strong>
                    </div>
                    <div>
                        <span style="color: #64748b; font-size: 12px; text-transform: uppercase; font-weight: 700; display: block; margin-bottom: 4px;">联系邮箱</span>
                        <a href="mailto:{email}" style="color: #3b82f6; text-decoration: none; font-size: 16px;">{email}</a>
                    </div>
                </div>
                
                <!-- 消息内容 -->
                <div style="margin-bottom: 30px;">
                    <span style="color: #64748b; font-size: 12px; text-transform: uppercase; font-weight: 700; display: block; margin-bottom: 10px;">详情内容</span>
                    <div style="background-color: rgba(59, 130, 246, 0.05); border-left: 4px solid #3b82f6; padding: 15px 20px; font-size: 15px; color: #e2e8f0; white-space: pre-wrap;">{message}</div>
                </div>
                
                <!-- 交互按钮 -->
                <div style="text-align: center;">
                    <a href="mailto:{email}" style="display: inline-block; background: #3b82f6; color: white; padding: 12px 30px; border-radius: 6px; font-weight: 600; text-decoration: none; transition: background 0.2s;">
                        立即回复客户
                    </a>
                </div>
            </div>
            
            <!-- 页脚 -->
            <div style="background-color: #111827; padding: 20px; text-align: center; border-top: 1px solid #334155;">
                <p style="margin: 0; color: #64748b; font-size: 12px;">
                    此邮件由 <strong>DarkVision-LPR</strong> 智能监测系统自动发送
                </p>
                <p style="margin: 5px 0 0; color: #475569; font-size: 11px;">
                    © 2026 DarkVision AI Technology. All rights reserved.
                </p>
            </div>
        </div>
    </div>
    """
    
    admin_email = "15968588744@163.com"
    try:
        email_service.send_email([admin_email], subject, content)
        logger.info(f"高级感通知邮件已发送至 {admin_email}")
    except Exception as e:
        logger.error(f"邮件发送失败: {e}")

