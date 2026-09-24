from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.schemas import RiskAssessment
from app.models.database import Attacker, AttackSession
from app.services.detection.scoring_engine import calculate_risk_level, LURE_GENERATION_TRIGGER_SCORE

router = APIRouter(prefix="/risk", tags=["Risk"])

@router.get("/{session_id}", response_model=RiskAssessment)
def get_risk_assessment(session_id: str, db: Session = Depends(get_db)):
    attacker = db.query(Attacker).filter(Attacker.session_id == session_id).first()
    if not attacker:
        raise HTTPException(status_code=404, detail="Session not found")

    attack_session = db.query(AttackSession).filter(AttackSession.session_id == session_id).first()
    attack_stage = attack_session.attack_stage if attack_session else "RECONNAISSANCE"
    risk_level = calculate_risk_level(attacker.risk_score)

    return RiskAssessment(
        session_id=session_id,
        risk_score=attacker.risk_score,
        risk_level=risk_level,
        attack_stage=attack_stage,
        behavior_type=attacker.behavior_type,
        score_breakdown={"cumulative_score": attacker.risk_score},
        should_generate_lure=attacker.risk_score >= LURE_GENERATION_TRIGGER_SCORE
    )
