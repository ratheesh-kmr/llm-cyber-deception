import pytest
from app.core.database import SessionLocal, init_db
from app.services.session_service import get_or_create_session
from app.services.llm.generator import generate_lure
from app.services.llm.validator import LureValidator, LureOutput

def test_lure_validator():
    valid_lure = LureOutput(
        lure_type="fake_config",
        title="test.env",
        content="# SYNTHETIC TEST ENVIRONMENT\nDB_PASS=123",
        interest="database",
        confidence=0.9
    )
    is_valid, errors = LureValidator.validate(valid_lure)
    assert is_valid is True
    assert len(errors) == 0

def test_lure_generation_and_storage():
    init_db()
    db = SessionLocal()
    attacker = get_or_create_session(db, source_ip="127.0.0.1", user_agent="PyTest")
    lure = generate_lure(db, session_id=attacker.session_id, interest="database")
    assert lure is not None
    assert lure.is_synthetic is True
    assert "database" in lure.target_interest
    db.close()
