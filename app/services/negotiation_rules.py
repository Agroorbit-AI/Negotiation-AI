# app/services/negotiation_rules.py

from app.models.negotiation import SessionStatus

ALLOWED_TRANSITIONS = {
    SessionStatus.active: {
        SessionStatus.completed,
        SessionStatus.cancelled,
    },
    SessionStatus.completed: set(),
    SessionStatus.cancelled: set(),
}


def validate_status_transition(current, new):
    if new not in ALLOWED_TRANSITIONS[current]:
        raise ValueError(
            f"Invalid transition from {current.value} → {new.value}"
        )
