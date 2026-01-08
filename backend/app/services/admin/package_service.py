from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.payment import Package, PackageFeature
from app.models.marketing import Promotion
from app.schemas.admin.package import PackageCreate, PackageUpdate, PromotionCreate
from datetime import datetime

class PackageService:
    def get_packages(self, db: Session) -> List[Package]:
        return db.query(Package).all()

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
                feature_value=feature.feature_value
            )
            db.add(new_feature)
        
        db.commit()
        db.refresh(new_pkg)
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
                    feature_value=feature.feature_value
                )
                db.add(new_feature)
        
        db.commit()
        db.refresh(pkg)
        return pkg

    def get_promotions(self, db: Session) -> List[Promotion]:
        return db.query(Promotion).all()

    def create_promotion(self, db: Session, promo_data: PromotionCreate) -> Promotion:
        new_promo = Promotion(
            name=promo_data.name,
            package_id=promo_data.package_id,
            promotional_price=promo_data.promotional_price,
            start_time=promo_data.start_time,
            end_time=promo_data.end_time,
            is_active=promo_data.is_active
        )
        db.add(new_promo)
        db.commit()
        db.refresh(new_promo)
        return new_promo

package_service = PackageService()
