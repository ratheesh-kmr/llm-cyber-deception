from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.schemas import EventResponse, EventCreate
from app.services.event_service import log_event, get_events

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("", response_model=List[EventResponse])
def list_events(session_id: Optional[str] = None, page: int = 1, size: int = 50, db: Session = Depends(get_db)):
    return get_events(db, session_id=session_id, page=page, size=size)

@router.post("", response_model=EventResponse)
def create_event(payload: EventCreate, db: Session = Depends(get_db)):
    return log_event(
        db,
        session_id=payload.session_id,
        endpoint=payload.endpoint,
        method=payload.method,
        metadata=payload.metadata
    )
