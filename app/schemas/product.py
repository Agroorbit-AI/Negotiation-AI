from pydantic import BaseModel
from uuid import UUID


class ProductCreate(BaseModel):
    name: str
    category: str
    base_price: float
    floor_price: float
    max_discount_percent: float
    unit: str


class ProductResponse(BaseModel):
    id: UUID
    name: str
    category: str
    base_price: float
    unit: str

    class Config:
        from_attributes = True
