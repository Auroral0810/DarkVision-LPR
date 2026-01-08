from pydantic import BaseModel
from typing import Optional, Dict

class PackageOut(BaseModel):
    id: int
    name: str
    code: str
    price: float
    duration_months: Optional[int]
    description: Optional[str]
    features: Dict[str, str]

    class Config:
        from_attributes = True
