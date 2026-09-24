from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.schemas import DashboardSummary
from app.models.database import Attacker, Event, Lure, LureInteraction, AttackSession
from app.services.detection.scoring_engine import calculate_risk_level

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(db: Session = Depends(get_db)):
    active_sessions = db.query(Attacker).filter(Attacker.status == "active").count()
    total_sessions = db.query(Attacker).count()
    total_events = db.query(Event).count()
    suspicious_events = db.query(Event).filter(Event.is_suspicious == True).count()

    all_attackers = db.query(Attacker).all()
    high_risk = sum(1 for a in all_attackers if calculate_risk_level(a.risk_score) == "HIGH")
    critical_risk = sum(1 for a in all_attackers if calculate_risk_level(a.risk_score) == "CRITICAL")

    generated_lures = db.query(Lure).count()
    deployed_lures = db.query(Lure).filter(Lure.status == "deployed").count()
    lure_interactions = db.query(LureInteraction).count()

    engagement_rate = round((lure_interactions / deployed_lures * 100.0) if deployed_lures > 0 else 0.0, 1)

    stage_counts = {}
    attack_sessions = db.query(AttackSession).all()
    for s in attack_sessions:
        stage_counts[s.attack_stage] = stage_counts.get(s.attack_stage, 0) + 1

    risk_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
    for a in all_attackers:
        lvl = calculate_risk_level(a.risk_score)
        risk_counts[lvl] = risk_counts.get(lvl, 0) + 1

    return DashboardSummary(
        active_sessions=active_sessions,
        total_sessions=total_sessions,
        total_events=total_events,
        suspicious_events=suspicious_events,
        high_risk_sessions=high_risk,
        critical_sessions=critical_risk,
        generated_lures=generated_lures,
        deployed_lures=deployed_lures,
        lure_interactions=lure_interactions,
        lure_engagement_rate=engagement_rate,
        attack_stage_distribution=stage_counts,
        risk_level_distribution=risk_counts
    )
