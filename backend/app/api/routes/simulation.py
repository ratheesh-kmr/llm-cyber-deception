import json
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.schemas import SimulationRunRequest, SimulationRunResponse
from app.services.simulation.runner import run_simulation_scenario, stream_simulation_scenario
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

@router.get("/stream")
def stream_simulation_endpoint(
    scenario_id: str = Query(..., description="ID of attack scenario to stream"),
    speed: float = Query(0.6, ge=0.05, le=3.0, description="Delay multiplier for animation speed"),
    target_url: Optional[str] = Query(None, description="Optional custom target url"),
    db: Session = Depends(get_db)
):
    """
    Server-Sent Events (SSE) endpoint providing live real-time cyber attack telemetry.
    Streams Red Team attacks, Blue Team detections, LLM lure deployments, and entrapments.
    """
    def event_generator():
        for event in stream_simulation_scenario(db, scenario_id=scenario_id, target_url=target_url, speed_factor=speed):
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
