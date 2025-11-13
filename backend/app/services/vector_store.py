"""
Vector store service using Qdrant.

This module handles all interactions with the Qdrant vector database
including indexing and searching.
"""

from typing import List, Dict, Tuple
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)


class VectorStoreService:
    """Service for managing Qdrant vector store operations."""
    
    def __init__(
        self,
        host: str,
        port: int,
        collection_name: str,
        embedding_dimension: int,
        api_key: str = None
    ):
        """
        Initialize Qdrant vector store service.
        
        Args:
            host: Qdrant server host
            port: Qdrant server port
            collection_name: Name of the collection to use
            embedding_dimension: Dimension of embedding vectors
            api_key: Optional API key for Qdrant Cloud
        """
        self.host = host
        self.port = port
        self.collection_name = collection_name
        self.embedding_dimension = embedding_dimension
        
        # Initialize Qdrant client
        if api_key:
            self.client = QdrantClient(url=f"https://{host}", api_key=api_key)
        else:
            self.client = QdrantClient(host=host, port=port)
    
    def create_collection(self, recreate: bool = False) -> bool:
        """
        Create a new collection in Qdrant.
        
        Args:
            recreate: If True, delete existing collection and create new one
            
        Returns:
            True if collection created successfully
        """
        try:
            # Check if collection exists
            collections = self.client.get_collections().collections
            collection_names = [col.name for col in collections]
            
            if self.collection_name in collection_names:
                if recreate:
                    self.client.delete_collection(self.collection_name)
                else:
                    print(f"Collection '{self.collection_name}' already exists")
                    return True
            
            # Create collection
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.embedding_dimension,
                    distance=Distance.COSINE
                )
            )
            
            print(f"Created collection '{self.collection_name}'")
            return True
            
        except Exception as e:
            print(f"Error creating collection: {e}")
            return False
    
    def index_documents(
        self,
        embeddings: np.ndarray,
        chunks: List[Dict[str, any]]
    ) -> bool:
        """
        Index documents into Qdrant collection.
        
        Args:
            embeddings: NumPy array of embeddings (n_docs, embedding_dim)
            chunks: List of chunk dictionaries with metadata
            
        Returns:
            True if indexing successful
        """
        try:
            points = []
            
            for idx, (embedding, chunk) in enumerate(zip(embeddings, chunks)):
                point = PointStruct(
                    id=idx,
                    vector=embedding.tolist(),
                    payload={
                        "chunk_id": chunk["id"],
                        "question": chunk["question"],
                        "answer": chunk["answer"],
                        "content": chunk["content"],
                        "metadata": chunk["metadata"]
                    }
                )
                points.append(point)
            
            # Upload points in batches
            batch_size = 100
            for i in range(0, len(points), batch_size):
                batch = points[i:i + batch_size]
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=batch
                )
            
            print(f"Indexed {len(points)} documents")
            return True
            
        except Exception as e:
            print(f"Error indexing documents: {e}")
            return False
    
    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
        score_threshold: float = 0.0
    ) -> List[Dict[str, any]]:
        """
        Search for similar documents.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of top results to return
            score_threshold: Minimum similarity score threshold
            
        Returns:
            List of search results with scores and metadata
        """
        try:
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding.tolist(),
                limit=top_k,
                score_threshold=score_threshold
            )
            
            results = []
            for hit in search_result:
                result = {
                    "chunk_id": hit.payload["chunk_id"],
                    "question": hit.payload["question"],
                    "answer": hit.payload["answer"],
                    "content": hit.payload["content"],
                    "score": hit.score,
                    "metadata": hit.payload["metadata"]
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            print(f"Error searching: {e}")
            return []
    
    def get_collection_info(self) -> Dict[str, any]:
        """
        Get information about the collection.
        
        Returns:
            Dictionary with collection information
        """
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "name": self.collection_name,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": str(info.status)
            }
        except Exception as e:
            print(f"Error getting collection info: {e}")
            return {}
    
    def health_check(self) -> bool:
        """
        Check if Qdrant server is accessible.
        
        Returns:
            True if server is accessible
        """
        try:
            self.client.get_collections()
            return True
        except Exception as e:
            print(f"Qdrant health check failed: {e}")
            return False
