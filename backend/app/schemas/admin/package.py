from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class FeatureItem(BaseModel):
    feature_key: str
    feature_value: str

class PackageBase(BaseModel):
    name: str
    code: str
    price: Decimal
    duration_months: Optional[int] = None
    description: Optional[str] = None
    is_active: bool = True

class PackageCreate(PackageBase):
    features: List[FeatureItem] = []

class PackageUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[Decimal] = None
    duration_months: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    features: Optional[List[FeatureItem]] = None

class PackageOut(PackageBase):
    id: int
    created_at: datetime
    features: List[FeatureItem] = []

    model_config = ConfigDict(from_attributes=True)

class PromotionBase(BaseModel):
    name: str
    package_id: int
    discount_rate: Decimal
    start_time: datetime
    end_time: datetime
    is_active: bool = True

class PackageFeatureUpdate(BaseModel):
    features: List[FeatureItem]

class PromotionCreate(PromotionBase):
    pass

class PromotionOut(PromotionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
