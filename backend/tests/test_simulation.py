import pytest
from app.core.database import SessionLocal, init_db
from app.services.simulation.runner import run_simulation_scenario
from simulator.scenarios import SCENARIOS

@pytest.fixture(scope="module", autouse=True)
def setup():
    init_db()

def test_simulation_execution_basic():
    db = SessionLocal()
    result = run_simulation_scenario(db, "basic_recon")
    assert result["status"] == "completed"
    assert result["steps_completed"] == 6
    assert result["final_risk_score"] > 0
    assert result["session_id"] is not None
    db.close()

def test_simulation_scenario_invalid():
    db = SessionLocal()
    with pytest.raises(ValueError, match="not found"):
        run_simulation_scenario(db, "non_existent_scenario_123")
    db.close()
