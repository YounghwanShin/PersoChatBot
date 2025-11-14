"""Dependency injection container for the application."""

from functools import lru_cache

from ..core.config import settings
from ..core.interfaces import (
    EmbeddingModelProtocol,
    VectorStoreProtocol,
    LLMClientProtocol,
    QueryProcessorProtocol
)
from ..infrastructure.embedding import create_embedding_model
from ..infrastructure.vector_store import create_vector_store
from ..infrastructure.llm import create_llm_client
from ..infrastructure.query_processor import create_query_processor
from ..domain.services import RAGService


@lru_cache()
def get_embedding_model() -> EmbeddingModelProtocol:
    """Get or create embedding model singleton.

    Returns:
        Embedding model instance
    """
    return create_embedding_model(
        api_key=settings.gemini_api_key,
        model_name=settings.embedding_model,
        dimension=settings.embedding_dimension
    )


@lru_cache()
def get_vector_store() -> VectorStoreProtocol:
    """Get or create vector store singleton.

    Returns:
        Vector store instance
    """
    return create_vector_store(
        host=settings.qdrant_host,
        port=settings.qdrant_port,
        collection_name=settings.qdrant_collection_name,
        embedding_dimension=settings.embedding_dimension,
        api_key=settings.qdrant_api_key
    )


@lru_cache()
def get_query_processor_llm() -> LLMClientProtocol:
    """Get or create query processor LLM client singleton.

    Returns:
        LLM client instance for query processing
    """
    return create_llm_client(
        api_key=settings.gemini_api_key,
        model_name=settings.query_rewriter_model,
        temperature=settings.query_rewriter_temperature,
        max_tokens=settings.query_rewriter_max_tokens
    )


@lru_cache()
def get_rag_llm() -> LLMClientProtocol:
    """Get or create RAG LLM client singleton.

    Returns:
        LLM client instance for RAG generation
    """
    return create_llm_client(
        api_key=settings.gemini_api_key,
        model_name=settings.llm_model,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens
    )


@lru_cache()
def get_query_processor() -> QueryProcessorProtocol:
    """Get or create query processor singleton.

    Returns:
        Query processor instance
    """
    llm_client = get_query_processor_llm()
    return create_query_processor(llm_client=llm_client)


@lru_cache()
def get_rag_service() -> RAGService:
    """Get or create RAG service singleton.

    Returns:
        RAG service instance
    """
    embedding_model = get_embedding_model()
    vector_store = get_vector_store()
    query_processor = get_query_processor()
    llm_client = get_rag_llm()

    return RAGService(
        embedding_model=embedding_model,
        vector_store=vector_store,
        query_processor=query_processor,
        llm_client=llm_client
    )
