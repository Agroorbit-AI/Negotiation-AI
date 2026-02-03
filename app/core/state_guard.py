from fastapi import HTTPException

def ensure_active_session(session):
    if session.status != "active":
        raise HTTPException(
            status_code=400,
            detail=f"Session is {session.status}. Action not allowed."
        )
