"""Dependency injection for FastAPI."""

from functools import lru_cache
from .config import settings
from .services.embedding import create_embedding_service
from .services.vector_store import VectorStoreService
from .services.query_rewriter import QueryRewriterService
from .services.rag_service import RAGService
from .services.llm_client import create_llm_client


@lru_cache()
def get_embedding_service():
    """Get or create embedding service singleton."""
    return create_embedding_service(
        api_key=settings.gemini_api_key,
        model_name=settings.embedding_model,
        dimension=settings.embedding_dimension
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
def get_query_rewriter_llm():
    """Get or create query rewriter LLM client singleton."""
    return create_llm_client(
        api_key=settings.gemini_api_key,
        model_name=settings.query_rewriter_model,
        temperature=settings.query_rewriter_temperature,
        max_tokens=settings.query_rewriter_max_tokens
    )


@lru_cache()
def get_rag_llm():
    """Get or create RAG LLM client singleton."""
    return create_llm_client(
        api_key=settings.gemini_api_key,
        model_name=settings.llm_model,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens
    )


@lru_cache()
def get_query_rewriter():
    """Get or create query rewriter service singleton."""
    llm_client = get_query_rewriter_llm()
    return QueryRewriterService(llm_client=llm_client)


@lru_cache()
def get_rag_service():
    """Get or create RAG service singleton."""
    embedding_service = get_embedding_service()
    vector_store = get_vector_store()
    query_rewriter = get_query_rewriter()
    llm_client = get_rag_llm()

    return RAGService(
        embedding_service=embedding_service,
        vector_store=vector_store,
        query_rewriter=query_rewriter,
        llm_client=llm_client
    )
