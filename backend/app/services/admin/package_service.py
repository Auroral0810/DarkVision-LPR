from sqlalchemy.orm import Session, joinedload
from typing import List, Optional, Any
from app.models.payment import Package, PackageFeature
from app.models.marketing import Promotion
from app.schemas.admin.package import PackageCreate, PackageUpdate, PromotionCreate, PackageOut, PromotionOut
from datetime import datetime
import json
from app.core.redis import redis_client
from app.core.logger import logger

CACHE_KEY_PACKAGES = "admin:packages:list"
CACHE_KEY_PROMOTIONS = "admin:promotions:list"
CACHE_EXPIRE_SECONDS = 3600

class PackageService:
    def _clear_cache(self, keys: List[str] = None):
        """清除 Redis 缓存"""
        if not redis_client:
            return
        
        keys_to_delete = keys or [CACHE_KEY_PACKAGES, CACHE_KEY_PROMOTIONS]
        try:
            # redis-py's delete accepts variable arguments
            redis_client.delete(*keys_to_delete)
            logger.info(f"Cleared cache keys: {keys_to_delete}")
        except Exception as e:
            logger.error(f"Failed to clear cache: {e}")

    def get_packages(self, db: Session) -> List[Any]:
        """获取套餐列表（带缓存）"""
        # 1. Try Cache
        if redis_client:
            try:
                cached = redis_client.get(CACHE_KEY_PACKAGES)
                if cached:
                    logger.info("Cache hit for packages")
                    return json.loads(cached)
            except Exception as e:
                logger.error(f"Redis get failed: {e}")

        # 2. Query DB
        pkgs = db.query(Package).options(
            joinedload(Package.features),
            joinedload(Package.promotions)
        ).order_by(Package.id.asc()).all()
        
        # 3. Serialize to list of dicts
        # Use Pydantic to ensure consistency and handle datetime/decimal serialization
        serialized = [PackageOut.model_validate(p).model_dump(mode='json') for p in pkgs]

        # 4. Set Cache
        if redis_client:
            try:
                redis_client.setex(CACHE_KEY_PACKAGES, CACHE_EXPIRE_SECONDS, json.dumps(serialized))
            except Exception as e:
                logger.error(f"Redis set failed: {e}")
                
        return serialized

    def create_package(self, db: Session, pkg_data: PackageCreate) -> Package:
        """创建套餐并刷新缓存"""
        new_pkg = Package(
            name=pkg_data.name,
            code=pkg_data.code,
            price=pkg_data.price,
            duration_months=pkg_data.duration_months,
            description=pkg_data.description,
            is_active=pkg_data.is_active
        )
        db.add(new_pkg)
        db.flush() # Get ID
        
        if pkg_data.features:
            for feature in pkg_data.features:
                new_feature = PackageFeature(
                    package_id=new_pkg.id,
                    feature_key=feature.feature_key,
                    feature_display_name=feature.feature_display_name,
                    feature_description=feature.feature_description,
                    feature_value=feature.feature_value
                )
                db.add(new_feature)
        
        db.commit()
        db.refresh(new_pkg)
        self._clear_cache([CACHE_KEY_PACKAGES])
        return new_pkg

    def update_package(self, db: Session, package_id: int, pkg_data: PackageUpdate) -> Optional[Package]:
        """更新套餐并刷新缓存"""
        pkg = db.query(Package).filter(Package.id == package_id).first()
        if not pkg:
            return None
        
        # Update fields
        for field, value in pkg_data.model_dump(exclude_unset=True, exclude={'features'}).items():
            setattr(pkg, field, value)
        
        # Update features if provided
        if pkg_data.features is not None:
            db.query(PackageFeature).filter(PackageFeature.package_id == package_id).delete()
            for feature in pkg_data.features:
                new_feature = PackageFeature(
                    package_id=package_id,
                    feature_key=feature.feature_key,
                    feature_display_name=feature.feature_display_name,
                    feature_description=feature.feature_description,
                    feature_value=feature.feature_value
                )
                db.add(new_feature)
        
        db.commit()
        db.refresh(pkg)
        self._clear_cache([CACHE_KEY_PACKAGES])
        return pkg

    def get_promotions(self, db: Session) -> List[Any]:
        """获取促销列表（带缓存）"""
        if redis_client:
            try:
                cached = redis_client.get(CACHE_KEY_PROMOTIONS)
                if cached: 
                    logger.info("Cache hit for promotions")
                    return json.loads(cached)
            except Exception as e:
                logger.error(f"Redis get failed: {e}")

        promos = db.query(Promotion).all()
        serialized = [PromotionOut.model_validate(p).model_dump(mode='json') for p in promos]
        
        if redis_client:
            try:
                redis_client.setex(CACHE_KEY_PROMOTIONS, CACHE_EXPIRE_SECONDS, json.dumps(serialized))
            except Exception as e:
                logger.error(f"Redis set failed: {e}")

        return serialized

    def create_promotion(self, db: Session, promo_data: PromotionCreate) -> Promotion:
        """创建促销并刷新缓存"""
        new_promo = Promotion(
            name=promo_data.name,
            package_id=promo_data.package_id,
            discount_rate=promo_data.discount_rate,
            start_time=promo_data.start_time,
            end_time=promo_data.end_time,
            is_active=promo_data.is_active
        )
        db.add(new_promo)
        db.commit()
        db.refresh(new_promo)
        # 促销信息可能影响套餐显示，两者都清除
        self._clear_cache([CACHE_KEY_PROMOTIONS, CACHE_KEY_PACKAGES])
        return new_promo

    def get_package_features(self, db: Session, package_id: int) -> List[PackageFeature]:
        return db.query(PackageFeature).filter(PackageFeature.package_id == package_id).all()

    def update_package_features(self, db: Session, package_id: int, feature_data: list) -> List[PackageFeature]:
        """单独更新套餐权益并刷新缓存"""
        db.query(PackageFeature).filter(PackageFeature.package_id == package_id).delete()
        for f in feature_data:
            # Handle potential dict or object
            key = getattr(f, 'feature_key', None) or (f.get('feature_key') if isinstance(f, dict) else None)
            val = getattr(f, 'feature_value', None) or (f.get('feature_value') if isinstance(f, dict) else None)
            name = getattr(f, 'feature_display_name', None) or (f.get('feature_display_name') if isinstance(f, dict) else None)
            desc = getattr(f, 'feature_description', None) or (f.get('feature_description') if isinstance(f, dict) else None)
            
            if key and val:
                new_f = PackageFeature(
                    package_id=package_id,
                    feature_key=key,
                    feature_display_name=name,
                    feature_description=desc,
                    feature_value=str(val) # Ensure string
                )
                db.add(new_f)
        db.commit()
        self._clear_cache([CACHE_KEY_PACKAGES])
        return self.get_package_features(db, package_id)

package_service = PackageService()
