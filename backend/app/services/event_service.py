from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app.models.database import Event, Attacker, AttackSession
from app.services.detection.suspicious_patterns import analyze_request
from app.services.detection.scoring_engine import evaluate_risk
from app.services.detection.interest_classifier import classify_interest
from app.services.llm.generator import generate_lure
from app.services.lure.deployment_manager import deploy_lure

def log_event(
    db: Session,
    session_id: str,
    endpoint: str,
    method: str,
    metadata: Optional[Dict[str, Any]] = None,
    source_ip: str = "127.0.0.1",
    user_agent: str = "Unknown"
) -> Event:
    """Logs HTTP event, evaluates risk score, updates session stage, and triggers lure generation if needed."""
    is_suspicious, risk_delta, event_type, desc = analyze_request(endpoint, method)
    severity = "CRITICAL" if risk_delta >= 4.0 else ("HIGH" if risk_delta >= 3.0 else ("MEDIUM" if risk_delta >= 2.0 else "LOW"))

    event = Event(
        session_id=session_id,
        event_type=event_type,
        endpoint=endpoint,
        method=method,
        timestamp=datetime.utcnow(),
        severity=severity,
        metadata_=metadata or {},
        is_suspicious=is_suspicious,
        risk_delta=risk_delta
    )
    db.add(event)

    # Update Attacker record
    attacker = db.query(Attacker).filter(Attacker.session_id == session_id).first()
    if attacker:
        current_score = attacker.risk_score
        all_events = db.query(Event).filter(Event.session_id == session_id).all()
        events_count = len(all_events) + 1
        attempted_login = any(e.event_type == "credential_attempt" for e in all_events) or (event_type == "credential_attempt")

        new_score, risk_level, attack_stage, should_gen_lure = evaluate_risk(
            current_score, risk_delta, events_count, attempted_login=attempted_login
        )

        attacker.risk_score = new_score
        attacker.last_seen = datetime.utcnow()

        # Update attack session summary
        attack_session = db.query(AttackSession).filter(AttackSession.session_id == session_id).first()
        if attack_session:
            attack_session.risk_score = new_score
            attack_session.attack_stage = attack_stage
            attack_session.total_events = events_count
            if is_suspicious:
                attack_session.suspicious_events += 1

        # Interest classification
        endpoints_list = [e.endpoint for e in all_events] + [endpoint]
        interest = classify_interest(endpoints_list)
        attacker.behavior_type = interest.upper()

        # Trigger automatic lure generation & deployment if threshold met
        if should_gen_lure:
            lure = generate_lure(db, session_id, interest=interest, attack_stage=attack_stage)
            if lure:
                deploy_lure(db, lure.lure_id)
                if attack_session:
                    attack_session.lures_generated += 1

    db.commit()
    db.refresh(event)
    return event

def get_events(db: Session, session_id: Optional[str] = None, page: int = 1, size: int = 50) -> List[Event]:
    query = db.query(Event)
    if session_id:
        query = query.filter(Event.session_id == session_id)
    return query.order_by(Event.timestamp.desc()).offset((page - 1) * size).limit(size).all()
