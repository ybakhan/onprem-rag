import hashlib
import logging
from pathlib import Path
import pymupdf4llm
from app.core.document_store import persist_document_store
from app.core.ingestion_pipeline import get_ingestion_pipeline

pdf_markdown_reader = pymupdf4llm.LlamaMarkdownReader()

logger = logging.getLogger(__name__)


def index_embed_pdf(path):
    """Index and embed PDF documents from the given path into the vector store."""
    llama_docs = pdf_markdown_reader.load_data(path)

    # Give every document a stable, predictable ID
    for doc in llama_docs:
        content_hash = hashlib.sha256(doc.text.encode("utf-8")).hexdigest()[:16]
        doc.id_ = f"{Path(path).stem}_{content_hash}"

        # Optional: store custom metadata
        doc.metadata["file_name"] = Path(path).name

    # Run the pipeline → returns only **new/updated** nodes, skips unchanged documents, upserts changed ones into ChromaDB
    get_ingestion_pipeline().run(
        documents=llama_docs,
        show_progress=True,
    )

    # After running the pipeline (which may add new docs to docstore) persist updates to disk
    persist_document_store()

    logger.info("Indexed document %s", path)
