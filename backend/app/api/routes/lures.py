from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.schemas import LureResponse, LureGenerateRequest, LureDeployRequest
from app.models.database import Lure, Attacker
from app.services.llm.generator import generate_lure
from app.services.lure.deployment_manager import deploy_lure

router = APIRouter(prefix="/lures", tags=["Lures"])

@router.get("", response_model=List[LureResponse])
def list_lures(db: Session = Depends(get_db)):
    return db.query(Lure).order_by(Lure.created_at.desc()).all()

@router.post("/generate", response_model=LureResponse)
def generate_lure_endpoint(payload: LureGenerateRequest, db: Session = Depends(get_db)):
    attacker = db.query(Attacker).filter(Attacker.session_id == payload.session_id).first()
    interest = payload.interest_override or (attacker.behavior_type.lower() if attacker and attacker.behavior_type else "reconnaissance")

    lure = generate_lure(db, session_id=payload.session_id, interest=interest)
    if not lure:
        raise HTTPException(status_code=500, detail="Failed to generate lure")
    return lure

@router.post("/{lure_id}/deploy", response_model=LureResponse)
def deploy_lure_endpoint(lure_id: str, payload: LureDeployRequest = None, db: Session = Depends(get_db)):
    custom_endpoint = payload.endpoint_path if payload else None
    lure = deploy_lure(db, lure_id, custom_endpoint=custom_endpoint)
    if not lure:
        raise HTTPException(status_code=404, detail="Lure not found")
    return lure

@router.get("/{lure_id}", response_model=LureResponse)
def get_lure(lure_id: str, db: Session = Depends(get_db)):
    lure = db.query(Lure).filter(Lure.lure_id == lure_id).first()
    if not lure:
        raise HTTPException(status_code=404, detail="Lure not found")
    return lure
