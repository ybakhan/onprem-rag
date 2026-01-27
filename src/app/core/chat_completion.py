import json
from http import HTTPStatus
import logging
import requests
from requests.exceptions import Timeout, HTTPError
from transformers import AutoTokenizer
from app.core.query import query
from app.core.prompt import generate_prompt
from app.config import settings
from app.core.exceptions import ChatCompletionTimeoutError, ChatCompletionError
from app.core.scanner import is_prompt_safe

logger = logging.getLogger(__name__)

tokenizer = AutoTokenizer.from_pretrained(settings.CHAT_COMPLETION_MODEL_ID)

def chat_completion(question, lang, previous_messages=None, **kwargs):
    """Generate a chat completion response using retrieved context and chat completion model."""

    is_prompt_safe(question)
    context = query(question, lang)
    prompt = generate_prompt(question, context, lang)

    if previous_messages is None:
        previous_messages = []

    messages = previous_messages + [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    payload = {
        "model": settings.CHAT_COMPLETION_MODEL_ID,
        "max_tokens": kwargs.get("max_tokens", settings.CHAT_COMPLETION_MAX_TOKENS),
        "temperature": kwargs.get("temperature", settings.CHAT_COMPLETION_TEMPERATURE),
        "top_p": kwargs.get("top_p", settings.CHAT_COMPLETION_TOP_P),
        "messages": messages,
    }
    logger.debug("Chat completion request\n%s", json.dumps(payload, indent=2))

    url = (
        f"http://{settings.CHAT_COMPLETION_HOST}:"
        f"{settings.CHAT_COMPLETION_PORT}/v1/chat/completions"
    )

    prompt_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    prompt_tokens = len(tokenizer(prompt_text)["input_ids"])

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
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            message=str(e)
        ) from e

    data = response.json()
    logger.debug("Chat completion response\n%s", json.dumps(data, indent=2))

    answer = data["choices"][0]["message"]["content"]
    completion_tokens = len(tokenizer(answer)["input_ids"])

    return answer, prompt_tokens, completion_tokens
