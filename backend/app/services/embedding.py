"""Embedding service using Google Gemini API."""

from abc import ABC, abstractmethod
from typing import List
import numpy as np
from google import genai
from google.genai import types


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


class GeminiEmbedding(EmbeddingModel):
    """Gemini API-based embedding model."""
    
    def __init__(self, api_key: str, model_name: str = "gemini-embedding-001", dimension: int = 768):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self._dimension = dimension
    
    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts using Gemini API."""
        result = self.client.models.embed_content(
            model=self.model_name,
            contents=texts,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=self._dimension
            )
        )
        
        embeddings = np.array([np.array(e.values) for e in result.embeddings])
        return embeddings
    
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
    api_key: str,
    model_name: str = "gemini-embedding-001",
    dimension: int = 768
) -> EmbeddingService:
    """Factory function to create embedding service."""
    model = GeminiEmbedding(api_key=api_key, model_name=model_name, dimension=dimension)
    return EmbeddingService(model)
