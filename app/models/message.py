import uuid
from sqlalchemy import Column, DateTime, ForeignKey, Text, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class ConversationMessage(Base):
    __tablename__ = "conversation_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    negotiation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("negotiation_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    sender = Column(String(20), nullable=False)

    message = Column(Text, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    negotiation = relationship(
        "NegotiationSession",
        backref="messages",
        lazy="joined",
    )