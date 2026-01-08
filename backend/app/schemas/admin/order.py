from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class OrderBase(BaseModel):
    order_no: str
    amount: Decimal
    status: str
    payment_method: Optional[str] = None

class OrderCreate(BaseModel):
    user_id: int
    package_id: int
    amount: Decimal
    status: str = "pending"
    payment_method: Optional[str] = None

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    payment_method: Optional[str] = None
    paid_at: Optional[datetime] = None

class OrderOut(OrderBase):
    id: int
    user_id: int
    package_id: int
    paid_at: Optional[datetime] = None
    created_at: datetime
    
    # Nested info
    nickname: Optional[str] = None
    package_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
