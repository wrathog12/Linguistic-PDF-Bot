"""RAG Service Module

Manages the Qdrant vector store and provides the search_docs tool
for the LangGraph agent to query user-uploaded PDF documents.
"""

import logging
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.tools import tool
from config import (
    EMBEDDING_MODEL_NAME, EMBEDDING_SIZE,
    QDRANT_HOST, QDRANT_PORT, QDRANT_COLLECTION,
)
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.http.exceptions import UnexpectedResponse
from langchain_core.runnables import RunnableConfig
from qdrant_client.models import Filter, FieldCondition, MatchValue

logger = logging.getLogger("voicebot")

# ==================== Embedding Model ====================
embedding_model = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL_NAME,
    model_kwargs={
        "device": "cpu",
        "trust_remote_code": True
    },
    encode_kwargs={
        "normalize_embeddings": True
    }
)

# ==================== Qdrant Client ====================
qdrant_client = QdrantClient(
    host=QDRANT_HOST,
    port=QDRANT_PORT,
)

try:
    qdrant_client.get_collection(collection_name=QDRANT_COLLECTION)
    logger.info(f"Connected to Qdrant collection: {QDRANT_COLLECTION}")
except UnexpectedResponse:
    qdrant_client.create_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=VectorParams(size=EMBEDDING_SIZE, distance=Distance.COSINE),
    )
    logger.info(f"Created new Qdrant collection: {QDRANT_COLLECTION}")

vectorstore = QdrantVectorStore(
    client=qdrant_client,
    collection_name=QDRANT_COLLECTION,
    embedding=embedding_model,
)

# ==================== RAG Tool ====================

@tool
def search_docs(query: str, config: RunnableConfig) -> str:
    """Search the user's uploaded PDF knowledge base for relevant context.

    This tool is called by the LangGraph agent when it determines the user's
    question may be answerable from their uploaded documents.
    """
    userid = config["configurable"].get("thread_id")
    logger.debug(f"RAG search for user {userid[:8]}...: {query[:60]}")

    metadata_filter = Filter(
        should=[
            FieldCondition(
                key="metadata.userid",
                match=MatchValue(value=userid)
            )
        ]
    )
    docs = vectorstore.similarity_search(query, k=4, filter=metadata_filter)

    if not docs:
        logger.debug("No relevant documents found in knowledge base.")
        return "No relevant information found in uploaded documents."

    logger.debug(f"Found {len(docs)} relevant chunks from knowledge base.")
    return "\n\n".join(
        f"[{doc.metadata.get('source', 'Unknown')}]\n{doc.page_content.strip()}"
        for doc in docs
    )
