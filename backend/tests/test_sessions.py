import pytest
from app.core.database import SessionLocal, init_db
from app.services.session_service import get_or_create_session, get_all_sessions

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()

def test_create_and_get_session():
    db = SessionLocal()
    attacker = get_or_create_session(db, source_ip="10.0.0.1", user_agent="PyTest-Agent")
    assert attacker.session_id is not None
    assert attacker.source_ip == "10.0.0.1"

    all_sess = get_all_sessions(db)
    assert len(all_sess) > 0
    db.close()
