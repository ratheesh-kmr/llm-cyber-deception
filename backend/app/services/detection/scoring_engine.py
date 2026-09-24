from typing import Dict, Any, Tuple
from app.core.scoring_config import RISK_THRESHOLDS, LURE_GENERATION_TRIGGER_SCORE
from app.services.detection.stage_tracker import determine_attack_stage

def calculate_risk_level(risk_score: float) -> str:
    """Categorizes numerical risk score into LOW | MEDIUM | HIGH | CRITICAL."""
    if risk_score >= RISK_THRESHOLDS["CRITICAL"][0]:
        return "CRITICAL"
    elif risk_score >= RISK_THRESHOLDS["HIGH"][0]:
        return "HIGH"
    elif risk_score >= RISK_THRESHOLDS["MEDIUM"][0]:
        return "MEDIUM"
    return "LOW"

def evaluate_risk(current_score: float, risk_delta: float, session_events_count: int, lure_interacted: bool = False, attempted_login: bool = False) -> Tuple[float, str, str, bool]:
    """
    Computes updated risk score, level, stage, and whether a lure should be generated.
    Returns: (new_risk_score, risk_level, attack_stage, should_generate_lure)
    """
    new_score = current_score + risk_delta
    risk_level = calculate_risk_level(new_score)
    attack_stage = determine_attack_stage(new_score, lure_interacted, attempted_login)

    # Trigger lure generation when threshold crossed
    should_generate_lure = (new_score >= LURE_GENERATION_TRIGGER_SCORE and current_score < LURE_GENERATION_TRIGGER_SCORE) or (new_score >= 8.0 and session_events_count % 5 == 0)

    return new_score, risk_level, attack_stage, should_generate_lure
