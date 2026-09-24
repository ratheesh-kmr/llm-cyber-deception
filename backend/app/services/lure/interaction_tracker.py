from datetime import datetime
from sqlalchemy.orm import Session
from app.models.database import LureInteraction, Attacker, AttackSession
from app.services.detection.scoring_engine import calculate_risk_level
from app.services.detection.stage_tracker import determine_attack_stage

def record_interaction(db: Session, lure_id: str, session_id: str, interaction_type: str = "VIEW", metadata: dict = None) -> LureInteraction:
    """Records an interaction with a deployed lure and updates attacker risk score."""
    interaction = LureInteraction(
        lure_id=lure_id,
        session_id=session_id,
        interaction_type=interaction_type,
        timestamp=datetime.utcnow(),
        metadata_=metadata or {}
    )
    db.add(interaction)

    # Boost risk score by 5 points on lure interaction
    attacker = db.query(Attacker).filter(Attacker.session_id == session_id).first()
    if attacker:
        attacker.risk_score += 5.0
        attacker.last_seen = datetime.utcnow()
        db.add(attacker)

    attack_session = db.query(AttackSession).filter(AttackSession.session_id == session_id).first()
    if attack_session:
        attack_session.risk_score += 5.0
        attack_session.lures_interacted += 1
        attack_session.attack_stage = "LURE_INTERACTION"
        db.add(attack_session)

    db.commit()
    db.refresh(interaction)
    return interaction
