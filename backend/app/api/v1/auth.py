from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.response import success, success_created, UnifiedResponse
from app.core.codes import ResponseCode
from app.core.security import decode_access_token
from app.schemas.user import (
    UserRegister, UserLoginByPhone, UserLoginByEmail,
    SMSCodeRequest, EmailCodeRequest, LoginResponse
)
from app.schemas.password import ResetPasswordRequest
from app.services.auth import (
    register_user,
    authenticate_by_phone_password,
    authenticate_by_phone_code,
    authenticate_by_email_password,
    authenticate_by_email_code,
    check_user_status,
    update_login_info,
    get_user_detail_info,
    create_user_token,
    get_user_by_id,
    logout_user,
    reset_password,
    log_login_attempt
)
from app.services.verification import verification_service
from app.core.exceptions import UnauthorizedException, TokenInvalidException, ParameterException
from app.api.deps import get_current_user as deps_get_current_user
from app.models.user import User

router = APIRouter()

# oauth2_scheme is now in deps.py, but for login/register we don't need it.
# We do need it for /me and /logout, but we can use deps_get_current_user for /me.
# For /logout, we can use the dependency too.

@router.post("/register", response_model=UnifiedResponse, summary="用户注册", tags=["认证"])
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    用户注册接口（支持手机号或邮箱）
    
    **注册流程**:
    1. 获取图形验证码 `/api/v1/captcha/generate`
    2. 验证图形验证码 `/api/v1/captcha/verify` (可选，通常前端做)
    3. 调用 `/api/v1/auth/sms/send` (手机) 或 `/api/v1/auth/email/send` (邮箱) 发送验证码
    4. 输入账号、验证码、昵称、密码进行注册
    
    **请求参数**:
    - **phone**: 手机号（可选，与邮箱二选一）
    - **sms_code**: 短信验证码（手机注册时必填）
    - **email**: 邮箱（可选，与手机二选一）
    - **email_code**: 邮箱验证码（邮箱注册时必填）
    - **nickname**: 昵称（2-50字符，全局唯一）
    - **password**: 密码（6-20字符）
    
    **说明**:
    - 注册成功后自动创建为 **FREE（普通）** 用户
    - 如果提供邮箱，会发送欢迎邮件
    - 验证码5分钟有效，使用后自动失效
    
    **示例请求**:
    ```json
    {
      "phone": "13800138000",
      "sms_code": "123456",
      "nickname": "新用户",
      "password": "123456"
    }
    ```
    或者
    ```json
    {
      "email": "user@example.com",
      "email_code": "123456",
      "nickname": "新用户",
      "password": "123456"
    }
    ```
    """
    user = register_user(db, user_data)
    user_detail = get_user_detail_info(db, user.id)
    
    return success_created(
        data=user_detail.model_dump(mode='json'),
        message="注册成功"
    )


@router.post("/login/phone", response_model=UnifiedResponse, summary="手机号登录", tags=["认证"])
def login_by_phone(
    login_data: UserLoginByPhone,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    手机号登录接口（支持密码和验证码两种方式）
    
    **方式一：手机号+密码**
    ```json
    {
      "phone": "13800138000",
      "password": "123456"
    }
    ```
    
    **方式二：手机号+验证码**
    ```json
    {
      "phone": "13800138000",
      "sms_code": "123456"
    }
    ```
    
    返回：
    - **access_token**: JWT访问令牌
    - **user_info**: 用户详细信息（包含会员状态、额度等）
    """
    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent", "")
    user_id = None
    account = login_data.phone
    
    try:
        # 判断使用哪种登录方式
        if login_data.password:
            user = authenticate_by_phone_password(db, login_data)
        elif login_data.sms_code:
            user = authenticate_by_phone_code(db, login_data)
        else:
            raise ParameterException("请提供密码或验证码")
        
        user_id = user.id
        
        # 检查用户状态
        check_user_status(user)
        
        # 更新登录信息
        update_login_info(db, user, client_ip)
        
        # 创建token
        access_token = create_user_token(user)
        
        # 获取用户详细信息
        user_detail = get_user_detail_info(db, user.id)
        
        # 记录成功登录日志
        # 记录成功统计
        try:
            from app.services.visit_statistics_service import record_page_view_log
            from app.models.statistics import PageType
            record_page_view_log(
                db=db,
                page_type=PageType.USER,
                ip_address=client_ip,
                user_id=user_id,
                page_path="/api/v1/auth/login",
                user_agent=user_agent
            )
        except Exception as e:
            from app.core.logger import logger
            logger.error(f"Failed to record login stats: {e}")

        
        return success(
            data={
                "access_token": access_token,
                "token_type": "bearer",
                "user_info": user_detail.model_dump(mode='json')
            },
            message="登录成功"
        )
    except Exception as e:
        # 记录失败登录日志
        failure_reason = str(e)
        log_login_attempt(db, user_id, client_ip, user_agent, success=False, failure_reason=failure_reason, account=account)
        raise


@router.post("/login/email", response_model=UnifiedResponse, summary="邮箱登录", tags=["认证"])
def login_by_email(
    login_data: UserLoginByEmail,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    邮箱登录接口（支持密码和验证码两种方式）
    
    **方式一：邮箱+密码**
    ```json
    {
      "email": "user@example.com",
      "password": "123456"
    }
    ```
    
    **方式二：邮箱+验证码**
    ```json
    {
      "email": "user@example.com",
      "email_code": "123456"
    }
    ```
    """
    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent", "")
    user_id = None
    account = login_data.email
    
    try:
        # 判断使用哪种登录方式
        if login_data.password:
            user = authenticate_by_email_password(db, login_data)
        elif login_data.email_code:
            user = authenticate_by_email_code(db, login_data)
        else:
            raise ParameterException("请提供密码或验证码")
        
        user_id = user.id
        
        # 检查用户状态
        check_user_status(user)
        
        # 更新登录信息
        update_login_info(db, user, client_ip)
        
        # 创建token
        access_token = create_user_token(user)
        
        # 获取用户详细信息
        user_detail = get_user_detail_info(db, user.id)
        
        # 记录成功登录日志
        # 记录成功统计
        try:
            from app.services.visit_statistics_service import record_page_view_log
            from app.models.statistics import PageType
            record_page_view_log(
                db=db,
                page_type=PageType.USER,
                ip_address=client_ip,
                user_id=user_id,
                page_path="/api/v1/auth/login",
                user_agent=user_agent
            )
        except Exception as e:
            from app.core.logger import logger
            logger.error(f"Failed to record login stats: {e}")

        
        return success(
            data={
                "access_token": access_token,
                "token_type": "bearer",
                "user_info": user_detail.model_dump(mode='json')
            },
            message="登录成功"
        )
    except Exception as e:
        # 记录失败登录日志
        failure_reason = str(e)
        log_login_attempt(db, user_id, client_ip, user_agent, success=False, failure_reason=failure_reason, account=account)
        raise


@router.post("/sms/send", response_model=UnifiedResponse, summary="发送短信验证码", tags=["认证"])
def send_sms_code(code_request: SMSCodeRequest):
    """
    发送短信验证码
    
    - **phone**: 手机号
    - **scene**: 使用场景（login/register/reset_password）
    
    **注意**：
    - 验证码有效期5分钟
    - 同一手机号1分钟内只能发送一次
    - 开发环境会在响应中返回验证码（生产环境不返回）
    """
    code = verification_service.send_sms_code(code_request.phone, code_request.scene)
    
    # 开发环境返回验证码，生产环境不返回
    return success(
        data={"code": code, "expire_seconds": 300},  # 生产环境删除 code 字段
        message="验证码已发送"
    )


@router.post("/email/send", response_model=UnifiedResponse, summary="发送邮箱验证码", tags=["认证"])
def send_email_code(code_request: EmailCodeRequest):
    """
    发送邮箱验证码
    
    - **email**: 邮箱
    - **scene**: 使用场景（login/register/reset_password）
    
    **注意**：
    - 验证码有效期5分钟
    - 同一邮箱1分钟内只能发送一次
    - 开发环境会在响应中返回验证码（生产环境不返回）
    """
    code = verification_service.send_email_code(code_request.email, code_request.scene)
    
    # 开发环境返回验证码，生产环境不返回
    return success(
        data={"code": code, "expire_seconds": 300},  # 生产环境删除 code 字段
        message="验证码已发送"
    )


@router.get("/me", response_model=UnifiedResponse, summary="获取当前用户信息", tags=["认证"])
def read_users_me(
    current_user: User = Depends(deps_get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取当前登录用户信息
    
    需要在 Header 中携带 token:
    ```
    Authorization: Bearer <your_token>
    ```
    
    返回用户详细信息，包括：
    - 基本信息（手机号、昵称、邮箱、头像等）
    - 会员信息（类型、到期时间）
    - 识别额度（每日额度、已用额度、剩余额度）
    - 实名认证状态
    - 企业信息（如果是企业用户）
    """
    # 获取用户详细信息（优先从缓存）
    user_detail = get_user_detail_info(db, current_user.id)
    
    return success(
        data=user_detail.model_dump(mode='json'),
        message="获取成功"
    )


@router.post("/logout", response_model=UnifiedResponse, summary="用户登出", tags=["认证"])
def logout(
    current_user: User = Depends(deps_get_current_user),
):
    """
    用户登出接口
    
    清除服务器端的token、用户信息缓存和在线状态
    """
    logout_user(current_user.id)
    
    return success(message="登出成功")


@router.post("/password/reset", response_model=UnifiedResponse, summary="重置密码", tags=["认证"])
def reset_password_endpoint(
    reset_data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    重置用户密码
    
    - **account**: 手机号或邮箱
    - **code**: 验证码（手机或邮箱）
    - **new_password**: 新密码
    - **confirm_password**: 确认新密码
    
    重置成功后，该用户的所有登录状态（Token）将失效，需重新登录。
    """
    reset_password(db, reset_data)
    
    return success(message="密码重置成功，请重新登录")
