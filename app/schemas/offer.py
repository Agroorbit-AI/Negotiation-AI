from uuid import UUID
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel


class OfferCreate(BaseModel):
    session_id: UUID
    customer_id: UUID
    offered_price: Decimal
    price: Decimal
    quantity: Decimal


class OfferResponse(BaseModel):
    id: UUID
    session_id: UUID
    customer_id: UUID
    offered_price: Decimal
    price: Decimal
    quantity: Decimal
    created_at: datetime

    class Config:
        from_attributes = True
