from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class WebSessionStartRequest(BaseModel):
    name: str
    phone_number: str
    product_id: UUID
    language: Optional[str] = "en"

class WebSessionStartResponse(BaseModel):
    session_id: UUID
    customer_id: UUID
    product_id: UUID
    status: str
