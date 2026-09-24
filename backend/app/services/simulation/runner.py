import uuid
import time
import httpx
import logging
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from simulator.scenarios import SCENARIO_MAP, SimulationScenario
from app.services.session_service import get_or_create_session
from app.services.event_service import log_event
from app.core.config import settings

logger = logging.getLogger("deception.simulation")

def run_simulation_scenario(db: Session, scenario_id: str, target_url: Optional[str] = None) -> Dict[str, Any]:
    """Runs an attack scenario directly against the local deception engine or gateway."""
    scenario: SimulationScenario = SCENARIO_MAP.get(scenario_id)
    if not scenario:
        raise ValueError(f"Scenario '{scenario_id}' not found.")

    session_id = str(uuid.uuid4())
    attacker = get_or_create_session(db, source_ip="192.168.1.100", user_agent="Mozilla/5.0 (Simulator/1.0)", session_id=session_id)

    target_host = target_url or f"http://127.0.0.1:{settings.DECEPTION_ENV_PORT}"

    steps_completed = 0
    with httpx.Client(timeout=10.0) as client:
        for step in scenario.steps:
            try:
                url = f"{target_host}{step.path}"
                headers = {"X-Session-ID": session_id, "User-Agent": "Mozilla/5.0 (Simulator/1.0)"}
                headers.update(step.headers)

                if step.method.upper() == "GET":
                    client.get(url, headers=headers)
                elif step.method.upper() == "POST":
                    client.post(url, headers=headers, json=step.body or {})
                steps_completed += 1
            except Exception as e:
                # Direct fallback: log event directly if HTTP server is starting up
                log_event(db, session_id=session_id, endpoint=step.path, method=step.method, source_ip="192.168.1.100")
                steps_completed += 1

            if step.delay_seconds:
                time.sleep(min(step.delay_seconds, 0.2))

    db.refresh(attacker)

    return {
        "run_id": str(uuid.uuid4()),
        "scenario_id": scenario_id,
        "scenario_name": scenario.name,
        "status": "completed",
        "steps_total": len(scenario.steps),
        "steps_completed": steps_completed,
        "session_id": session_id,
        "final_risk_score": attacker.risk_score,
        "behavior_type": attacker.behavior_type
    }
