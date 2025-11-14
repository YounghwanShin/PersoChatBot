"""Protocol for embedding models."""

from typing import Protocol, List
import numpy as np


class EmbeddingModelProtocol(Protocol):
    """Protocol defining the interface for embedding models."""

    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts into embeddings.

        Args:
            texts: List of text strings to encode

        Returns:
            Array of embeddings
        """
        ...

    def get_dimension(self) -> int:
        """Get the dimension of embeddings.

        Returns:
            Embedding dimension
        """
        ...
