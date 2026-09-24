import json
import logging
import httpx
from typing import Optional
from app.core.config import settings
from app.services.llm.providers import LLMProvider, LureOutput, MockProvider

logger = logging.getLogger("deception.llm.openai")

class OpenAIProvider(LLMProvider):
    """OpenAI API integration for synthetic lure generation."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.OPENAI_MODEL
        self.base_url = settings.OPENAI_BASE_URL

    def generate(self, context: dict) -> Optional[LureOutput]:
        if not self.api_key:
            logger.info("OpenAI API key missing. Falling back to MockProvider.")
            return MockProvider().generate(context)

        interest = context.get("interest", "reconnaissance")
        system_prompt = (
            "You generate synthetic cybersecurity lure artifacts for deception environments. "
            "Return valid JSON ONLY with keys: lure_type, title, content, interest, confidence. "
            "Content MUST start with '# SYNTHETIC DECEPTION ARTIFACT'. Never include actual credentials."
        )
        user_prompt = f"Target Interest: {interest}. Generate an appropriate lure file."

        try:
            with httpx.Client(timeout=settings.LLM_TIMEOUT_SECONDS) as client:
                res = client.post(
                    f"{self.base_url}/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        "response_format": {"type": "json_object"}
                    }
                )
                if res.status_code == 200:
                    data = res.json()
                    content = data["choices"][0]["message"]["content"]
                    parsed = json.loads(content)
                    return LureOutput(
                        lure_type=parsed.get("lure_type", "fake_config"),
                        title=parsed.get("title", "config.env"),
                        content=parsed.get("content", "# SYNTHETIC\nDB_PASS=fake_pass_123"),
                        interest=interest,
                        confidence=float(parsed.get("confidence", 0.90))
                    )
        except Exception as e:
            logger.warning(f"OpenAI generation failed: {e}. Falling back to MockProvider.")

        if settings.LLM_FALLBACK_TO_MOCK:
            return MockProvider().generate(context)
        return None

    @property
    def provider_name(self) -> str:
        return "openai"
