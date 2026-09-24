import uuid
import time
from typing import Optional
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.database import Lure, LLMGeneration
from app.services.llm.providers import MockProvider, LLMProvider
from app.services.llm.ollama_provider import OllamaProvider
from app.services.llm.openai_provider import OpenAIProvider
from app.services.llm.validator import LureValidator

def get_llm_provider(provider_type: Optional[str] = None) -> LLMProvider:
    p_type = (provider_type or settings.LLM_PROVIDER).lower()
    if p_type == "ollama":
        return OllamaProvider()
    elif p_type == "openai":
        return OpenAIProvider()
    return MockProvider()

def generate_lure(db: Session, session_id: str, interest: str, attack_stage: str = "RESOURCE_DISCOVERY", provider_name: Optional[str] = None) -> Optional[Lure]:
    """Generates, validates, and stores a new synthetic lure."""
    provider = get_llm_provider(provider_name)
    gen_id = str(uuid.uuid4())
    start_time = time.time()

    context = {
        "interest": interest,
        "attack_stage": attack_stage,
        "session_id": session_id
    }

    # Generate lure content
    raw_lure = provider.generate(context)
    elapsed_ms = (time.time() - start_time) * 1000

    if not raw_lure:
        return None

    # Validate lure output
    is_valid, errors = LureValidator.validate(raw_lure)

    # Save LLM generation audit record
    audit = LLMGeneration(
        generation_id=gen_id,
        prompt_template=f"lure_generation_{interest}",
        model=provider.provider_name,
        input_context=context,
        output={"lure_type": raw_lure.lure_type, "title": raw_lure.title, "content": raw_lure.content},
        validation_status="passed" if is_valid else "failed",
        validation_errors=errors if errors else None,
        processing_time_ms=elapsed_ms,
        session_id=session_id
    )
    db.add(audit)
    db.commit()

    if not is_valid:
        # Fallback to Mock if LLM output failed validation
        raw_lure = MockProvider().generate(context)
        is_valid, errors = LureValidator.validate(raw_lure)

    lure_uuid = str(uuid.uuid4())
    endpoint_path = f"/lures/{interest}/{raw_lure.title}"

    db_lure = Lure(
        lure_id=lure_uuid,
        lure_type=raw_lure.lure_type,
        title=raw_lure.title,
        content=raw_lure.content,
        target_interest=interest,
        generated_by=provider.provider_name,
        status="generated",
        endpoint_path=endpoint_path,
        confidence=raw_lure.confidence,
        validation_passed=is_valid,
        is_synthetic=True
    )
    db.add(db_lure)
    db.commit()
    db.refresh(db_lure)

    return db_lure
