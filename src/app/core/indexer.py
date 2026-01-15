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

    # load document pages
    llama_docs = pdf_markdown_reader.load_data(
        file_path=path,
        embed_images=False,  # No base64 image data inserted into markdown → keeps output clean & small
        ignore_images=True,  # Images are completely ignored during analysis → slightly faster, cleaner text order on image-heavy pages
        write_images=False,  # no image files saved to disk
        show_progress=True,
    )

    file_path = Path(path)
    file_stem = file_path.stem
    file_name = file_path.name

    # Give every page a stable, predictable ID
    for doc in llama_docs:
        content_hash = hashlib.sha256(doc.text.encode("utf-8")).hexdigest()[:16]
        doc.id_ = f"{file_stem}_{content_hash}"

        page = doc.metadata["page"]
        logger.debug("Loaded page %s of document %s with ID %s", page, path, doc.id_)
        # Path(f"{path}-{page}.md").write_bytes(doc.text.encode())

        # Optional: store custom metadata
        doc.metadata["file_name"] = file_name

    # Run the pipeline → returns only **new/updated** nodes, skips unchanged documents, upserts changed ones into ChromaDB
    documents = get_ingestion_pipeline().run(
        documents=llama_docs,
        show_progress=True,
    )

    # After running the pipeline (which may add new docs to docstore) persist updates to disk
    persist_document_store()

    logger.info("Indexed document %s", path)

    return documents
