from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.response import success, UnifiedResponse
from app.core.security import decode_access_token
from app.schemas.user import UserProfileUpdate, UserDetailInfo, PasswordChange, RealNameVerificationSubmit
from app.services.auth import (
    get_user_by_id,
    update_user_profile,
    get_user_detail_info,
    update_password,
    submit_real_name_verification,
    withdraw_real_name_verification
)
from app.core.exceptions import UnauthorizedException, TokenInvalidException

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """从token中获取当前用户ID"""
    payload = decode_access_token(token)
    if not payload:
        raise TokenInvalidException()
    
    user_id = payload.get("user_id")
    if not user_id:
        raise UnauthorizedException()
    
    return user_id


@router.put("/profile", response_model=UnifiedResponse[UserDetailInfo], summary="更新用户基本信息", tags=["用户"])
def update_profile(
    profile_data: UserProfileUpdate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    更新当前用户的基本信息
    
    可更新字段：
    - **nickname**: 昵称（2-50字符）
    - **avatar_url**: 头像URL（OSS地址）
    - **gender**: 性别（male/female/unknown）
    - **birthday**: 生日（YYYY-MM-DD格式）
    - **address**: 地址（省/市/区/详细地址）
    
    **注意**：
    - 昵称必须全局唯一
    - 头像URL应为OSS上传后返回的URL
    - 更新后会自动清除用户信息缓存
    """
    # 构建更新数据字典（只包含非None的字段）
    update_data = {}
    if profile_data.nickname is not None:
        update_data['nickname'] = profile_data.nickname
    if profile_data.avatar_url is not None:
        update_data['avatar_url'] = profile_data.avatar_url
    if profile_data.gender is not None:
        update_data['gender'] = profile_data.gender
    if profile_data.birthday is not None:
        update_data['birthday'] = profile_data.birthday
    if profile_data.address is not None:
        update_data['address'] = profile_data.address
    
    # 更新用户信息
    update_user_profile(db, user_id, update_data)
    
    # 获取更新后的用户详细信息
    user_detail = get_user_detail_info(db, user_id)
    
    return success(
        data=user_detail.model_dump(mode='json'),
        message="更新成功"
    )


@router.put("/password", response_model=UnifiedResponse, summary="修改登录密码", tags=["用户"])
def change_password(
    password_data: PasswordChange,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    修改当前用户的登录密码
    
    需要提供：
    - **old_password**: 旧密码
    - **new_password**: 新密码（6-20字符）
    - **confirm_password**: 确认新密码
    
    修改成功后，所有设备将强制下线，需使用新密码重新登录。
    """
    update_password(db, user_id, password_data)
    
    return success(message="密码修改成功，请重新登录")

@router.post("/verify", response_model=UnifiedResponse, summary="提交实名认证", tags=["用户"])
def verify_real_name(
    verify_data: RealNameVerificationSubmit,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    提交实名认证申请
    
    1. 调用第三方接口核验姓名和身份证号
    2. 核验通过后，记录申请信息等待管理员人工审核照片
    3. 如果核验失败，直接返回失败原因
    """
    submit_real_name_verification(db, user_id, verify_data)
    return success(message="实名认证已经提交，请等待管理员审核照片")

@router.post("/verify/withdraw", response_model=UnifiedResponse, summary="撤回实名认证申请", tags=["用户"])
def withdraw_verification(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    撤回正在审核中的实名认证申请
    """
    withdraw_real_name_verification(db, user_id)
    return success(message="申请已成功撤回")
