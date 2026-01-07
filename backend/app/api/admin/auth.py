from fastapi import APIRouter, Depends, Request
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
    get_user_detail_info,
    create_user_token,
    logout_user,
    log_login_attempt
)
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
    """
    管理员登录接口（支持手机号或邮箱 + 密码）
    
    **请求参数**:
    - **account**: 手机号或邮箱
    - **password**: 密码
    - **captcha_code**: 图形验证码（可选，如果前端开启验证）
    - **captcha_key**: 图形验证码Key（可选）
    
    **返回数据**:
    - **access_token**: JWT访问令牌
    - **token_type**: 令牌类型（bearer）
    - **user_info**: 用户详细信息
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
            # 既不是手机也不是邮箱，可能是用户名？目前仅支持手机/邮箱
            # 如果支持用户名登录，这里可以扩展
            raise ParameterException("账号格式错误，请输入有效的手机号或邮箱")
            
        if not user:
            raise UnauthorizedException("账号或密码错误")
            
        user_id = user.id
        
        # 3. 检查用户状态
        check_user_status(user)
        
        # 4. 检查管理员权限
        # 允许 admin 和 enterprise 类型登录管理后台 (根据业务需求调整)
        # 假设只有 user_type='admin' 才能登录 admin-portal
        if user.user_type != 'admin':
             # 也可以允许 enterprise 用户登录，视具体需求
             # if user.user_type not in ['admin', 'enterprise']:
            raise UnauthorizedException("无权访问管理后台")
        
        # 5. 更新登录信息
        update_login_info(db, user, client_ip)
        
        # 6. 创建token
        access_token = create_user_token(user)
        
        # 7. 获取用户详细信息
        user_detail = get_user_detail_info(db, user.id)
        
        # 8. 记录成功登录日志
        log_login_attempt(db, user_id, client_ip, user_agent, success=True, account=account)
        
        return success(
            data={
                "access_token": access_token,
                "token_type": "bearer",
                "user_info": user_detail.model_dump(mode='json')
            },
            message="登录成功"
        )
        
    except (UnauthorizedException, ResourceNotFoundException, ParameterException) as e:
        # 业务异常直接抛出，但在抛出前记录失败日志
        failure_reason = str(e.detail if hasattr(e, 'detail') else e.message if hasattr(e, 'message') else str(e))
        # user_id might not be defined if user lookup failed, use None
        uid = locals().get('user_id', None)
        log_login_attempt(db, uid, client_ip, user_agent, success=False, failure_reason=failure_reason, account=account)
        raise e
    except Exception as e:
        # 系统未知异常
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
    
    需要在 Header 中携带 token:
    ```
    Authorization: Bearer <your_token>
    ```
    """
    user_detail = get_user_detail_info(db, current_user.id)
    
    return success(
        data=user_detail.model_dump(mode='json'),
        message="获取成功"
    )


@router.post("/logout", response_model=UnifiedResponse, summary="管理员登出", tags=["管理员-认证"])
def admin_logout(
    current_user: User = Depends(get_current_user),
):
    """
    管理员登出接口
    
    清除服务器端的token和用户信息缓存
    """
    logout_user(current_user.id)
    
    return success(message="登出成功")
