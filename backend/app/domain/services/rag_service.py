"""RAG (Retrieval-Augmented Generation) service with business logic."""

from typing import List, Dict, Tuple
import numpy as np

from ...core.interfaces import (
    EmbeddingModelProtocol,
    VectorStoreProtocol,
    LLMClientProtocol,
    QueryProcessorProtocol
)


class RAGService:
    """Service orchestrating the complete RAG pipeline."""

    def __init__(
        self,
        embedding_model: EmbeddingModelProtocol,
        vector_store: VectorStoreProtocol,
        query_processor: QueryProcessorProtocol,
        llm_client: LLMClientProtocol
    ):
        """Initialize RAG service.

        Args:
            embedding_model: Model for generating embeddings
            vector_store: Vector store for retrieval
            query_processor: Processor for query rewriting
            llm_client: LLM client for generation
        """
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.query_processor = query_processor
        self.llm_client = llm_client

    def retrieve_context(
        self,
        query: str,
        top_k: int = 3,
        score_threshold: float = 0.5
    ) -> Tuple[List[Dict], str]:
        """Retrieve relevant context for a query.

        Args:
            query: User query
            top_k: Number of results to retrieve
            score_threshold: Minimum similarity threshold

        Returns:
            Tuple of (retrieved chunks, processed query)
        """
        processed_query = self.query_processor.process_query(query)
        query_embedding = self.embedding_model.encode([processed_query])[0]

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            score_threshold=score_threshold
        )

        return results, processed_query

    def format_context(self, retrieved_chunks: List[Dict]) -> str:
        """Format retrieved chunks into context string.

        Args:
            retrieved_chunks: Retrieved document chunks

        Returns:
            Formatted context string
        """
        if not retrieved_chunks:
            return "관련 정보를 찾을 수 없습니다."

        context_parts = []
        for i, chunk in enumerate(retrieved_chunks, 1):
            context_parts.append(
                f"[참고 자료 {i}]\n"
                f"질문: {chunk['question']}\n"
                f"답변: {chunk['answer']}\n"
                f"(유사도: {chunk['score']:.2f})"
            )

        return "\n\n".join(context_parts)

    def generate_response(
        self,
        query: str,
        context: str,
        conversation_history: List[Dict] = None
    ) -> str:
        """Generate response using LLM with retrieved context.

        Args:
            query: User query
            context: Formatted context from retrieval
            conversation_history: Previous conversation (unused in current version)

        Returns:
            Generated answer
        """
        system_prompt = """You are an AI assistant that answers questions about Perso.ai.

Important rules:
1. Use only the provided reference materials to answer.
2. Do not guess or make up information not in the reference materials.
3. If you cannot provide an accurate answer, say "The information is not available in the provided materials."
4. Provide friendly and clear answers.
5. Use the exact expressions from the reference materials when possible."""

        user_prompt = f"""Question: {query}

{context}

Please answer the question based on the above reference materials."""

        full_prompt = f"{system_prompt}\n\n{user_prompt}"

        response = self.llm_client.generate(full_prompt)
        return response

    def calculate_confidence(self, retrieved_chunks: List[Dict]) -> float:
        """Calculate confidence score based on retrieval quality.

        Args:
            retrieved_chunks: Retrieved document chunks

        Returns:
            Confidence score between 0 and 1
        """
        if not retrieved_chunks:
            return 0.0

        scores = [chunk["score"] for chunk in retrieved_chunks]
        avg_score = sum(scores) / len(scores)

        num_relevant = len([s for s in scores if s > 0.7])
        relevance_boost = min(num_relevant * 0.1, 0.3)

        confidence = min(avg_score + relevance_boost, 1.0)
        return round(confidence, 2)

    def chat(
        self,
        query: str,
        conversation_history: List[Dict] = None,
        top_k: int = 3,
        score_threshold: float = 0.5
    ) -> Dict:
        """Main chat function combining retrieval and generation.

        Args:
            query: User query
            conversation_history: Previous conversation
            top_k: Number of documents to retrieve
            score_threshold: Minimum similarity threshold

        Returns:
            Dictionary with answer, chunks, confidence, and rewritten query
        """
        retrieved_chunks, processed_query = self.retrieve_context(
            query=query,
            top_k=top_k,
            score_threshold=score_threshold
        )

        context = self.format_context(retrieved_chunks)

        answer = self.generate_response(
            query=query,
            context=context,
            conversation_history=conversation_history
        )

        confidence = self.calculate_confidence(retrieved_chunks)

        return {
            "answer": answer,
            "retrieved_chunks": [
                {
                    "content": chunk["answer"],
                    "score": chunk["score"],
                    "metadata": {
                        "question": chunk.get("question", ""),
                        "category": chunk.get("category", "")
                    }
                }
                for chunk in retrieved_chunks
            ],
            "confidence": confidence,
            "rewritten_query": processed_query
        }
