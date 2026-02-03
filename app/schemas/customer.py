from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class CustomerCreate(BaseModel):
    name: str
    phone_number: str
    language: str


class CustomerOut(BaseModel):
    id: UUID
    name: str
    phone_number: str
    language_preference: str
    created_at: datetime

    class Config:
        from_attributes = True
