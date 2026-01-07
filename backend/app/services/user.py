from sqlalchemy.orm import Session
from app.models.user import User, UserProfile, UserMembership, RealNameVerification
from app.models.role import AdminRole, Role
from app.schemas.user import UserDetailInfo as UserDetail
from typing import Optional

def get_user_detail_info(db: Session, user_id: int) -> Optional[UserDetail]:
    """
    获取用户详细信息（包含角色、会员、认证等信息）
    """
    # Eagerly load admin_roles and associated role to prevent lazy loading issues
    from sqlalchemy.orm import joinedload
    user = db.query(User).options(
        joinedload(User.admin_roles).joinedload(AdminRole.role)
    ).filter(User.id == user_id).first()

    if not user:
        return None

    # 构建基础信息
    user_info = {
        "id": user.id,
        "phone": user.phone,
        "nickname": user.nickname,
        "email": user.email,
        "avatar_url": user.avatar_url,
        "user_type": user.user_type,
        "status": user.status,
        "created_at": user.created_at,
        "last_login_at": user.last_login_at,
        "roles": []  # 默认为空列表
    }

    # 获取角色信息 (如果是管理员)
    if user.user_type == 'admin':
        # 调试输出
        print(f"DEBUG: Checking roles for user {user_id}")
        import logging
        logger = logging.getLogger("darkvision")
        
        # 通过 AdminRole 关联查询角色名称
        # user.admin_roles 是 relationship 列表，每个元素是 AdminRole 对象，包含 role 对象
        roles = []
        if user.admin_roles:
            print(f"DEBUG: Found {len(user.admin_roles)} admin_roles entries")
            for ar in user.admin_roles:
                print(f"DEBUG: Processing AdminRole: {ar}, Role: {ar.role}")
                if ar.role:
                    roles.append(ar.role.name)
                else:
                    logger.warning(f"AdminRole found but no Role associated for user {user_id}")
        else:
             print("DEBUG: No admin_roles found (empty list)")

        # 如果没有分配具体角色但类型是admin，赋予默认ROOT角色作为容错（可选）
        if not roles:
            print("DEBUG: No specific roles found, defaulting to ROOT")
            roles = ["ROOT"]
            
        user_info["roles"] = roles
    else:
        # 普通用户无特定管理角色
        user_info["roles"] = []

    # 获取会员信息
    if user.membership:
        user_info.update({
            "membership_type": user.membership.membership_type,
            "membership_expire_date": user.membership.expire_date,
            "is_membership_active": bool(user.membership.is_active)
        })

    # 获取个人资料
    if user.profile:
        user_info.update({
            "gender": user.profile.gender,
            "birthday": user.profile.birthday,
            "address": user.profile.address,
            "real_name": user.profile.real_name
        })
        
    # 获取实名认证状态
    if user.real_name_verification:
        user_info.update({
            "is_verified": user.real_name_verification.status == 'approved',
            "verification_status": user.real_name_verification.status,
            "reject_reason": user.real_name_verification.reject_reason,
            "id_card_front": user.real_name_verification.id_card_front,
            "id_card_back": user.real_name_verification.id_card_back,
            "face_photo": user.real_name_verification.face_photo
        })
    else:
         user_info.update({
            "is_verified": False,
            "verification_status": None
        })

    # 填充配额信息 (根据业务逻辑，这里暂给默认值或查询配额表)
    # 假设每日限额存储在 SubAccount 或者其他配置表中，这里简化处理
    user_info.update({
        "daily_quota": 999999, # 示例
        "used_quota_today": 0,
        "remaining_quota_today": 999999
    })

    return UserDetail(**user_info)


from app.schemas.admin.user import AdminSelfInfo

def get_admin_detail_info(db: Session, user_id: int) -> Optional[AdminSelfInfo]:
    """
    获取管理员详细信息（仅包含角色等管理必要信息）
    """
    # Eagerly load admin_roles and associated role
    from sqlalchemy.orm import joinedload
    user = db.query(User).options(
        joinedload(User.admin_roles).joinedload(AdminRole.role)
    ).filter(User.id == user_id).first()

    if not user:
        return None
        
    roles = []
    if user.user_type == 'admin':
        if user.admin_roles:
            for ar in user.admin_roles:
                if ar.role:
                    roles.append(ar.role.name)
        
        # 容错：如果admin类型但无角色，给空列表或默认值，这里给空列表让前端处理权限拒绝，或者给ROOT方便调试
        # 根据用户需求，数据库已有角色，所以这里应该能查到
        if not roles:
            # 只有当确实没查到角色时，才（可选地）给一个默认值
            # roles = ["ROOT"] 
            pass
            
    return AdminSelfInfo(
        id=user.id,
        phone=user.phone,
        nickname=user.nickname,
        email=user.email,
        avatar_url=user.avatar_url,
        user_type=user.user_type,
        status=user.status,
        roles=roles,
        created_at=user.created_at,
        last_login_at=user.last_login_at
    )
