import json
import logging
import requests
from app.core.query import query
from app.core.prompt import generate_prompt
from app.config import settings

logger = logging.getLogger(__name__)


def chat_completion(question):
    """Generate a chat completion response using retrieved context and chat completion model."""
    context = query(question)
    prompt = generate_prompt(question, context)

    payload = {
        "model": settings.CHAT_COMPLETION_MODEL_ID,
        "max_tokens": settings.CHAT_COMPLETION_MAX_TOKENS,
        "temperature": settings.CHAT_COMPLETION_TEMPERATURE,
        "top_p": settings.CHAT_COMPLETION_TOP_P,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }
    logger.debug("Chat completion request\n%s", json.dumps(payload, indent=2))

    url = f"http://{settings.CHAT_COMPLETION_HOST}:{settings.CHAT_COMPLETION_PORT}/v1/chat/completions"
    response = requests.post(
        url=url,
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=settings.CHAT_COMPLETION_TIMEOUT_SECONDS,
    )

    logger.debug("Chat completion response\n%s", json.dumps(response.json(), indent=2))
