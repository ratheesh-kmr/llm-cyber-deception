import pytest
from app.services.detection.scoring_engine import calculate_risk_level, evaluate_risk

def test_risk_level_categories():
    assert calculate_risk_level(2.0) == "LOW"
    assert calculate_risk_level(5.0) == "MEDIUM"
    assert calculate_risk_level(9.0) == "HIGH"
    assert calculate_risk_level(15.0) == "CRITICAL"

def test_evaluate_risk_escalation():
    new_score, level, stage, trigger = evaluate_risk(current_score=2.0, risk_delta=4.0, session_events_count=3)
    assert new_score == 6.0
    assert level == "MEDIUM"
    assert stage == "CONFIGURATION_DISCOVERY"
    assert trigger is True
