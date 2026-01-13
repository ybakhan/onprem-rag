from threading import Lock
import logging
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from app.config import settings


_EMBED_MODEL = None
_LOCK = Lock()

logger = logging.getLogger(__name__)


def get_embedding_model():
    """Get or create a HuggingFace embedding model instance with thread-safe singleton pattern."""
    global _EMBED_MODEL  # pylint: disable=global-statement
    if _EMBED_MODEL is None:
        with _LOCK:
            if _EMBED_MODEL is None:
                _EMBED_MODEL = HuggingFaceEmbedding(
                    model_name=settings.EMBEDDING_MODEL_ID,
                    max_length=settings.EMBEDDING_DIMENSION,
                    embed_batch_size=settings.EMBEDDING_BATCH_SIZE,
                    device=settings.DEVICE,
                    normalize=True,
                    trust_remote_code=True,  # google/embeddinggemma-300m Uses custom model code executed locally when the model is loaded
                    show_progress_bar=True,
                )
                logger.info(
                    "Initialized embedding model %s", settings.EMBEDDING_MODEL_ID
                )

    return _EMBED_MODEL
