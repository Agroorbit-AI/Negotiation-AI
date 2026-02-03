from enum import Enum


class SessionStatus(str, Enum):
    active = "active"
    completed = "completed"
    cancelled = "cancelled"
