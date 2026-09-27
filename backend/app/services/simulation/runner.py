import uuid
import time
import httpx
import logging
from typing import Dict, Any, Optional, Generator
from sqlalchemy.orm import Session
from simulator.scenarios import SCENARIO_MAP, SimulationScenario
from app.services.session_service import get_or_create_session
from app.services.event_service import log_event
from app.core.config import settings
from app.models.database import Lure, Attacker, AttackSession

logger = logging.getLogger("deception.simulation")

def resolve_target_host(target_url: Optional[str] = None) -> str:
    """Detects whether standalone port 8001 or mounted /gateway should be targeted."""
    if target_url:
        return target_url.rstrip("/")

    try:
        r = httpx.get(f"http://127.0.0.1:{settings.DECEPTION_ENV_PORT}/", timeout=0.2)
        if r.status_code < 500:
            return f"http://127.0.0.1:{settings.DECEPTION_ENV_PORT}"
    except Exception:
        pass

    return f"http://127.0.0.1:{settings.APP_PORT}/gateway"

def run_simulation_scenario(db: Session, scenario_id: str, target_url: Optional[str] = None) -> Dict[str, Any]:
    """Runs an attack scenario directly against the local deception engine or gateway."""
    scenario: SimulationScenario = SCENARIO_MAP.get(scenario_id)
    if not scenario:
        raise ValueError(f"Scenario '{scenario_id}' not found.")

    session_id = str(uuid.uuid4())
    attacker = get_or_create_session(db, source_ip="192.168.1.100", user_agent="Mozilla/5.0 (CyberSimulator/2.0)", session_id=session_id)
    target_host = resolve_target_host(target_url)

    steps_completed = 0
    with httpx.Client(timeout=2.0) as client:
        for step in scenario.steps:
            try:
                url = f"{target_host}{step.path}"
                headers = {"X-Session-ID": session_id, "User-Agent": "Mozilla/5.0 (CyberSimulator/2.0)"}
                headers.update(step.headers)

                if step.method.upper() == "GET":
                    client.get(url, headers=headers)
                elif step.method.upper() == "POST":
                    client.post(url, headers=headers, json=step.body or {})
                steps_completed += 1
            except Exception as e:
                log_event(db, session_id=session_id, endpoint=step.path, method=step.method, source_ip="192.168.1.100")
                steps_completed += 1

            if step.delay_seconds:
                time.sleep(min(step.delay_seconds, 0.05))

        deployed_lure = db.query(Lure).filter(
            Lure.status == "deployed"
        ).order_by(Lure.created_at.desc()).first()

        if deployed_lure and deployed_lure.endpoint_path:
            try:
                lure_subpath = deployed_lure.endpoint_path
                if not lure_subpath.startswith("/"):
                    lure_subpath = f"/{lure_subpath}"
                lure_url = f"{target_host}{lure_subpath}"
                client.get(lure_url, headers={"X-Session-ID": session_id})
            except Exception:
                pass

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

def stream_simulation_scenario(
    db: Session,
    scenario_id: str,
    target_url: Optional[str] = None,
    speed_factor: float = 1.0
) -> Generator[Dict[str, Any], None, None]:
    """
    Yields live real-time attack simulation events for the War Room interface.
    Emits Red Team action events, Blue Team detection responses, lure deployments, and entrapment alerts.
    """
    scenario: SimulationScenario = SCENARIO_MAP.get(scenario_id)
    if not scenario:
        yield {"type": "error", "message": f"Scenario '{scenario_id}' not found."}
        return

    session_id = str(uuid.uuid4())
    attacker = get_or_create_session(db, source_ip="192.168.1.100", user_agent="Mozilla/5.0 (CyberSimulator/2.0)", session_id=session_id)
    target_host = resolve_target_host(target_url)

    yield {
        "type": "scenario_start",
        "scenario_id": scenario_id,
        "scenario_name": scenario.name,
        "description": scenario.description,
        "session_id": session_id,
        "target_host": target_host,
        "total_steps": len(scenario.steps),
        "expected_interest": scenario.expected_interest,
        "timestamp": time.strftime("%H:%M:%S")
    }

    initial_lure_ids = set(l[0] for l in db.query(Lure.lure_id).all())
    steps_completed = 0

    with httpx.Client(timeout=3.0) as client:
        for idx, step in enumerate(scenario.steps, 1):
            url = f"{target_host}{step.path}"

            # 1. Announce step intent (Red Team)
            yield {
                "type": "step_start",
                "step_index": idx,
                "total_steps": len(scenario.steps),
                "method": step.method.upper(),
                "path": step.path,
                "url": url,
                "description": step.description,
                "body": step.body,
                "timestamp": time.strftime("%H:%M:%S")
            }

            # Configurable pause for realistic live animation
            pause_time = max(0.2, (step.delay_seconds or 1.0) * speed_factor)
            time.sleep(pause_time)

            status_code = None
            resp_snippet = ""
            start_req = time.time()

            try:
                headers = {"X-Session-ID": session_id, "User-Agent": "Mozilla/5.0 (CyberSimulator/2.0)"}
                headers.update(step.headers)

                if step.method.upper() == "GET":
                    r = client.get(url, headers=headers)
                elif step.method.upper() == "POST":
                    r = client.post(url, headers=headers, json=step.body or {})
                else:
                    r = client.request(step.method, url, headers=headers)

                status_code = r.status_code
                resp_snippet = r.text[:200]
            except Exception as e:
                log_event(db, session_id=session_id, endpoint=step.path, method=step.method, source_ip="192.168.1.100")
                status_code = 500
                resp_snippet = f"Gateway logged request directly: {str(e)[:100]}"

            duration_ms = round((time.time() - start_req) * 1000, 1)
            steps_completed += 1

            # Fetch updated state from DB
            db.expire_all()
            att = db.query(Attacker).filter(Attacker.session_id == session_id).first()
            att_sess = db.query(AttackSession).filter(AttackSession.session_id == session_id).first()

            # Check if any new lure was generated & deployed during this step
            current_lures = db.query(Lure).all()
            new_lures = [l for l in current_lures if l.lure_id not in initial_lure_ids]

            for nl in new_lures:
                initial_lure_ids.add(nl.lure_id)
                yield {
                    "type": "lure_deployed",
                    "step_index": idx,
                    "lure_id": nl.lure_id,
                    "title": nl.title,
                    "target_interest": nl.target_interest,
                    "endpoint_path": nl.endpoint_path,
                    "content_preview": nl.content[:160],
                    "generated_by": nl.generated_by,
                    "timestamp": time.strftime("%H:%M:%S")
                }

            # 2. Emit Blue Team evaluation result
            yield {
                "type": "step_finish",
                "step_index": idx,
                "total_steps": len(scenario.steps),
                "method": step.method.upper(),
                "path": step.path,
                "status_code": status_code,
                "duration_ms": duration_ms,
                "risk_score": round(att.risk_score, 1) if att else 0.0,
                "attack_stage": att_sess.attack_stage if att_sess else "RECONNAISSANCE",
                "behavior_type": att.behavior_type if att else "RECONNAISSANCE",
                "response_snippet": resp_snippet,
                "timestamp": time.strftime("%H:%M:%S")
            }

        # Step 3: Check for deployed lure and simulate attacker entrapment
        deployed_lure = db.query(Lure).filter(
            Lure.status == "deployed"
        ).order_by(Lure.created_at.desc()).first()

        if deployed_lure and deployed_lure.endpoint_path:
            time.sleep(0.6 * speed_factor)
            lure_subpath = deployed_lure.endpoint_path
            if not lure_subpath.startswith("/"):
                lure_subpath = f"/{lure_subpath}"
            lure_url = f"{target_host}{lure_subpath}"

            yield {
                "type": "entrapment_probe",
                "lure_id": deployed_lure.lure_id,
                "lure_title": deployed_lure.title,
                "lure_url": lure_url,
                "message": f"Attacker discovered newly deployed honey-token endpoint: {deployed_lure.endpoint_path}",
                "timestamp": time.strftime("%H:%M:%S")
            }

            time.sleep(0.5 * speed_factor)
            try:
                client.get(lure_url, headers={"X-Session-ID": session_id})
                db.expire_all()
                att = db.query(Attacker).filter(Attacker.session_id == session_id).first()
                att_sess = db.query(AttackSession).filter(AttackSession.session_id == session_id).first()

                yield {
                    "type": "lure_entrapped",
                    "lure_id": deployed_lure.lure_id,
                    "lure_title": deployed_lure.title,
                    "endpoint": deployed_lure.endpoint_path,
                    "risk_boost": 5.0,
                    "final_risk_score": round(att.risk_score, 1) if att else 0.0,
                    "attack_stage": att_sess.attack_stage if att_sess else "LURE_INTERACTION",
                    "message": "ATTACKER TRAPPED: Adversary accessed synthetic asset. Honey-token triggered!",
                    "timestamp": time.strftime("%H:%M:%S")
                }
            except Exception:
                pass

    db.expire_all()
    final_att = db.query(Attacker).filter(Attacker.session_id == session_id).first()
    final_sess = db.query(AttackSession).filter(AttackSession.session_id == session_id).first()

    yield {
        "type": "scenario_complete",
        "scenario_id": scenario_id,
        "scenario_name": scenario.name,
        "session_id": session_id,
        "final_risk_score": round(final_att.risk_score, 1) if final_att else 0.0,
        "final_stage": final_sess.attack_stage if final_sess else "COMPLETED",
        "steps_completed": steps_completed,
        "total_steps": len(scenario.steps),
        "status": "completed",
        "timestamp": time.strftime("%H:%M:%S")
    }
