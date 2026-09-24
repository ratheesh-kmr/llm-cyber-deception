import json
import logging
import httpx
from typing import Optional
from app.core.config import settings
from app.services.llm.providers import LLMProvider, LureOutput, MockProvider

logger = logging.getLogger("deception.llm.ollama")

class OllamaProvider(LLMProvider):
    """Local Ollama LLM provider integration."""

    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        self.base_url = base_url or settings.OLLAMA_BASE_URL
        self.model = model or settings.OLLAMA_MODEL

    def generate(self, context: dict) -> Optional[LureOutput]:
        interest = context.get("interest", "reconnaissance")
        prompt = (
            f"You are a cybersecurity deception generator. Create a realistic synthetic lure file for the target interest: '{interest}'.\n"
            "Respond ONLY with a JSON object containing keys: lure_type, title, content, interest, confidence.\n"
            "The content MUST include the line '# SYNTHETIC TEST ENVIRONMENT'. Do NOT include any code execution or real secrets."
        )

        try:
            with httpx.Client(timeout=settings.LLM_TIMEOUT_SECONDS) as client:
                res = client.post(
                    f"{self.base_url}/api/generate",
                    json={"model": self.model, "prompt": prompt, "stream": False, "format": "json"}
                )
                if res.status_code == 200:
                    data = res.json()
                    response_text = data.get("response", "")
                    parsed = json.loads(response_text)
                    return LureOutput(
                        lure_type=parsed.get("lure_type", "fake_config"),
                        title=parsed.get("title", "config.env"),
                        content=parsed.get("content", "# SYNTHETIC\nDB_PASS=fake_pass_123"),
                        interest=interest,
                        confidence=float(parsed.get("confidence", 0.85))
                    )
        except Exception as e:
            logger.warning(f"Ollama generation failed: {e}. Falling back to MockProvider.")

        if settings.LLM_FALLBACK_TO_MOCK:
            return MockProvider().generate(context)
        return None

    @property
    def provider_name(self) -> str:
        return "ollama"
