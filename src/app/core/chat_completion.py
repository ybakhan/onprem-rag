import json
import logging
import requests
from requests.exceptions import Timeout, HTTPError, JSONDecodeError
from app.core.query import query
from app.core.prompt import generate_prompt
from app.config import settings
from app.core.exceptions import ChatCompletionTimeoutError, ChatCompletionError

logger = logging.getLogger(__name__)


def chat_completion(question, lang):
    """Generate a chat completion response using retrieved context and chat completion model."""
    context = query(question, lang)
    prompt = generate_prompt(question, context, lang)

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

    url = (
        f"http://{settings.CHAT_COMPLETION_HOST}:"
        f"{settings.CHAT_COMPLETION_PORT}/v1/chat/completions"
    )

    try:
        response = requests.post(
            url=url,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=settings.CHAT_COMPLETION_TIMEOUT_SECONDS,
        )
        response.raise_for_status()

    except Timeout as e:
        raise ChatCompletionTimeoutError() from e
    
    except HTTPError as e:
        raise ChatCompletionError(
            status_code=e.response.status_code,
            message=e.response.text[:300]
        ) from e

    except Exception as e:
        raise ChatCompletionError(
            message=str(e)
        ) from e

    data = response.json()
    logger.debug("Chat completion response\n%s", json.dumps(data, indent=2))

    answer = data["choices"][0]["message"]["content"]
    return answer
