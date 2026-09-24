"""
Attack Simulation Scenarios
SAFE predefined attack sequences for testing the deception platform.

SECURITY NOTE: These are pre-scripted HTTP request sequences.
The simulator ONLY interacts with the local deception environment.
No real external systems are contacted.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SimulationStep:
    """A single HTTP request in a simulation scenario."""
    method: str
    path: str
    headers: dict = field(default_factory=dict)
    body: Optional[dict] = None
    delay_seconds: float = 1.0
    description: str = ""


@dataclass
class SimulationScenario:
    """A complete predefined attack simulation scenario."""
    scenario_id: str
    name: str
    description: str
    expected_interest: str
    expected_stage: str
    expected_min_risk_score: float
    steps: List[SimulationStep]


# ── Simulation Scenarios ──────────────────────────────────────────────────────

SCENARIOS = [

    SimulationScenario(
        scenario_id="basic_recon",
        name="Basic Reconnaissance",
        description="Simulates initial attacker probing the site structure",
        expected_interest="reconnaissance",
        expected_stage="RESOURCE_DISCOVERY",
        expected_min_risk_score=3.0,
        steps=[
            SimulationStep("GET", "/", delay_seconds=2.0, description="Homepage visit"),
            SimulationStep("GET", "/robots.txt", description="Check robots.txt"),
            SimulationStep("GET", "/sitemap.xml", description="Check sitemap"),
            SimulationStep("GET", "/.git", description="Git exposure probe"),
            SimulationStep("GET", "/admin", description="Admin page probe"),
            SimulationStep("GET", "/login", description="Login page discovery"),
        ]
    ),

    SimulationScenario(
        scenario_id="admin_discovery",
        name="Admin Panel Discovery",
        description="Simulates attacker discovering and probing admin functionality",
        expected_interest="admin",
        expected_stage="RESOURCE_DISCOVERY",
        expected_min_risk_score=6.0,
        steps=[
            SimulationStep("GET", "/", description="Initial visit"),
            SimulationStep("GET", "/admin", description="Admin access attempt"),
            SimulationStep("GET", "/admin/users", description="Admin users probe"),
            SimulationStep("GET", "/admin/config", description="Admin config probe"),
            SimulationStep("GET", "/admin/logs", description="Admin logs probe"),
            SimulationStep("GET", "/management", description="Management panel probe"),
            SimulationStep("GET", "/panel", description="Panel probe"),
        ]
    ),

    SimulationScenario(
        scenario_id="config_discovery",
        name="Configuration File Discovery",
        description="Simulates attacker hunting for exposed configuration files",
        expected_interest="configuration",
        expected_stage="CONFIGURATION_DISCOVERY",
        expected_min_risk_score=8.0,
        steps=[
            SimulationStep("GET", "/admin", description="Admin probe"),
            SimulationStep("GET", "/config", description="Config endpoint probe"),
            SimulationStep("GET", "/.env", description=".env file probe"),
            SimulationStep("GET", "/config/database", description="DB config probe"),
            SimulationStep("GET", "/backup/config", description="Backup config probe"),
            SimulationStep("GET", "/settings", description="Settings probe"),
        ]
    ),

    SimulationScenario(
        scenario_id="credential_discovery",
        name="Credential Discovery",
        description="Simulates attacker attempting to discover or brute-force credentials",
        expected_interest="credentials",
        expected_stage="CREDENTIAL_DISCOVERY",
        expected_min_risk_score=10.0,
        steps=[
            SimulationStep("GET", "/login", description="Login page access"),
            SimulationStep("POST", "/login",
                           body={"username": "admin", "password": "admin"},
                           description="Admin/admin attempt"),
            SimulationStep("POST", "/login",
                           body={"username": "admin", "password": "password"},
                           description="Admin/password attempt"),
            SimulationStep("GET", "/admin", description="Admin access attempt"),
            SimulationStep("GET", "/backup/keys", description="Key backup probe"),
            SimulationStep("POST", "/login",
                           body={"username": "backup_operator", "password": "backup"},
                           description="Service account attempt"),
        ]
    ),

    SimulationScenario(
        scenario_id="database_focused",
        name="Database-Focused Attack",
        description="Simulates attacker specifically targeting database configuration and credentials",
        expected_interest="database",
        expected_stage="CREDENTIAL_DISCOVERY",
        expected_min_risk_score=11.0,
        steps=[
            SimulationStep("GET", "/admin", description="Admin probe"),
            SimulationStep("GET", "/config", description="Config probe"),
            SimulationStep("GET", "/backup/db", description="DB backup probe"),
            SimulationStep("GET", "/.env", description=".env probe"),
            SimulationStep("GET", "/admin/db", description="Admin DB probe"),
            SimulationStep("GET", "/api/internal", description="Internal API probe"),
            SimulationStep("GET", "/backup", description="Backup listing probe"),
        ]
    ),
]

SCENARIO_MAP = {s.scenario_id: s for s in SCENARIOS}
