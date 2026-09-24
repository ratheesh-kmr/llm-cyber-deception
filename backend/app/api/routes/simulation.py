from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.schemas import SimulationRunRequest, SimulationRunResponse
from app.services.simulation.runner import run_simulation_scenario
from simulator.scenarios import SCENARIOS

router = APIRouter(prefix="/simulation", tags=["Simulation"])

@router.get("/scenarios")
def list_scenarios():
    return [
        {
            "scenario_id": s.scenario_id,
            "name": s.name,
            "description": s.description,
            "expected_interest": s.expected_interest,
            "expected_stage": s.expected_stage,
            "step_count": len(s.steps)
        }
        for s in SCENARIOS
    ]

@router.post("/run", response_model=SimulationRunResponse)
def run_simulation(payload: SimulationRunRequest, db: Session = Depends(get_db)):
    try:
        result = run_simulation_scenario(db, payload.scenario_id, payload.target_url)
        return SimulationRunResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation error: {str(e)}")
