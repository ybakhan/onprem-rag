import os
import logging
from threading import Lock
from llama_index.core.storage.docstore import SimpleDocumentStore
from app.config import settings


_DOCUMENT_STORE = None
_LOCK = Lock()

document_store_path = os.path.join(settings.DOCUMENT_STORE_DIR, "docstore.json")

logger = logging.getLogger(__name__)


def get_document_store():
    """
    Get or create a document store instance with thread-safe singleton pattern.
    The docstore exists as backup / source of truth, and
    for compatibility with vector DBs that don't store text
    """
    global _DOCUMENT_STORE  # pylint: disable=global-statement

    if _DOCUMENT_STORE is None:
        with _LOCK:
            if _DOCUMENT_STORE is None:
                if os.path.exists(settings.DOCUMENT_STORE_DIR):
                    _DOCUMENT_STORE = SimpleDocumentStore.from_persist_dir(
                        persist_dir=settings.DOCUMENT_STORE_DIR
                    )
                    logger.info(
                        "Initialized docstore from %s", settings.DOCUMENT_STORE_DIR
                    )
                else:
                    logger.info(
                        "Persist directory %s does not exist yet. Creating new docstore.",
                        settings.DOCUMENT_STORE_DIR,
                    )
                    _DOCUMENT_STORE = SimpleDocumentStore()

    return _DOCUMENT_STORE


def persist_document_store():
    """Persist the document store to disk if it exists."""
    if _DOCUMENT_STORE is not None:
        _DOCUMENT_STORE.persist(persist_path=document_store_path)
