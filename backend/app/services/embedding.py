"""
Embedding service with pluggable architecture.

This module provides a modular embedding system that allows
easy switching between different embedding models.
"""

from abc import ABC, abstractmethod
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingModel(ABC):
    """Abstract base class for embedding models."""
    
    @abstractmethod
    def encode(self, texts: List[str]) -> np.ndarray:
        """
        Encode texts into embeddings.
        
        Args:
            texts: List of text strings to encode
            
        Returns:
            NumPy array of embeddings
        """
        pass
    
    @abstractmethod
    def get_dimension(self) -> int:
        """
        Get the dimension of embeddings.
        
        Returns:
            Embedding dimension
        """
        pass


class SentenceTransformerEmbedding(EmbeddingModel):
    """Sentence-Transformers based embedding model."""
    
    def __init__(self, model_name: str):
        """
        Initialize Sentence-Transformers model.
        
        Args:
            model_name: Name of the model from Hugging Face
        """
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self._dimension = self.model.get_sentence_embedding_dimension()
    
    def encode(self, texts: List[str]) -> np.ndarray:
        """
        Encode texts using Sentence-Transformers.
        
        Args:
            texts: List of text strings to encode
            
        Returns:
            NumPy array of embeddings
        """
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
    """
    OpenAI embedding model (placeholder for future implementation).
    
    To use OpenAI embeddings, implement this class with:
    - openai.Embedding.create() API calls
    - Proper API key handling
    """
    
    def __init__(self, api_key: str, model_name: str = "text-embedding-ada-002"):
        """
        Initialize OpenAI embedding model.
        
        Args:
            api_key: OpenAI API key
            model_name: Name of the OpenAI embedding model
        """
        self.api_key = api_key
        self.model_name = model_name
        self._dimension = 1536  # ada-002 dimension
    
    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts using OpenAI API."""
        raise NotImplementedError("OpenAI embedding not implemented yet")
    
    def get_dimension(self) -> int:
        """Get embedding dimension."""
        return self._dimension


class EmbeddingService:
    """Service for managing embedding operations."""
    
    def __init__(self, model: EmbeddingModel):
        """
        Initialize embedding service.
        
        Args:
            model: An instance of EmbeddingModel
        """
        self.model = model
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Embed multiple texts.
        
        Args:
            texts: List of text strings
            
        Returns:
            NumPy array of embeddings
        """
        return self.model.encode(texts)
    
    def embed_single(self, text: str) -> np.ndarray:
        """
        Embed a single text.
        
        Args:
            text: Text string to embed
            
        Returns:
            NumPy array of single embedding
        """
        return self.model.encode([text])[0]
    
    def get_dimension(self) -> int:
        """Get embedding dimension."""
        return self.model.get_dimension()


def create_embedding_service(
    model_type: str = "sentence-transformers",
    model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    **kwargs
) -> EmbeddingService:
    """
    Factory function to create embedding service.
    
    Args:
        model_type: Type of embedding model ('sentence-transformers', 'openai', etc.)
        model_name: Name of the specific model
        **kwargs: Additional arguments for model initialization
        
    Returns:
        EmbeddingService instance
        
    Example:
        >>> service = create_embedding_service('sentence-transformers')
        >>> embeddings = service.embed_texts(['Hello', 'World'])
    """
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
