from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.base import Base  # ✅ correct base import


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

    # ✅ FIX: category is now plain STRING (no enum)
    category = Column(String, nullable=False)

    base_price = Column(Float, nullable=False)
    floor_price = Column(Float, nullable=False)
    max_discount_percent = Column(Float, nullable=False)

    # ✅ keep unit simple too (string is safest)
    unit = Column(String, nullable=False)
