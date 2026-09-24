from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.schemas import LureInteractionResponse
from app.models.database import LureInteraction

router = APIRouter(prefix="/interactions", tags=["Interactions"])

@router.get("", response_model=List[LureInteractionResponse])
def list_interactions(db: Session = Depends(get_db)):
    return db.query(LureInteraction).order_by(LureInteraction.timestamp.desc()).all()
