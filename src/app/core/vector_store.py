import logging
from threading import Lock
import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from app.config import settings
from app.core.embedding_model import get_embedding_model

_VECTOR_STORE = None
_LOCK = Lock()

logger = logging.getLogger(__name__)


def get_vector_store():
    """Get or create a ChromaDB vector store instance with thread-safe singleton pattern."""
    global _VECTOR_STORE  # pylint: disable=global-statement

    if _VECTOR_STORE is None:
        with _LOCK:
            if _VECTOR_STORE is None:
                db = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
                chroma_collection = db.get_or_create_collection(
                    settings.VECTOR_DB_COLLECTION_NAME
                )
                _VECTOR_STORE = ChromaVectorStore(chroma_collection=chroma_collection)
                logger.info(
                    "Initialized chroma vector store from %s",
                    settings.VECTOR_DB_PATH,
                )
    return _VECTOR_STORE


def get_vector_store_index():
    """Get a VectorStoreIndex from the vector store with embedding model."""
    return VectorStoreIndex.from_vector_store(
        vector_store=get_vector_store(), embed_model=get_embedding_model()
    )
