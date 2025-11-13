"""Embedding service with pluggable architecture."""

from abc import ABC, abstractmethod
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingModel(ABC):
    """Abstract base class for embedding models."""
    
    @abstractmethod
    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts into embeddings."""
        pass
    
    @abstractmethod
    def get_dimension(self) -> int:
        """Get the dimension of embeddings."""
        pass


class SentenceTransformerEmbedding(EmbeddingModel):
    """Sentence-Transformers based embedding model."""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self._dimension = self.model.get_sentence_embedding_dimension()
    
    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts using Sentence-Transformers."""
        embeddings = self.model.encode(
            texts,
            show_progress_bar=False,
            convert_to_numpy=True
        )
        return embeddings
    
    def get_dimension(self) -> int:
        """Get embedding dimension."""
        return self._dimension


class OpenAIEmbedding(EmbeddingModel):
    """OpenAI embedding model (placeholder for future implementation)."""
    
    def __init__(self, api_key: str, model_name: str = "text-embedding-ada-002"):
        self.api_key = api_key
        self.model_name = model_name
        self._dimension = 1536
    
    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts using OpenAI API."""
        raise NotImplementedError("OpenAI embedding not implemented yet")
    
    def get_dimension(self) -> int:
        """Get embedding dimension."""
        return self._dimension


class EmbeddingService:
    """Service for managing embedding operations."""
    
    def __init__(self, model: EmbeddingModel):
        self.model = model
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """Embed multiple texts."""
        return self.model.encode(texts)
    
    def embed_single(self, text: str) -> np.ndarray:
        """Embed a single text."""
        return self.model.encode([text])[0]
    
    def get_dimension(self) -> int:
        """Get embedding dimension."""
        return self.model.get_dimension()


def create_embedding_service(
    model_type: str = "sentence-transformers",
    model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    **kwargs
) -> EmbeddingService:
    """Factory function to create embedding service."""
    if model_type == "sentence-transformers":
        model = SentenceTransformerEmbedding(model_name)
    elif model_type == "openai":
        api_key = kwargs.get("api_key")
        if not api_key:
            raise ValueError("OpenAI API key required")
        model = OpenAIEmbedding(api_key, model_name)
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    return EmbeddingService(model)
