import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal, init_db
from app.services.session_service import get_or_create_session
from app.services.llm.generator import generate_lure
from app.services.lure.deployment_manager import deploy_lure

@pytest.fixture(scope="module", autouse=True)
def setup():
    init_db()

def test_gateway_home():
    client = TestClient(app)
    response = client.get("/gateway/")
    assert response.status_code == 200
    assert "Meridian Technologies" in response.text
    assert "Employee Login" in response.text
    assert "deception_session" in response.cookies

def test_gateway_login_flow():
    client = TestClient(app)
    # GET login page
    get_res = client.get("/gateway/login")
    assert get_res.status_code == 200
    assert "Access Panel" in get_res.text

    # POST invalid login
    post_res = client.post("/gateway/login", json={"username": "admin", "password": "password123"})
    assert post_res.status_code == 401
    assert post_res.json()["error"] == "Unauthorized"

def test_gateway_recon_probes():
    client = TestClient(app)
    # Probe robots.txt
    res = client.get("/gateway/robots.txt")
    assert res.status_code == 200
    assert "Disallow: /admin/" in res.text

    # Probe sitemap.xml
    res_sitemap = client.get("/gateway/sitemap.xml")
    assert res_sitemap.status_code == 200
    assert "meridian-tech.internal" in res_sitemap.text

def test_gateway_deployed_lure_interaction():
    client = TestClient(app)
    db = SessionLocal()
    session = get_or_create_session(db, source_ip="192.168.1.55", user_agent="Attacker-Bot/1.0")
    sess_id = session.session_id

    # Generate and deploy a lure
    lure = generate_lure(db, session_id=sess_id, interest="database")
    assert lure is not None
    deploy_lure(db, lure_id=lure.lure_id, custom_endpoint="/config/database")
    lure_content = lure.content
    db.close()

    # Now request this endpoint via gateway
    headers = {"X-Session-ID": sess_id}
    res = client.get("/gateway/config/database", headers=headers)
    assert res.status_code == 200
    assert lure_content in res.text
