import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal, init_db
from app.services.session_service import get_or_create_session

@pytest.fixture(scope="module", autouse=True)
def setup():
    init_db()

def test_api_root_and_health():
    client = TestClient(app)
    root = client.get("/")
    assert root.status_code == 200
    assert root.json()["status"] == "online"

    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "healthy"

def test_dashboard_summary_endpoint():
    client = TestClient(app)
    res = client.get("/api/dashboard/summary")
    assert res.status_code == 200
    data = res.json()
    assert "total_sessions" in data
    assert "active_sessions" in data
    assert "lure_engagement_rate" in data

def test_sessions_and_detail_endpoints():
    client = TestClient(app)
    db = SessionLocal()
    attacker = get_or_create_session(db, source_ip="192.168.1.77", user_agent="PyTest-Detail")
    session_id = attacker.session_id
    db.close()

    # List sessions
    res_list = client.get("/api/sessions")
    assert res_list.status_code == 200
    assert isinstance(res_list.json(), list)

    # Get session detail
    res_detail = client.get(f"/api/sessions/{session_id}")
    assert res_detail.status_code == 200
    detail = res_detail.json()
    assert detail["session_id"] == session_id
    assert "events" in detail
    assert "attack_sessions" in detail
    assert "lure_interactions" in detail

def test_direct_lure_generation_endpoint():
    client = TestClient(app)
    res = client.post("/api/lures/generate", json={"interest_override": "credentials"})
    assert res.status_code == 200
    data = res.json()
    assert data["target_interest"] == "credentials"
    assert data["is_synthetic"] is True
    assert data["validation_passed"] is True
