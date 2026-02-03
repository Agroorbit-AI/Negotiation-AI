from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class MessageCreate(BaseModel):
    session_id: UUID  # client still uses session_id
    sender: str
    message: str


class MessageResponse(BaseModel):
    id: UUID
    session_id: UUID  # map negotiation_id → session_id in response
    sender: str
    message: str
    created_at: datetime

    class Config:
        orm_mode = True
