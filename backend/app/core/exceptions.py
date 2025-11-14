"""Custom exceptions for the application."""


class ApplicationError(Exception):
    """Base exception for application errors."""
    pass


class EmbeddingError(ApplicationError):
    """Exception raised for embedding-related errors."""
    pass


class VectorStoreError(ApplicationError):
    """Exception raised for vector store operations."""
    pass


class LLMError(ApplicationError):
    """Exception raised for LLM operations."""
    pass


class QueryProcessingError(ApplicationError):
    """Exception raised for query processing operations."""
    pass
