from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.models.negotiation import (
    NegotiationSession,
    SessionStatus,
    ChannelEnum,
)
from app.schemas.negotiation import (
    NegotiationCreate,
    NegotiationResponse,
    NegotiationStatusUpdate,
)
from app.services.negotiation_state import transition_session_state

router = APIRouter(prefix="/negotiations", tags=["Negotiations"])


# --------------------------------
# Create Negotiation Session
# --------------------------------
@router.post("/", response_model=NegotiationResponse)
def start_negotiation(
    payload: NegotiationCreate,
    db: Session = Depends(get_db),
):
    session = NegotiationSession(
        customer_id=payload.customer_id,
        product_id=payload.product_id,
        channel=payload.channel,              # ✅ enum-safe
        status=SessionStatus.active,           # ✅ FIXED
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


# ------------------------------------
# Update Negotiation Session Status
# ------------------------------------
@router.patch(
    "/{session_id}/status",
    response_model=NegotiationResponse,
)
def update_negotiation_status(
    session_id: UUID,
    payload: NegotiationStatusUpdate,
    db: Session = Depends(get_db),
):
    """
    Transitions negotiation session state.

    Allowed transitions:
    - active -> completed
    - active -> cancelled
    """

    session = (
        db.query(NegotiationSession)
        .filter(NegotiationSession.id == session_id)
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Negotiation session not found",
        )

    # ✅ SINGLE SOURCE OF TRUTH FOR STATE CHANGES
    transition_session_state(session, payload.status)

    db.commit()
    db.refresh(session)

    return session
