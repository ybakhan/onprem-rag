
import uvicorn

from pydantic import ValidationError
from fastapi import FastAPI, Request
from .config import settings
from .routes import router
from .middleware import add_request_id
from .errors import validation_error_handler, value_error_handler, general_exception_handler

app = FastAPI(
    title="Chat Completion API",
    description="OpenAI-compatible chat completion endpoint",
    version="0.1.0",
    # docs_url="/docs", # Swagger UI
)

app.include_router(router, prefix="/v1")

# Register exception handlers
app.exception_handler(ValidationError)(validation_error_handler)
app.exception_handler(ValueError)(value_error_handler)
app.exception_handler(Exception)(general_exception_handler)

@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    """Add request ID middleware."""
    return await add_request_id(request, call_next)

if __name__ == "__main__":
    uvicorn.run(
        "app.app:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,   # Auto-reload for development (set to False in production)
        log_level="info"
    )
