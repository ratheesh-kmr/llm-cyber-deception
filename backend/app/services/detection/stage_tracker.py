from app.core.scoring_config import STAGE_RISK_THRESHOLDS

def determine_attack_stage(risk_score: float, interacted_with_lure: bool = False, attempted_login: bool = False) -> str:
    """
    Determines current attack stage based on cumulative risk score and key interactions.
    Stages: RECONNAISSANCE → RESOURCE_DISCOVERY → CONFIGURATION_DISCOVERY
            → CREDENTIAL_DISCOVERY → LURE_INTERACTION → CREDENTIAL_ATTEMPT
    """
    if attempted_login:
        return "CREDENTIAL_ATTEMPT"
    if interacted_with_lure:
        return "LURE_INTERACTION"

    if risk_score >= STAGE_RISK_THRESHOLDS["CREDENTIAL_DISCOVERY"]:
        return "CREDENTIAL_DISCOVERY"
    elif risk_score >= STAGE_RISK_THRESHOLDS["CONFIGURATION_DISCOVERY"]:
        return "CONFIGURATION_DISCOVERY"
    elif risk_score >= STAGE_RISK_THRESHOLDS["RESOURCE_DISCOVERY"]:
        return "RESOURCE_DISCOVERY"
    else:
        return "RECONNAISSANCE"
