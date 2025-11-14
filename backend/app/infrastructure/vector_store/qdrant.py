"""Vector store implementation using Qdrant."""

from typing import List, Optional, Dict, Any
import logging
import numpy as np
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from ...core.interfaces import VectorStoreProtocol

logger = logging.getLogger(__name__)


class QdrantVectorStore(VectorStoreProtocol):
    """Qdrant vector store implementation."""

    def __init__(
        self,
        host: str,
        port: int,
        collection_name: str,
        embedding_dimension: int,
        api_key: Optional[str] = None
    ):
        """Initialize Qdrant vector store.

        Args:
            host: Qdrant server host
            port: Qdrant server port
            collection_name: Name of the collection
            embedding_dimension: Dimension of embedding vectors
            api_key: Optional API key for Qdrant Cloud
        """
        self.collection_name = collection_name
        self.embedding_dimension = embedding_dimension

        # Remove port from host if it's already included
        if ":" in host:
            host = host.split(":")[0]

        try:
            if api_key:
                self.client = QdrantClient(url=f"https://{host}:{port}", api_key=api_key)
            else:
                self.client = QdrantClient(host=host, port=port)
            logger.info(f"Qdrant client initialized: {host}:{port}")
        except Exception as e:
            logger.error(f"Error initializing Qdrant client: {e}")
            raise

    def create_collection(self, recreate: bool = False) -> bool:
        """Create a new collection.

        Args:
            recreate: Whether to recreate if exists

        Returns:
            True if successful
        """
        try:
            collections = self.client.get_collections().collections
            collection_names = [col.name for col in collections]

            if self.collection_name in collection_names:
                if recreate:
                    logger.info(f"Deleting existing collection: {self.collection_name}")
                    self.client.delete_collection(collection_name=self.collection_name)
                else:
                    logger.info(f"Collection already exists: {self.collection_name}")
                    return True

            logger.info(f"Creating collection: {self.collection_name}")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.embedding_dimension,
                    distance=Distance.COSINE
                )
            )
            logger.info(f"Collection created: {self.collection_name}")
            return True
        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            return False

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
        try:
            if len(embeddings) != len(chunks):
                logger.error("Mismatch between embeddings and chunks count")
                return False

            points = []
            for i, (embedding, chunk) in enumerate(zip(embeddings, chunks)):
                point = PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding.tolist() if isinstance(embedding, np.ndarray) else embedding,
                    payload={
                        "question": chunk.get("question", ""),
                        "answer": chunk.get("answer", ""),
                        "category": chunk.get("category", ""),
                        "content": chunk.get("content", "")
                    }
                )
                points.append(point)

            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Indexed {len(points)} documents to {self.collection_name}")
            return True
        except Exception as e:
            logger.error(f"Error indexing documents: {e}")
            return False

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
        try:
            query_vector = query_embedding.tolist() if isinstance(query_embedding, np.ndarray) else query_embedding

            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k,
                score_threshold=score_threshold
            )

            results = []
            for scored_point in search_result:
                result = {
                    "id": scored_point.id,
                    "score": scored_point.score,
                    "question": scored_point.payload.get("question", ""),
                    "answer": scored_point.payload.get("answer", ""),
                    "category": scored_point.payload.get("category", ""),
                    "content": scored_point.payload.get("content", "")
                }
                results.append(result)

            logger.info(f"Found {len(results)} similar documents")
            return results
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return []

    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection.

        Returns:
            Collection metadata
        """
        try:
            info = self.client.get_collection(collection_name=self.collection_name)
            return {
                "name": self.collection_name,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": str(info.status)
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {}

    def health_check(self) -> bool:
        """Check if the vector store is accessible.

        Returns:
            True if healthy
        """
        try:
            self.client.get_collections()
            return True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
