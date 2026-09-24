import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.database import Attacker, AttackSession

def get_or_create_session(db: Session, source_ip: str, user_agent: Optional[str] = None, session_id: Optional[str] = None) -> Attacker:
    """Finds existing session by session_id or creates a new one."""
    if session_id:
        attacker = db.query(Attacker).filter(Attacker.session_id == session_id).first()
        if attacker:
            attacker.last_seen = datetime.utcnow()
            db.commit()
            return attacker

    # Create new session
    new_id = session_id or str(uuid.uuid4())
    attacker = Attacker(
        session_id=new_id,
        source_ip=source_ip,
        user_agent=user_agent or "Unknown",
        first_seen=datetime.utcnow(),
        last_seen=datetime.utcnow(),
        risk_score=0.0,
        behavior_type="RECONNAISSANCE",
        status="active"
    )
    db.add(attacker)

    attack_session = AttackSession(
        session_id=new_id,
        started_at=datetime.utcnow(),
        risk_score=0.0,
        attack_stage="RECONNAISSANCE",
        total_events=0,
        suspicious_events=0,
        lures_generated=0,
        lures_interacted=0
    )
    db.add(attack_session)

    db.commit()
    db.refresh(attacker)
    return attacker

def get_all_sessions(db: Session, page: int = 1, size: int = 20) -> List[Attacker]:
    return db.query(Attacker).order_by(Attacker.last_seen.desc()).offset((page - 1) * size).limit(size).all()

def get_session_detail(db: Session, session_id: str) -> Optional[Attacker]:
    return db.query(Attacker).filter(Attacker.session_id == session_id).first()
