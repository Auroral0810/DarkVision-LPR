from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.response import UnifiedResponse, success_response, error_response
from app.services.admin.package_service import package_service
from app.schemas.admin.package import (
    PackageOut, PackageCreate, PackageUpdate, 
    PromotionOut, PromotionCreate, FeatureItem, PackageFeatureUpdate
)

router = APIRouter()

@router.get("/packages", response_model=UnifiedResponse[List[PackageOut]])
def get_packages(db: Session = Depends(get_db)):
    pkgs = package_service.get_packages(db)
    return success_response(data=pkgs)

@router.post("/packages", response_model=UnifiedResponse)
def create_package(pkg_data: PackageCreate, db: Session = Depends(get_db)):
    pkg = package_service.create_package(db, pkg_data)
    return success_response(data={"id": pkg.id}, message="套餐创建成功")

@router.put("/packages/{package_id}", response_model=UnifiedResponse)
def update_package(package_id: int, pkg_data: PackageUpdate, db: Session = Depends(get_db)):
    pkg = package_service.update_package(db, package_id, pkg_data)
    if not pkg:
        return error_response(message="套餐未找到")
    return success_response(message="套餐更新成功")

@router.get("/promotions", response_model=UnifiedResponse[List[PromotionOut]])
def get_promotions(db: Session = Depends(get_db)):
    promos = package_service.get_promotions(db)
    return success_response(data=promos)

@router.post("/promotions", response_model=UnifiedResponse)
def create_promotion(promo_data: PromotionCreate, db: Session = Depends(get_db)):
    promo = package_service.create_promotion(db, promo_data)
    return success_response(data={"id": promo.id}, message="活动创建成功")

@router.get("/packages/{package_id}/features", response_model=UnifiedResponse[List[FeatureItem]])
def get_package_features(package_id: int, db: Session = Depends(get_db)):
    features = package_service.get_package_features(db, package_id)
    return success_response(data=features)

@router.put("/packages/{package_id}/features", response_model=UnifiedResponse)
def update_package_features(package_id: int, feature_data: PackageFeatureUpdate, db: Session = Depends(get_db)):
    package_service.update_package_features(db, package_id, feature_data.features)
    return success_response(message="套餐权益更新成功")
