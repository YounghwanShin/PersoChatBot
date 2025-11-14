"""Protocol for vector store operations."""

from typing import Protocol, List, Dict, Any
import numpy as np


class VectorStoreProtocol(Protocol):
    """Protocol defining the interface for vector store operations."""

    def create_collection(self, recreate: bool = False) -> bool:
        """Create a new collection.

        Args:
            recreate: Whether to recreate if exists

        Returns:
            True if successful
        """
        ...

    def index_documents(
        self,
        embeddings: np.ndarray,
        chunks: List[Dict[str, Any]]
    ) -> bool:
        """Index documents into the vector store.

        Args:
            embeddings: Document embeddings
            chunks: Document chunks with metadata

        Returns:
            True if successful
        """
        ...

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
        score_threshold: float = 0.0
    ) -> List[Dict[str, Any]]:
        """Search for similar documents.

        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            score_threshold: Minimum similarity score

        Returns:
            List of search results with scores
        """
        ...

    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection.

        Returns:
            Collection metadata
        """
        ...

    def health_check(self) -> bool:
        """Check if the vector store is accessible.

        Returns:
            True if healthy
        """
        ...
