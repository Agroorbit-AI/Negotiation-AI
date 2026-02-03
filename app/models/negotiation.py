import uuid
import enum
from sqlalchemy import Column, DateTime, ForeignKey, Enum as SQLEnum, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


# ------------------ ENUMS ------------------

class SessionStatus(str, enum.Enum):
    active = "active"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"


class ChannelEnum(str, enum.Enum):
    web = "web"
    whatsapp = "whatsapp"
    telecalling = "telecalling"


# ------------------ MODEL ------------------

class NegotiationSession(Base):
    __tablename__ = "negotiation_sessions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    customer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False
    )

    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False
    )

    # 🔥 ORM RELATIONSHIPS (THIS FIXES YOUR ERROR)
    customer = relationship("Customer", backref="negotiation_sessions")
    product = relationship("Product", backref="negotiation_sessions")

    channel = Column(
        SQLEnum(ChannelEnum, name="channelenum"),
        nullable=False
    )

    status = Column(
        SQLEnum(SessionStatus, name="sessionstatus"),
        nullable=False,
        default=SessionStatus.active
    )

    # ---------------- AGREEMENT DATA ----------------

    final_price = Column(
        Float,
        nullable=True
    )

    agreed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    agreement_channel = Column(
        SQLEnum(ChannelEnum, name="agreementchannelenum"),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
