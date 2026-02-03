import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.base import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String(100), nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    language_preference = Column(String(10), default="en")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
