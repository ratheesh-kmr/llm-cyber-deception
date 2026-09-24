"""
Active Cyber Deception Platform — LLM Provider Abstraction

SECURITY CONSTRAINTS:
  1. LLM output is NEVER executed directly.
  2. All LLM output passes through LureValidator before use.
  3. Raw user input is NEVER included in LLM prompts.
  4. All generated content is labeled synthetic.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
import json
import random


# ── Output Schema ─────────────────────────────────────────────────────────────

@dataclass
class LureOutput:
    """Structured output that the LLM must return. Validated before use."""
    lure_type: str
    title: str
    content: str
    interest: str
    confidence: float


# ── Abstract Base Provider ────────────────────────────────────────────────────

class LLMProvider(ABC):
    """
    Abstract base class for all LLM providers.
    All providers must implement generate() with the same interface.
    """

    @abstractmethod
    def generate(self, context: dict) -> Optional[LureOutput]:
        """
        Generate a synthetic lure based on sanitized attacker behavioral context.

        Args:
            context: Sanitized dict containing ONLY:
                     - interest (str): attacker interest category
                     - attack_stage (str): current attack stage
                     - requested_resources (list[str]): visited endpoints
                     - risk_level (str): LOW/MEDIUM/HIGH/CRITICAL
                     - session_duration_minutes (float): session age

        Returns:
            LureOutput if generation succeeded, None on failure.
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the name of this provider."""
        pass


# ── Mock Provider (DEMO MODE) ─────────────────────────────────────────────────

class MockProvider(LLMProvider):
    """
    Deterministic mock LLM provider for demo mode.
    Returns predefined realistic synthetic lures based on attacker interest.
    No external API calls. No API key required.
    Used when LLM_PROVIDER=mock.
    """

    MOCK_LURES = {
        "database": {
            "lure_type": "fake_database_config",
            "title": "production.env",
            "content": (
                "# Meridian Technologies Production Database Config\n"
                "# SYNTHETIC TEST ENVIRONMENT — DO NOT USE IN PRODUCTION\n"
                "DB_HOST=10.10.20.15\n"
                "DB_PORT=5432\n"
                "DB_NAME=prod_customers_v3\n"
                "DB_USER=dbadmin_prod\n"
                "DB_PASS=synthetic_db_pass_2026\n"
                "DB_SSL_MODE=require\n"
                "DB_MAX_CONNECTIONS=100\n"
                "REDIS_URL=redis://10.10.20.16:6379\n"
                "REDIS_PASSWORD=synthetic_redis_pass_2026\n"
                "BACKUP_DB_HOST=10.10.20.17\n"
                "BACKUP_SCHEDULE=0 2 * * *\n"
            ),
            "interest": "database",
            "confidence": 0.95,
        },
        "credentials": {
            "lure_type": "fake_credentials",
            "title": "service-accounts.txt",
            "content": (
                "# Meridian Technologies Service Account Credentials\n"
                "# SYNTHETIC — ALL VALUES ARE FAKE\n"
                "# Generated for deception environment testing\n\n"
                "[backup_service]\n"
                "username: backup_operator\n"
                "password: synthetic_backup_2026\n"
                "role: backup_admin\n"
                "last_rotated: 2026-01-15\n\n"
                "[reporting_service]\n"
                "username: report_svc_user\n"
                "password: synthetic_report_svc_99\n"
                "role: readonly\n"
                "last_rotated: 2026-03-01\n\n"
                "[api_gateway]\n"
                "api_key: sk-synthetic-meridian-api-2026-xK9pQ7\n"
                "secret: synthetic_gateway_secret_2026\n"
            ),
            "interest": "credentials",
            "confidence": 0.92,
        },
        "api": {
            "lure_type": "fake_api_documentation",
            "title": "Internal Reporting API v2.md",
            "content": (
                "# Meridian Technologies Internal Reporting API v2\n"
                "# SYNTHETIC DOCUMENTATION — DECEPTION ENVIRONMENT\n\n"
                "Base URL: http://api.meridian-tech.internal/v2/reporting\n"
                "Authentication: Bearer token required\n\n"
                "## Authentication\n"
                "POST /auth/token\n"
                "Body: { \"client_id\": \"<id>\", \"client_secret\": \"<secret>\" }\n\n"
                "## Endpoints\n"
                "GET /reports/financial — Quarterly financial summaries\n"
                "GET /reports/users — Active user export\n"
                "POST /reports/generate — Trigger report generation\n\n"
                "## Example Token (SYNTHETIC)\n"
                "Authorization: Bearer synthetic-internal-api-token-meridian-2026\n"
            ),
            "interest": "api",
            "confidence": 0.90,
        },
        "admin": {
            "lure_type": "fake_internal_document",
            "title": "Database Migration Plan Q1 2026.pdf.txt",
            "content": (
                "MERIDIAN TECHNOLOGIES — INTERNAL CONFIDENTIAL\n"
                "[SYNTHETIC DOCUMENT — DECEPTION ENVIRONMENT]\n\n"
                "Project: Database Migration Plan — Q1 2026\n"
                "Author: Infrastructure Team\n"
                "Classification: Internal Use Only\n\n"
                "1. OVERVIEW\n"
                "Migration from legacy PostgreSQL 12 cluster to PostgreSQL 15 HA cluster.\n"
                "Target completion: 2026-03-15.\n\n"
                "2. MIGRATION CREDENTIALS (TEST ENV)\n"
                "Migration User: db_migration_svc\n"
                "Password: synthetic_migration_2026\n"
                "Target DB Host: 10.10.30.50\n\n"
                "3. SCHEDULE\n"
                "Phase 1 (2026-02-01): Schema migration\n"
                "Phase 2 (2026-02-15): Data migration\n"
                "Phase 3 (2026-03-01): Cutover\n"
            ),
            "interest": "admin",
            "confidence": 0.88,
        },
        "reconnaissance": {
            "lure_type": "fake_backup_file",
            "title": "backup_inventory_2026.txt",
            "content": (
                "# Meridian Technologies Backup Inventory\n"
                "# SYNTHETIC — DECEPTION ENVIRONMENT\n"
                "# Generated: 2026-09-01 02:00:00 UTC\n\n"
                "BACKUP CATALOG:\n"
                "backup_prod_db_2026-08-31.tar.gz   (4.2 GB)  /backups/db/\n"
                "backup_config_2026-08-31.tar.gz    (128 MB)  /backups/config/\n"
                "backup_userdata_2026-08-31.tar.gz  (11.7 GB) /backups/users/\n"
                "backup_apikeys_2026-08-31.tar.gz   (2 KB)    /backups/keys/\n\n"
                "BACKUP SERVER: 10.10.20.20\n"
                "BACKUP USER: backup_operator\n"
                "BACKUP KEY: /etc/backup/synthetic_id_rsa\n"
            ),
            "interest": "reconnaissance",
            "confidence": 0.85,
        },
    }

    def generate(self, context: dict) -> Optional[LureOutput]:
        interest = context.get("interest", "reconnaissance")
        lure_data = self.MOCK_LURES.get(interest, self.MOCK_LURES["reconnaissance"])
        return LureOutput(**lure_data)

    @property
    def provider_name(self) -> str:
        return "mock"


# ── Lure Type Definitions ─────────────────────────────────────────────────────

LURE_TYPES = [
    "fake_credentials",
    "fake_database_config",
    "fake_internal_document",
    "fake_api_documentation",
    "fake_backup_file",
    "fake_config",
]

# ── Prohibited Content Patterns (for LureValidator) ──────────────────────────

PROHIBITED_COMMANDS = [
    "rm -rf", "chmod", "curl ", "wget ", "eval(", "exec(",
    "os.system", "subprocess", "import os", "__import__",
    "powershell", "cmd.exe", "/bin/sh", "/bin/bash",
    "SELECT ", "DROP TABLE", "UPDATE ", "DELETE FROM",
]

PROHIBITED_REAL_PATTERNS = [
    # Real credential patterns
    "AKIA",          # AWS access key prefix
    "ghp_",          # GitHub personal token prefix
    "sk-proj-",      # OpenAI key prefix
]

# Lures must contain at least one of these synthetic markers
SYNTHETIC_MARKERS = [
    "synthetic",
    "SYNTHETIC",
    "deception",
    "DECEPTION",
    "meridian-tech.internal",
    "test environment",
    "TEST ENVIRONMENT",
]
