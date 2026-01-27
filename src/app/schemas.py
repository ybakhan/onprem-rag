import logging

from pydantic import BaseModel, Field, field_validator
from .config import settings

logger = logging.getLogger(__name__)

class Message(BaseModel):
    """Message model for chat completion."""
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    """Chat completion request model."""

    messages: list[Message] = Field(..., min_items=1)
    lang: str = "en"
    max_tokens: int = Field(settings.CHAT_COMPLETION_MAX_TOKENS, ge=1)
    temperature: float = Field(settings.CHAT_COMPLETION_TEMPERATURE, ge=0.0, le=2.0)
    top_p: float = Field(settings.CHAT_COMPLETION_TOP_P, ge=0.0, le=1.0)

    @field_validator("messages")
    @classmethod
    def validate_last_message_role(cls, messages: list[Message]) -> list[Message]:
        """Validate that the last message is from the user."""
        
        if messages[-1].role != "user":
            raise ValueError("The last message must be from the user.")
        return messages
