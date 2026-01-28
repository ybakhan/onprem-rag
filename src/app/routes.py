import logging
import time
import uuid

from datetime import datetime
from fastapi import APIRouter, Body, HTTPException
from .core.chat_completion_local import chat_completion_local
from .config import settings
from .schemas import ChatCompletionRequest, Model, ModelsResponse
from .middleware import request_id_var

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/chat/completions")
async def chat_completions(req: ChatCompletionRequest = Body(...)):
    """Handle chat completion requests."""

    start_time = time.time()
    request_id = request_id_var.get()

    try:
        logger.debug(
            f"Processing chat completion request [ID: {request_id}] with params: "
            f"lang={req.lang}, max_tokens={req.max_tokens}, "
            f"temperature={req.temperature}, top_p={req.top_p}"
        )

        # convert pydantic message to dict
        previous_messages_dicts = [msg.model_dump() for msg in req.messages[:-1]]

        content, prompt_tokens, completion_tokens = chat_completion_local(
            previous_messages=previous_messages_dicts,
            question=req.messages[-1].content,
            lang=req.lang,
            max_tokens=req.max_tokens,
            temperature=req.temperature,
            top_p=req.top_p,
        )

        id_ = f"chatcmpl-{uuid.uuid4().hex[:29]}"

        response = {
            "id": id_,
            "object": "chat.completion",
            "created": int(time.time()),
            "model": settings.CHAT_COMPLETION_MODEL_ID,
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            }],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
            }
        }

        elapsed_time = time.time() - start_time
        logger.info(
            f"Completed request [ID: {request_id}] - "
            f"tokens: {prompt_tokens + completion_tokens}, time: {elapsed_time:.2f}s"
        )
        
        return response

    except Exception as e:
        logger.error(f"Error processing request [ID: {request_id}]: {str(e)}", exc_info=True)
        
        raise HTTPException(status_code=500, detail={
            "error": {
                "message": "An internal server error occurred.",
                "type": "server_error"
            }
        }) from e

@router.get("/models")
async def list_models():
    """List available models."""
    now = int(datetime.utcnow().timestamp())

    available_models = [
        Model(id=settings.CHAT_COMPLETION_MODEL_ID, created=now),
    ]

    return ModelsResponse(data=available_models)
