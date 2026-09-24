from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.schemas import SessionResponse, SessionDetailResponse, SessionCreate
from app.services.session_service import get_or_create_session, get_all_sessions, get_session_detail

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.get("", response_model=List[SessionResponse])
def list_sessions(page: int = 1, size: int = 20, db: Session = Depends(get_db)):
    return get_all_sessions(db, page, size)

@router.post("", response_model=SessionResponse)
def create_session(payload: SessionCreate, db: Session = Depends(get_db)):
    return get_or_create_session(db, source_ip=payload.source_ip, user_agent=payload.user_agent)

@router.get("/{session_id}", response_model=SessionDetailResponse)
def get_session(session_id: str, db: Session = Depends(get_db)):
    session = get_session_detail(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
