import logging
from llama_index.core.vector_stores import MetadataFilter, MetadataFilters, FilterOperator
from app.core.vector_store import get_vector_store_index
from app.config import settings
from app.core.common import METADATA_FIELD_NAME_LANG

logger = logging.getLogger(__name__)


def query(query_str, lang):
    """Query the vector store index and return relevant context."""

    index = get_vector_store_index()

    retriever = index.as_retriever(
        similarity_top_k=settings.SIMILARITY_TOP_K,
        filters=MetadataFilters(
            filters=[
                MetadataFilter(
                    key=METADATA_FIELD_NAME_LANG,
                    value=lang,          
                    operator=FilterOperator.EQ,
                )
            ]
        )
    )

    nodes = retriever.retrieve(query_str)
    logger.debug("Retrieved %s nodes", len(nodes))

    for node in nodes:
        logger.debug("Score: %.4f", node.score)
        # logger.debug("Chunk text:\n%s", node.node.get_text())
        # logger.debug("Metadata:%s", node.node.metadata[METADATA_FIELD_NAME_LANG])
        # logger.debug("=" * 100)

    # Build context_str — most common style:
    context_str = "\n\n".join([node.node.get_content() for node in nodes])
    # context_str = "\n" + "=" * 100 + "\n".join(node.node.get_content() for node in nodes)

    return context_str
