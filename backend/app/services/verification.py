from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from typing import Tuple, List, Optional
from datetime import datetime

from app.models.user import RealNameVerification, User, UserProfile
from app.schemas.admin.verification import VerificationListParams, VerificationListItem

class VerificationService:
    def list_verifications(self, db: Session, params: VerificationListParams) -> Tuple[List[RealNameVerification], int]:
        """
        管理员查询实名认证列表
        """
        query = db.query(RealNameVerification).join(RealNameVerification.user)
        
        # 预加载关联数据
        query = query.options(
            joinedload(RealNameVerification.user),
            joinedload(RealNameVerification.user).joinedload(User.profile)
        )
        
        # 筛选
        if params.status:
            query = query.filter(RealNameVerification.status == params.status)
            
        if params.keyword:
            keyword = f"%{params.keyword}%"
            query = query.filter(
                (User.nickname.ilike(keyword)) | 
                (User.phone.ilike(keyword)) |
                (User.email.ilike(keyword))
            )

        total = query.count()
        
        # 排序：待处理优先，然后按时间倒序
        if params.status == 'pending':
            query = query.order_by(RealNameVerification.created_at.asc())
        else:
            query = query.order_by(RealNameVerification.created_at.desc())
            
        items = query.offset((params.page - 1) * params.page_size)\
                     .limit(params.page_size).all()
        
        return items, total

    def audit_verification(self, db: Session, verification_id: int, admin_id: int, action: str, reason: Optional[str] = None) -> Optional[RealNameVerification]:
        """
        审核实名认证
        """
        verification = db.query(RealNameVerification).filter(RealNameVerification.id == verification_id).first()
        if not verification:
            return None
            
        if action == 'approve':
            verification.status = 'approved'
            verification.reject_reason = None
            # 同步更新 UserProfile 中的状态（如果有对应字段，这里假设 RealNameVerification 是主数据源）
             # 也可以选择在这里同步写入 UserProfile 的 real_name 和 id_card_number，但逻辑上应该是在申请时就写入或者 approved 后写入
            # 这里我们假设申请时数据在 Profile 或专门的申请表里。
            # 根据模型，RealNameVerification 没有存 real_name, id_card_number, 这些在 UserProfile.
            # 因此我们需要确保前端提交申请时更新了 UserProfile，或者我们从哪里获取这些信息？
            # 仔细查看模型：User.real_name_verification 关联 RealNameVerification
            # UserProfile 也有 real_name, id_card_number.
            # 审核通过后，通常不需要额外操作，因为业务逻辑会检查 user.is_verified
            pass
            
        elif action == 'reject':
            verification.status = 'rejected'
            verification.reject_reason = reason
        
        verification.reviewed_by = admin_id
        verification.reviewed_at = datetime.now()
        
        db.add(verification)
        db.commit()
        db.refresh(verification)
        
        # 审核后清除用户缓存，确保用户端刷新后能看到最新认证状态
        try:
            from app.services.auth import invalidate_user_cache
            invalidate_user_cache(verification.user_id)
        except Exception as e:
            # 记录错误但不阻塞返回
            from app.core.logger import logger
            logger.error(f"Failed to invalidate user cache for user {verification.user_id}: {e}")
            
        return verification
        
    def get_verification_detail(self, db: Session, verification_id: int) -> Optional[RealNameVerification]:
        return db.query(RealNameVerification).options(
            joinedload(RealNameVerification.user).joinedload(User.profile)
        ).filter(RealNameVerification.id == verification_id).first()

verification_service = VerificationService()
