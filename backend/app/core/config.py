import os
from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    APP_NAME: str = "Active Cyber Deception Platform"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_SECRET_KEY: str = "dev-secret-key-cyber-deception-2026"

    DATABASE_URL: str = "sqlite:///./deception.db"

    LLM_PROVIDER: str = "mock"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-4o-mini"
    LLM_TIMEOUT_SECONDS: int = 30
    LLM_MAX_RETRIES: int = 3
    LLM_FALLBACK_TO_MOCK: bool = True

    RISK_LOW_THRESHOLD: float = 3.0
    RISK_MEDIUM_THRESHOLD: float = 7.0
    RISK_HIGH_THRESHOLD: float = 11.0
    LURE_GENERATION_RISK_THRESHOLD: float = 4.0

    DASHBOARD_USERNAME: str = "admin"
    DASHBOARD_PASSWORD: str = "admin"

    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173"
    ALLOWED_HOSTS: str = "*"

    FAKE_COMPANY_NAME: str = "Meridian Technologies Ltd."
    FAKE_DOMAIN: str = "meridian-tech.internal"
    DECEPTION_ENV_HOST: str = "0.0.0.0"
    DECEPTION_ENV_PORT: int = 8001

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
