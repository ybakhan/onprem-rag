import logging
from threading import Lock
from llama_index.core.ingestion import IngestionPipeline, DocstoreStrategy
from llama_index.core.node_parser import SentenceSplitter
from app.core.embedding_model import get_embedding_model
from app.core.document_store import get_document_store
from app.core.vector_store import get_vector_store
from app.config import settings


_INGESTION_PIPELINE = None
_LOCK = Lock()

logger = logging.getLogger(__name__)


def get_ingestion_pipeline():
    """Get or create an ingestion pipeline instance with thread-safe singleton pattern."""
    global _INGESTION_PIPELINE  # pylint: disable=global-statement

    if _INGESTION_PIPELINE is None:
        with _LOCK:
            if _INGESTION_PIPELINE is None:
                _INGESTION_PIPELINE = IngestionPipeline(
                    transformations=[
                        SentenceSplitter(
                            chunk_size=settings.EMBEDDING_CHUNK_SIZE,
                            chunk_overlap=settings.EMBEDDING_CHUNK_OVERLAP,
                        ),
                        get_embedding_model(),
                    ],
                    docstore=get_document_store(),
                    vector_store=get_vector_store(),
                    docstore_strategy=DocstoreStrategy.UPSERTS,
                )
                logger.info("Initialized document ingestion pipeline")

    return _INGESTION_PIPELINE
