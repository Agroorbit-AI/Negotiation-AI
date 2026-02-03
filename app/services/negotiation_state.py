from fastapi import HTTPException, status
from app.models.negotiation import SessionStatus, NegotiationSession


ALLOWED_TRANSITIONS = {
    SessionStatus.active: {
        SessionStatus.completed,
        SessionStatus.cancelled,
    },
    SessionStatus.completed: set(),
    SessionStatus.cancelled: set(),
}


def transition_session_state(
    session: NegotiationSession,
    new_status: SessionStatus,
):
    current_status = session.status

    if new_status == current_status:
        return  # no-op allowed

    allowed = ALLOWED_TRANSITIONS.get(current_status, set())

    if new_status not in allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status transition: {current_status.value} → {new_status.value}",
        )

    session.status = new_status
