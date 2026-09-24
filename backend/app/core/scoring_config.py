"""
Active Cyber Deception Platform — Risk Scoring Engine Design Specification
Implemented as a configuration-driven, deterministic scoring engine.

DESIGN RULE: The LLM must NEVER determine the final numerical risk score.
All scoring is rule-based and deterministic.
"""

# ── Risk Score Thresholds ─────────────────────────────────────────────────────
RISK_THRESHOLDS = {
    "LOW":      (0,  3),
    "MEDIUM":   (4,  7),
    "HIGH":     (8,  11),
    "CRITICAL": (12, float("inf")),
}

# ── Scoring Rules (Configurable) ─────────────────────────────────────────────
SCORING_RULES = {
    # Endpoint-based rules
    "admin_access":            {"score": 2,  "description": "Access to /admin endpoint"},
    "config_access":           {"score": 3,  "description": "Access to /config endpoint"},
    "backup_access":           {"score": 3,  "description": "Access to /backup endpoint"},
    "api_internal_access":     {"score": 2,  "description": "Access to internal API docs"},
    "document_access":         {"score": 1,  "description": "Access to document listing"},
    "directory_traversal":     {"score": 4,  "description": "Directory traversal attempt"},
    "common_vuln_probe":       {"score": 3,  "description": "Common vulnerability probe"},

    # Behavioral rules
    "multiple_failed_requests": {"score": 2, "description": "Multiple 4xx responses in session"},
    "credential_attempt":       {"score": 4, "description": "Login POST attempt detected"},
    "rapid_request_pattern":    {"score": 3, "description": "High request rate detected (>10 req/min)"},
    "sequential_enumeration":   {"score": 3, "description": "Sequential resource enumeration detected"},

    # Interaction rules
    "lure_interaction":         {"score": 5, "description": "Attacker accessed a deployed lure"},
}

# ── Attack Stage Definitions ──────────────────────────────────────────────────
ATTACK_STAGES = [
    "RECONNAISSANCE",
    "RESOURCE_DISCOVERY",
    "CONFIGURATION_DISCOVERY",
    "CREDENTIAL_DISCOVERY",
    "LURE_INTERACTION",
    "CREDENTIAL_ATTEMPT",
]

STAGE_RISK_THRESHOLDS = {
    "RECONNAISSANCE":          0,
    "RESOURCE_DISCOVERY":      3,
    "CONFIGURATION_DISCOVERY": 5,
    "CREDENTIAL_DISCOVERY":    8,
    "LURE_INTERACTION":        10,
    "CREDENTIAL_ATTEMPT":      12,
}

# ── Interest Classification Rules ────────────────────────────────────────────
INTEREST_PATTERNS = {
    "database":        ["/config", "/backup/db", "/admin/db", ".env", "database"],
    "credentials":     ["/login", "/auth", "/admin/users", "/backup/keys", "password"],
    "api":             ["/api/internal", "/api/docs", "/swagger", "/graphql"],
    "admin":           ["/admin", "/admin/panel", "/management", "/dashboard"],
    "configuration":   ["/config", "/.env", "/settings", "/backup/config"],
    "reconnaissance":  ["/", "/robots.txt", "/sitemap.xml", "/.git"],
}

# ── Lure Generation Trigger ───────────────────────────────────────────────────
LURE_GENERATION_TRIGGER_SCORE = 4  # Generate a lure when score exceeds this

# ── Interest to Lure Type Mapping ────────────────────────────────────────────
INTEREST_TO_LURE_TYPE = {
    "database":      "fake_database_config",
    "credentials":   "fake_credentials",
    "api":           "fake_api_documentation",
    "admin":         "fake_internal_document",
    "configuration": "fake_config",
    "reconnaissance":"fake_backup_file",
}
