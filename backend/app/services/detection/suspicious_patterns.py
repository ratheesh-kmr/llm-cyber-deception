import re
from typing import Tuple, Optional

# Suspicious patterns in URL paths or request parameters
PATTERNS = [
    (r"\.\./", "directory_traversal", 4.0, "Directory traversal pattern detected"),
    (r"/\.env", "config_access", 3.0, "Attempted access to environment file"),
    (r"/\.git", "common_vuln_probe", 3.0, "Attempted access to .git repository"),
    (r"/admin", "admin_access", 2.0, "Access to admin endpoint"),
    (r"/config", "config_access", 3.0, "Access to configuration endpoint"),
    (r"/backup", "backup_access", 3.0, "Access to backup endpoint"),
    (r"/api/internal", "api_internal_access", 2.0, "Access to internal API endpoints"),
    (r"SELECT.*FROM", "common_vuln_probe", 4.0, "SQL injection pattern in parameter"),
    (r"UNION.*SELECT", "common_vuln_probe", 4.0, "SQL injection pattern in parameter"),
    (r"<script>", "common_vuln_probe", 3.0, "XSS pattern in request"),
    (r"/robots\.txt", "reconnaissance", 1.0, "Access to robots.txt"),
    (r"/sitemap\.xml", "reconnaissance", 1.0, "Access to sitemap.xml"),
    (r"/login", "credential_discovery", 2.0, "Access to login page"),
]

def analyze_request(path: str, method: str, body: Optional[dict] = None) -> Tuple[bool, float, str, Optional[str]]:
    """
    Analyzes an incoming HTTP request for suspicious patterns.
    Returns: (is_suspicious, risk_delta, event_type, description)
    """
    if method.upper() == "POST" and "/login" in path:
        return True, 4.0, "credential_attempt", "Attacker attempted login POST request"

    for pattern, event_type, delta, desc in PATTERNS:
        if re.search(pattern, path, re.IGNORECASE):
            is_suspicious = delta > 1.0
            return is_suspicious, delta, event_type, desc

    return False, 0.0, "NORMAL_REQUEST", "Normal request"
