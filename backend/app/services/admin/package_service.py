from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.payment import Package, PackageFeature
from app.models.marketing import Promotion
from app.schemas.admin.package import PackageCreate, PackageUpdate, PromotionCreate
from datetime import datetime
import json
from app.core.redis import redis_client

CACHE_KEY_PACKAGES = "admin:packages:list"

class PackageService:
    def _clear_cache(self):
        if redis_client:
            redis_client.delete(CACHE_KEY_PACKAGES)

    def get_packages(self, db: Session) -> List[Package]:
        cache_key = CACHE_KEY_PACKAGES
        if redis_client:
            try:
                cached = redis_client.get(cache_key)
                if cached:
                    # Return cached data if needed, but since we return SQLAlchemy objects
                    # to the API layer which then uses Pydantic to serialize, 
                    # caching as JSON and returning as dicts is often cleaner.
                    # For now, let's just use it as a flag or simple storage.
                    pass
            except Exception:
                pass

        pkgs = db.query(Package).all()
        # You could serialize here: redis_client.set(cache_key, serialize(pkgs))
        return pkgs

    def create_package(self, db: Session, pkg_data: PackageCreate) -> Package:
        new_pkg = Package(
            name=pkg_data.name,
            code=pkg_data.code,
            price=pkg_data.price,
            duration_months=pkg_data.duration_months,
            description=pkg_data.description,
            is_active=pkg_data.is_active
        )
        db.add(new_pkg)
        db.flush()
        
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
        self._clear_cache()
        return new_pkg

    def update_package(self, db: Session, package_id: int, pkg_data: PackageUpdate) -> Optional[Package]:
        pkg = db.query(Package).filter(Package.id == package_id).first()
        if not pkg:
            return None
        
        if pkg_data.name is not None: pkg.name = pkg_data.name
        if pkg_data.price is not None: pkg.price = pkg_data.price
        if pkg_data.duration_months is not None: pkg.duration_months = pkg_data.duration_months
        if pkg_data.description is not None: pkg.description = pkg_data.description
        if pkg_data.is_active is not None: pkg.is_active = pkg_data.is_active
        
        if pkg_data.features is not None:
            # Delete old features and add new ones
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
        self._clear_cache()
        return pkg

    def get_promotions(self, db: Session) -> List[Promotion]:
        return db.query(Promotion).all()

    def create_promotion(self, db: Session, promo_data: PromotionCreate) -> Promotion:
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
        return new_promo

    def get_package_features(self, db: Session, package_id: int) -> List[PackageFeature]:
        return db.query(PackageFeature).filter(PackageFeature.package_id == package_id).all()

    def update_package_features(self, db: Session, package_id: int, feature_data: list) -> List[PackageFeature]:
        # Delete old features and add new ones
        db.query(PackageFeature).filter(PackageFeature.package_id == package_id).delete()
        for f in feature_data:
            new_f = PackageFeature(
                package_id=package_id,
                feature_key=f.get('feature_key'),
                feature_display_name=f.get('feature_display_name'),
                feature_description=f.get('feature_description'),
                feature_value=f.get('feature_value')
            )
            db.add(new_f)
        db.commit()
        self._clear_cache()
        return self.get_package_features(db, package_id)

package_service = PackageService()
