"""
Active Cyber Deception with LLM-Generated Lures
Pydantic Schemas for Request/Response Validation

These schemas define the API contract for all endpoints.
All fields are type-checked. No unvalidated data passes through the API.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator, AliasChoices, ConfigDict
import uuid


# ── Base Schema with Pydantic V2 Config ───────────────────────────────────────

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# ── Common ────────────────────────────────────────────────────────────────────

class PaginationParams(BaseSchema):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)


class PaginatedResponse(BaseSchema):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int


class ErrorResponse(BaseSchema):
    error: str
    detail: str
    code: int


# ── Session Schemas ───────────────────────────────────────────────────────────

class SessionCreate(BaseSchema):
    source_ip: str = Field(..., max_length=45)
    user_agent: Optional[str] = Field(None, max_length=500)


class SessionResponse(BaseSchema):
    session_id: str
    source_ip: str
    user_agent: Optional[str]
    first_seen: datetime
    last_seen: datetime
    risk_score: float
    behavior_type: Optional[str]
    status: str


class SessionDetailResponse(SessionResponse):
    events: List["EventResponse"] = []
    attack_sessions: List["AttackSessionResponse"] = []
    lure_interactions: List["LureInteractionResponse"] = []


# ── Event Schemas ─────────────────────────────────────────────────────────────

class EventCreate(BaseSchema):
    session_id: str = Field(..., max_length=36)
    event_type: str = Field(..., max_length=50)
    endpoint: str = Field(..., max_length=500)
    method: str = Field(..., max_length=10)
    severity: str = Field(..., max_length=20)
    metadata: Optional[Dict[str, Any]] = None
    is_suspicious: bool = False
    risk_delta: float = 0.0

    @field_validator("severity")
    @classmethod
    def validate_severity(cls, v: str) -> str:
        allowed = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
        if v.upper() not in allowed:
            raise ValueError(f"severity must be one of {allowed}")
        return v.upper()

    @field_validator("method")
    @classmethod
    def validate_method(cls, v: str) -> str:
        allowed = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}
        if v.upper() not in allowed:
            raise ValueError(f"method must be one of {allowed}")
        return v.upper()


class EventResponse(BaseSchema):
    id: int
    session_id: str
    event_type: str
    endpoint: str
    method: str
    timestamp: datetime
    severity: str
    is_suspicious: bool
    risk_delta: float
    metadata: Optional[Dict[str, Any]] = Field(default=None, validation_alias=AliasChoices("metadata_", "metadata"))


# ── Risk Schemas ──────────────────────────────────────────────────────────────

class RiskAssessment(BaseSchema):
    session_id: str
    risk_score: float
    risk_level: str  # LOW | MEDIUM | HIGH | CRITICAL
    attack_stage: str
    behavior_type: Optional[str]
    score_breakdown: Dict[str, float]
    should_generate_lure: bool


# ── Lure Schemas ──────────────────────────────────────────────────────────────

class LureGenerateRequest(BaseSchema):
    session_id: Optional[str] = Field(None, max_length=36)
    interest_override: Optional[str] = Field(None, max_length=50)


class LureResponse(BaseSchema):
    lure_id: str
    lure_type: str
    title: str
    content: str
    target_interest: str
    generated_by: str
    created_at: datetime
    deployed_at: Optional[datetime]
    status: str
    endpoint_path: Optional[str]
    confidence: Optional[float]
    validation_passed: bool
    is_synthetic: bool  # Always True


class LureDeployRequest(BaseSchema):
    endpoint_path: Optional[str] = Field(None, max_length=200)


# ── Interaction Schemas ───────────────────────────────────────────────────────

class LureInteractionResponse(BaseSchema):
    id: int
    lure_id: str
    session_id: str
    interaction_type: str
    timestamp: datetime
    time_spent_seconds: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = Field(default=None, validation_alias=AliasChoices("metadata_", "metadata"))


# ── Attack Session Schemas ────────────────────────────────────────────────────

class AttackSessionResponse(BaseSchema):
    id: int
    session_id: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    risk_score: float
    attack_stage: str
    total_events: int
    suspicious_events: int
    lures_generated: int
    lures_interacted: int


# ── Simulation Schemas ────────────────────────────────────────────────────────

class SimulationRunRequest(BaseSchema):
    scenario_id: str = Field(..., max_length=50)
    target_url: Optional[str] = Field(None, max_length=200)


class SimulationRunResponse(BaseSchema):
    run_id: str
    scenario_id: str
    scenario_name: str
    status: str  # running | completed | failed
    steps_total: int
    steps_completed: int
    session_id: Optional[str] = None
    final_risk_score: Optional[float] = 0.0
    behavior_type: Optional[str] = None


# ── Dashboard Schemas ─────────────────────────────────────────────────────────

class DashboardSummary(BaseSchema):
    active_sessions: int
    total_sessions: int
    total_events: int
    suspicious_events: int
    high_risk_sessions: int
    critical_sessions: int
    generated_lures: int
    deployed_lures: int
    lure_interactions: int
    lure_engagement_rate: float
    attack_stage_distribution: Dict[str, int]
    risk_level_distribution: Dict[str, int]


# ── Forward references update ─────────────────────────────────────────────────
SessionDetailResponse.model_rebuild()
