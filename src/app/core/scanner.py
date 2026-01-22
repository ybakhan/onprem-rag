import logging

from llm_guard import scan_prompt
from llm_guard.input_scanners import (
    InvisibleText,
    PromptInjection,
    TokenLimit,
    Toxicity,
)
from app.config import settings
from app.core.exceptions import UnsafePromptDetected

logger = logging.getLogger(__name__)

#  Instantiate scanners
input_scanners = [
    # Block very long prompts, adjust limit to model context window
    TokenLimit(
        limit=round(settings.CHAT_COMPLETION_MAX_TOKENS * 0.9), # keep under ~80-90% of model's context
    ),

    # Detect hidden / invisible characters
    InvisibleText(),

    # Detect toxic content   
    Toxicity(threshold=0.5),

    # Prompt injection / jailbreak detector
    PromptInjection(
        # threshold=0.92,            # lower to catch more
    ),
]


def is_prompt_safe(user_prompt: str) -> bool:
    """
    Returns True if the prompt passes all scanners, raises exception if it should be blocked.
    Does NOT modify or sanitize the prompt.
    """
    _, results, risk_scores = scan_prompt(
        prompt=user_prompt,
        scanners=input_scanners,
    )

    is_valid = all(results.values())

    if not is_valid:
        # include scanners that triggered
        failed = {name: score for name, score in risk_scores.items() if score > 0}

        # Log the failure reason(s)
        logger.warning(
            "Prompt blocked by safety scanners",
            extra={
                "failed_scanners": failed,
                # Add more context if needed
                # "request_id": request_id,
            }
        )

        raise UnsafePromptDetected(
                failed_scanners=failed,
                message="Prompt blocked by safety filters"
            )

    return is_valid
