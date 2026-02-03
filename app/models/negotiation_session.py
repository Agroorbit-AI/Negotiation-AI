from sqlalchemy import Column, ForeignKey, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from db.base import Base
from enums.session_status import SessionStatus


class NegotiationSession(Base):
    __tablename__ = "negotiation_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)

    status = Column(
        Enum(SessionStatus, name="sessionstatus"),
        nullable=False,
        default=SessionStatus.active,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
