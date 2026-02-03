from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from enum import Enum
from app.models.negotiation import SessionStatus

class ChannelEnum(str, Enum):
    web = "web"
    whatsapp = "whatsapp"
    telecalling = "telecalling"

class NegotiationCreate(BaseModel):
    customer_id: UUID
    product_id: UUID
    channel: str = Field(default="web", example="web")

class NegotiationStatusUpdate(BaseModel):
    status: SessionStatus

class NegotiationResponse(BaseModel):
    id: UUID
    customer_id: UUID
    product_id: UUID
    channel: ChannelEnum
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
