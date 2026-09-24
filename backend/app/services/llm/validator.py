from typing import Tuple, List
from app.services.llm.providers import PROHIBITED_COMMANDS, PROHIBITED_REAL_PATTERNS, SYNTHETIC_MARKERS, LureOutput

class LureValidator:
    """Validates LLM outputs against security boundaries before deployment."""

    @staticmethod
    def validate(lure: LureOutput) -> Tuple[bool, List[str]]:
        """
        Validates a LureOutput.
        Returns (is_valid, list_of_error_messages).
        """
        errors = []

        if not lure.content or len(lure.content.strip()) < 10:
            errors.append("Lure content is empty or too short.")

        if not lure.title:
            errors.append("Lure title is missing.")

        content_lower = lure.content.lower()

        # Check for prohibited commands
        for cmd in PROHIBITED_COMMANDS:
            if cmd.lower() in content_lower:
                errors.append(f"Prohibited command pattern detected: '{cmd}'")

        # Check for real credential format patterns
        for pattern in PROHIBITED_REAL_PATTERNS:
            if pattern in lure.content:
                errors.append(f"Potential real credential pattern detected: '{pattern}'")

        # Check synthetic marker presence
        has_marker = any(marker in lure.content for marker in SYNTHETIC_MARKERS)
        if not has_marker:
            # Inject synthetic marker if missing
            lure.content = f"# SYNTHETIC DECEPTION ARTIFACT — DO NOT USE IN PRODUCTION\n{lure.content}"

        return len(errors) == 0, errors
