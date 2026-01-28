# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings using Pydantic BaseSettings."""

    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    CHAT_COMPLETION_HOST: str = "silma-kashif-2b-rag"
    CHAT_COMPLETION_PORT: int = 9091
    CHAT_COMPLETION_MODEL_ID: str = "silma-ai/SILMA-Kashif-2B-Instruct-v1.0"
    CHAT_COMPLETION_TIMEOUT_SECONDS: int = 30
    CHAT_COMPLETION_TEMPERATURE: float = 0.5
    CHAT_COMPLETION_TOP_P: float = 0.95
    CHAT_COMPLETION_MAX_TOKENS: int = 12000
    CHAT_COMPLETION_LOCAL: bool = False
    CHAT_COMPLETION_LANG: str = "en"

    DEVICE: str = "cpu"

    DOCUMENT_STORE_DIR: str = "./storage"

    EMBEDDING_MODEL_ID: str = "Omartificial-Intelligence-Space/AraGemma-Embedding-300m"
    EMBEDDING_MODEL_DIR: str = "/models"
    EMBEDDING_BATCH_SIZE: int = 10  # optimize based on available VRAM
    EMBEDDING_DIMENSION: int = 768
    EMBEDDING_CHUNK_SIZE: int = (
        # If typical question needs 1–2 clear ideas → 400–600 tokens
        # If it needs understanding relationships / reasoning → 700–1200 tokens
        # If it's keyword lookup → 250–450 tokens
        512
    )
    EMBEDDING_CHUNK_OVERLAP: int = 128  # 15–20% of chunk_size is usually good

    SIMILARITY_TOP_K: int = 6  # adjust as needed

    VECTOR_DB_PATH: str = "./storage/chromadb"
    VECTOR_DB_COLLECTION_NAME: str = "collection"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        case_sensitive=False,
    )


settings = Settings()
