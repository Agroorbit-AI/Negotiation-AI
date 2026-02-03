from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID


# -------------------------
# CONTEXT OBJECTS
# -------------------------

class ProductContext(BaseModel):
    product_id: UUID
    name: str
    category: str
    unit: str
    base_price: float
    floor_price: float
    max_discount_percent: float
    free_delivery: bool = True


class OfferContext(BaseModel):
    offered_price: float
    created_at: datetime


class MessageContext(BaseModel):
    sender: str
    content: str
    created_at: datetime


class CustomerPurchaseHistory(BaseModel):
    last_price: Optional[float] = None
    last_quantity: Optional[float] = None
    last_purchase_date: Optional[datetime] = None


# -------------------------
# AI INPUT
# -------------------------

class AINegotiationInput(BaseModel):
    session_id: UUID
    customer_id: UUID
    product: ProductContext
    customer_history: CustomerPurchaseHistory
    offers: List[OfferContext]
    messages: List[MessageContext]
    latest_offer: Optional[float] = None
    best_offer: Optional[float] = None
    total_attempts: int = 0


# -------------------------
# AI OUTPUT
# -------------------------

class AINegotiationDecision(BaseModel):
    decision_type: str  # accept | reject | counter
    counter_price: Optional[float] = None
    message_text: str
    confidence_score: Optional[float] = None
