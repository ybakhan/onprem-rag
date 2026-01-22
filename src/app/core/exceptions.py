from app.config import settings

class ChatCompletionError(Exception):
    """General chat completion failure."""
    def __init__(self, status_code: int | None = None, message: str = ""):
        self.status_code = status_code
        self.message = message
        super().__init__(message)


class ChatCompletionTimeoutError(Exception):
    """The model backend did not respond in time."""
    def __init__(self):
        msg = f"Chat completion timed out after {settings.CHAT_COMPLETION_TIMEOUT_SECONDS} seconds"
        super().__init__(msg)


class UnsafePromptDetected(Exception):
    """
    Raised when the prompt fails one or more safety scanners.
    
    Attributes:
        failed_scanners: dict[str, float] - scanners that blocked the prompt (name → risk score)
    """
    def __init__(
        self,
        failed_scanners: dict[str, float],
        message: str = "The prompt was blocked by safety checks"
    ):
        self.failed_scanners = failed_scanners
        self.message = message
        super().__init__(message)
