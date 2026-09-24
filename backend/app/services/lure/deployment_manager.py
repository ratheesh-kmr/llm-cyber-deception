from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from app.models.database import Lure

def deploy_lure(db: Session, lure_id: str, custom_endpoint: Optional[str] = None) -> Optional[Lure]:
    """Deploys a generated lure so it becomes active and accessible on gateway endpoints."""
    lure = db.query(Lure).filter(Lure.lure_id == lure_id).first()
    if not lure:
        return None

    lure.status = "deployed"
    lure.deployed_at = datetime.utcnow()
    if custom_endpoint:
        lure.endpoint_path = custom_endpoint
    db.commit()
    db.refresh(lure)
    return lure

def get_active_lures(db: Session):
    """Returns all currently deployed lures."""
    return db.query(Lure).filter(Lure.status == "deployed").all()
