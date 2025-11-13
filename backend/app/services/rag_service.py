"""
RAG (Retrieval-Augmented Generation) service.

This module orchestrates the entire RAG pipeline:
1. Query rewriting
2. Vector retrieval
3. LLM response generation
"""

from typing import List, Dict, Tuple
import google.generativeai as genai
from .embedding import EmbeddingService
from .vector_store import VectorStoreService
from .query_rewriter import QueryRewriterService


class RAGService:
    """Service orchestrating the complete RAG pipeline."""
    
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStoreService,
        query_rewriter: QueryRewriterService,
        gemini_api_key: str,
        model_name: str = "gemini-1.5-flash",
        temperature: float = 0.1,
        max_tokens: int = 512
    ):
        """
        Initialize RAG service.
        
        Args:
            embedding_service: Service for text embeddings
            vector_store: Vector database service
            query_rewriter: Query rewriting service
            gemini_api_key: Google Gemini API key
            model_name: Name of Gemini model to use
            temperature: LLM temperature parameter
            max_tokens: Maximum tokens to generate
        """
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.query_rewriter = query_rewriter
        
        # Initialize Gemini
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel(model_name)
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def retrieve_context(
        self,
        query: str,
        top_k: int = 3,
        score_threshold: float = 0.5
    ) -> Tuple[List[Dict], str]:
        """
        Retrieve relevant context for a query.
        
        Args:
            query: User's question
            top_k: Number of documents to retrieve
            score_threshold: Minimum similarity score
            
        Returns:
            Tuple of (retrieved_chunks, rewritten_query)
        """
        # Rewrite query for better retrieval
        rewritten_query = self.query_rewriter.rewrite_query(query, expand=True)
        
        # Generate embedding for the rewritten query
        query_embedding = self.embedding_service.embed_single(rewritten_query)
        
        # Search vector database
        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            score_threshold=score_threshold
        )
        
        return results, rewritten_query
    
    def format_context(self, retrieved_chunks: List[Dict]) -> str:
        """
        Format retrieved chunks into context string.
        
        Args:
            retrieved_chunks: List of retrieved chunk dictionaries
            
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
        """
        Generate response using LLM with retrieved context.
        
        Args:
            query: User's question
            context: Retrieved context
            conversation_history: Previous conversation messages
            
        Returns:
            Generated answer string
        """
        # Build the prompt
        system_prompt = """당신은 Perso.ai에 대한 질문에 답변하는 AI 어시스턴트입니다.

[중요 원칙]
1. 반드시 제공된 참고 자료만을 사용하여 답변하세요.
2. 참고 자료에 없는 내용은 추측하거나 만들어내지 마세요.
3. 정확한 답변을 제공할 수 없다면, "제공된 정보에서는 해당 내용을 찾을 수 없습니다"라고 답변하세요.
4. 답변은 친절하고 명확하게 작성하세요.
5. 가능한 경우 참고 자료의 정확한 표현을 사용하세요."""
        
        user_prompt = f"""질문: {query}

{context}

위 참고 자료를 바탕으로 질문에 답변해주세요."""
        
        # Build conversation history if provided
        messages = []
        if conversation_history:
            for msg in conversation_history[-5:]:  # Last 5 messages
                messages.append({
                    "role": msg["role"],
                    "parts": [msg["content"]]
                })
        
        # Add current query
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        try:
            # Generate response
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                )
            )
            
            return response.text.strip()
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "죄송합니다. 답변을 생성하는 중 오류가 발생했습니다."
    
    def calculate_confidence(self, retrieved_chunks: List[Dict]) -> float:
        """
        Calculate confidence score based on retrieval quality.
        
        Args:
            retrieved_chunks: List of retrieved chunks
            
        Returns:
            Confidence score between 0 and 1
        """
        if not retrieved_chunks:
            return 0.0
        
        # Average of top scores
        scores = [chunk["score"] for chunk in retrieved_chunks]
        avg_score = sum(scores) / len(scores)
        
        # Adjust based on number of relevant chunks
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
        """
        Main chat function combining retrieval and generation.
        
        Args:
            query: User's question
            conversation_history: Previous conversation messages
            top_k: Number of documents to retrieve
            score_threshold: Minimum similarity score
            
        Returns:
            Dictionary with answer, retrieved_chunks, and confidence
        """
        # Retrieve relevant context
        retrieved_chunks, rewritten_query = self.retrieve_context(
            query=query,
            top_k=top_k,
            score_threshold=score_threshold
        )
        
        # Format context
        context = self.format_context(retrieved_chunks)
        
        # Generate response
        answer = self.generate_response(
            query=query,
            context=context,
            conversation_history=conversation_history
        )
        
        # Calculate confidence
        confidence = self.calculate_confidence(retrieved_chunks)
        
        return {
            "answer": answer,
            "retrieved_chunks": [
                {
                    "content": chunk["answer"],
                    "score": chunk["score"],
                    "metadata": chunk["metadata"]
                }
                for chunk in retrieved_chunks
            ],
            "confidence": confidence,
            "rewritten_query": rewritten_query
        }
