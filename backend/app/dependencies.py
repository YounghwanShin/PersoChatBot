"""
Dependency injection for FastAPI.

This module provides singleton services that are injected into route handlers.
"""

from functools import lru_cache
from .config import settings
from .services.embedding import create_embedding_service
from .services.vector_store import VectorStoreService
from .services.query_rewriter import QueryRewriterService
from .services.rag_service import RAGService


@lru_cache()
def get_embedding_service():
    """Get or create embedding service singleton."""
    return create_embedding_service(
        model_type="sentence-transformers",
        model_name=settings.embedding_model
    )


@lru_cache()
def get_vector_store():
    """Get or create vector store service singleton."""
    return VectorStoreService(
        host=settings.qdrant_host,
        port=settings.qdrant_port,
        collection_name=settings.qdrant_collection_name,
        embedding_dimension=settings.embedding_dimension,
        api_key=settings.qdrant_api_key
    )


@lru_cache()
def get_query_rewriter():
    """Get or create query rewriter service singleton."""
    return QueryRewriterService()


@lru_cache()
def get_rag_service():
    """Get or create RAG service singleton."""
    embedding_service = get_embedding_service()
    vector_store = get_vector_store()
    query_rewriter = get_query_rewriter()
    
    return RAGService(
        embedding_service=embedding_service,
        vector_store=vector_store,
        query_rewriter=query_rewriter,
        gemini_api_key=settings.gemini_api_key,
        model_name=settings.llm_model,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens
    )
