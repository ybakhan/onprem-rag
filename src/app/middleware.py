import uuid

from contextvars import ContextVar
from fastapi import Request

request_id_var: ContextVar[str] = ContextVar("request_id", default="----")

async def add_request_id(request: Request, call_next):
    """Add request ID to context."""

    rid = str(uuid.uuid4())[:8]
    token = request_id_var.set(rid)
    try:
        response = await call_next(request)
        return response
    finally:
        request_id_var.reset(token)
