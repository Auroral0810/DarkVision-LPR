from fastapi import APIRouter, Depends, Request
import time, json
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.response import success, UnifiedResponse
from app.core.security import decode_access_token
from app.schemas.user import UserLoginGeneric, UserLoginByPhone, UserLoginByEmail
from app.services.auth import (
    authenticate_by_phone_password,
    authenticate_by_email_password,
    check_user_status,
    update_login_info,
    create_user_token,
    logout_user,
    log_login_attempt
)
from app.services import log_service
from app.services.user import get_admin_detail_info # New import
from app.services.captcha import captcha_service
from app.core.exceptions import ParameterException, UnauthorizedException, ResourceNotFoundException
from app.api.deps import get_current_user
from app.models.user import User
import re

router = APIRouter()


@router.post("/login", response_model=UnifiedResponse, summary="管理员登录", tags=["管理员-认证"])
def admin_login(
    login_data: UserLoginGeneric,
    request: Request,
    db: Session = Depends(get_db)
):
    t1 = time.time()
    """
    管理员登录接口（支持手机号或邮箱 + 密码）
    """
    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent", "")
    user_id = None
    account = login_data.account
    
    # 1. 验证图形验证码 (如果提供了)
    if login_data.captcha_code and login_data.captcha_key:
        is_valid = captcha_service.verify_captcha(login_data.captcha_key, login_data.captcha_code)
        if not is_valid:
            raise ParameterException("验证码错误或已过期")
    
    try:
        # 2. 判断账号类型 (手机号/邮箱)
        # 简单的正则判断
        phone_pattern = r"^1[3-9]\d{9}$"
        email_pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        
        user = None
        
        if re.match(phone_pattern, account):
            # 手机号登录
            login_req = UserLoginByPhone(phone=account, password=login_data.password)
            user = authenticate_by_phone_password(db, login_req)
        elif re.match(email_pattern, account):
            # 邮箱登录
            login_req = UserLoginByEmail(email=account, password=login_data.password)
            user = authenticate_by_email_password(db, login_req)
        else:
            # 既不是手机也不是邮箱
            raise ParameterException("账号格式错误，请输入有效的手机号或邮箱")
            
        if not user:
            raise UnauthorizedException("账号或密码错误")
            
        user_id = user.id
        
        # 3. 检查用户状态
        check_user_status(user)
        
        # 4. 检查管理员权限
        if user.user_type != 'admin':
            raise UnauthorizedException("无权访问管理后台")
        
        # 5. 更新登录信息
        update_login_info(db, user, client_ip)
        
        # 6. 创建token
        access_token = create_user_token(user)
        
        # 7. 获取管理员详细信息 (使用新服务)
        user_detail = get_admin_detail_info(db, user.id)
        
        # 9. 记录成功统计
        try:
            from app.services.visit_statistics_service import record_page_view_log
            from app.models.statistics import PageType
            record_page_view_log(
                db=db,
                page_type=PageType.ADMIN,
                ip_address=client_ip,
                user_id=user_id,
                page_path="/api/admin/login",
                user_agent=user_agent
            )
        except Exception as e:
            from app.core.logger import logger
            logger.error(f"Failed to record admin login stats: {e}")
            
        t2 = time.time()
        res_data = {
            "access_token": access_token,
            "token_type": "bearer",
            "user_info": user_detail.model_dump(mode='json')
        }
        log_result = {
            "code": 20000,
            "message": "登录成功",
            "data": res_data
        }
        
        log_service.create_log(
            db, user.id, "auth", "login", 
            f"Admin login success: {account}", request=request,
            duration=int((t2 - t1) * 1000), result=log_result
        )
        return success(data=res_data, message="登录成功")
        
    except (UnauthorizedException, ResourceNotFoundException, ParameterException) as e:
        failure_reason = str(e.detail if hasattr(e, 'detail') else e.message if hasattr(e, 'message') else str(e))
        uid = locals().get('user_id', None)
        log_login_attempt(db, uid, client_ip, user_agent, success=False, failure_reason=failure_reason, account=account)
        raise e
    except Exception as e:
        failure_reason = f"System Error: {str(e)}"
        uid = locals().get('user_id', None)
        log_login_attempt(db, uid, client_ip, user_agent, success=False, failure_reason=failure_reason, account=account)
        raise e


@router.get("/me", response_model=UnifiedResponse, summary="获取当前管理员信息", tags=["管理员-认证"])
def get_admin_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取当前登录管理员信息
    """
    user_detail = get_admin_detail_info(db, current_user.id)
    
    return success(
        data=user_detail.model_dump(mode='json'),
        message="获取成功"
    )


@router.post("/logout", response_model=UnifiedResponse, summary="管理员登出", tags=["管理员-认证"])
def admin_logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    管理员登出接口
    
    清除服务器端的token、用户信息缓存和在线状态
    """
    t1 = time.time()
    logout_user(current_user.id)
    t2 = time.time()
    
    log_result = {
        "code": 20000,
        "message": "登出成功",
        "data": None
    }
    
    log_service.create_log(
        db, current_user.id, "auth", "logout", 
        f"Admin logout: {current_user.phone}", request=request,
        duration=int((t2 - t1) * 1000), result=log_result
    )
    
    return success(message="登出成功")
