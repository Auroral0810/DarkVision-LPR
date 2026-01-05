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
    """发送通知邮件给管理员"""
    subject = f"【DarkVision-LPR】收到新的在线咨询 - 来自 {name}"
    content = f"""
    <h3>收到新的在线咨询</h3>
    <p><strong>姓名:</strong> {name}</p>
    <p><strong>邮箱:</strong> {email}</p>
    <p><strong>咨询内容:</strong></p>
    <div style="background: #f4f4f5; padding: 15px; border-radius: 5px; margin-top: 10px;">
        {message}
    </div>
    <p style="color: #999; font-size: 12px; margin-top: 20px;">请及时在后台进行处理回复。</p>
    """
    # 发送给管理员 (这里配置为您的邮箱)
    admin_email = "15968588744@163.com"
    try:
        email_service.send_email([admin_email], subject, content)
        logger.info(f"Contact notification email sent to {admin_email}")
    except Exception as e:
        logger.error(f"Failed to send contact notification email: {e}")

