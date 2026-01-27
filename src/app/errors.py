
import logging
from http import HTTPStatus
from pydantic import ValidationError
from fastapi import Request
from fastapi.responses import JSONResponse
from .middleware import request_id_var
from .config import settings
from .core.exceptions import (
    ChatCompletionError,
    ChatCompletionTimeoutError,
    UnsafePromptDetected,
)

logger = logging.getLogger(__name__)


async def validation_error_handler(_request: Request, exc: ValidationError):
    """Handle validation errors."""

    request_id = request_id_var.get()
    logger.warning(f"Validation error in request [ID: {request_id}]: {exc.errors()}")

    return JSONResponse(status_code=400, content={
        "error": {
            "request_id": request_id,
            "message": "Validation failed",
            "type": "invalid_request_error",
            "details": exc.errors(),
        }
    })

async def value_error_handler(_request: Request, exc: ValueError):
    """Handle value errors."""

    request_id = request_id_var.get()
    logger.warning(f"Value error in request [ID: {request_id}]: {str(exc)}")

    return JSONResponse(status_code=400, content={
        "error": {
            "request_id": request_id,
            "message": "Bad request",
            "type": "invalid_request_error",
            "details": [
                {
                    "message": str(exc),
                    "type": "value_error",
                }
            ],
        }
    })


async def general_exception_handler(_request: Request, exc: Exception):
    """Handle unexpected errors."""

    request_id = request_id_var.get()
    logger.error(f"Unexpected error in request [ID: {request_id}]: {str(exc)}", exc_info=True)

    return JSONResponse(status_code=500, content={
        "error": {
            "request_id": request_id,
            "message": "An internal server error occurred.",
            "type": "server_error",
            "details": [
                {
                    "message": "Unexpected server error",
                    "type": "internal_error",
                    "code": type(exc).__name__    
                }
            ],
        }
    })

async def chat_completion_error_handler(_request: Request, exc: ChatCompletionError):
    """Handle general chat completion failures (e.g. backend errors, invalid params from model)."""
    
    request_id = request_id_var.get()
    status_code = exc.status_code or 500
    log_level = logger.error if status_code >= 500 else logger.warning

    log_level(
        f"Chat completion error [ID: {request_id}]: {exc.message} "
        f"(status={status_code})",
        exc_info=True
    )

    content = {
        "error": {
            "request_id": request_id,
            "message": "Chat completion failed",
            "type": "invalid_request_error" if status_code < 500 else "server_error",
            "details": [
                {
                    "message": exc.message,
                    "type": "completion_error",
                }
            ],
        }
    }

    return JSONResponse(status_code=status_code, content=content)

async def chat_completion_timeout_handler(_request: Request, exc: ChatCompletionTimeoutError):
    """Handle chat completion timeouts"""

    request_id = request_id_var.get()
    logger.warning(f"Chat completion timeout [ID: {request_id}]: {str(exc)}")

    return JSONResponse(status_code=HTTPStatus.GATEWAY_TIMEOUT.value, content={
        "error": {
            "request_id": request_id,
            "message": "Chat completion failed",
            "type": "timeout_error",
            "details": [
                {
                    "message": str(exc),
                    "type": "timeout",
                    "timeout_seconds": settings.CHAT_COMPLETION_TIMEOUT_SECONDS,
                }
            ],
        }
    })

async def unsafe_prompt_detected_handler(_request: Request, exc: UnsafePromptDetected):
    """Handle safety blockages (403 Forbidden or 400 depending on policy)."""
    
    request_id = request_id_var.get()
    logger.warning(
        f"Unsafe prompt detected [ID: {request_id}]: {exc.message} "
        f"failed scanners: {exc.failed_scanners}"
    )

    return JSONResponse(status_code=400, content={
        "error": {
            "request_id": request_id,
            "message": "Prompt blocked by safety checks",
            "type": "invalid_request_error",
            "details": [
                {
                    "message": exc.message,
                    "type": "safety_violation",
                    "failed_scanners": exc.failed_scanners,
                }
            ],
        }
    })
