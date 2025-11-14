"""RAG (Retrieval-Augmented Generation) service."""

from typing import List, Dict, Tuple
from google import genai
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
        model_name: str = "gemini-2.0-flash-exp",
        temperature: float = 0.1,
        max_tokens: int = 512
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.query_rewriter = query_rewriter
        
        self.client = genai.Client(api_key=gemini_api_key)
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def retrieve_context(
        self,
        query: str,
        top_k: int = 3,
        score_threshold: float = 0.5
    ) -> Tuple[List[Dict], str]:
        """Retrieve relevant context for a query."""
        rewritten_query = self.query_rewriter.rewrite_query(query, expand=True)
        query_embedding = self.embedding_service.embed_single(rewritten_query)
        
        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            score_threshold=score_threshold
        )
        
        return results, rewritten_query
    
    def format_context(self, retrieved_chunks: List[Dict]) -> str:
        """Format retrieved chunks into context string."""
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
        """Generate response using Gemini API with retrieved context."""
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
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
                config=genai.types.GenerateContentConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                )
            )
            
            return response.text.strip()
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "죄송합니다. 답변을 생성하는 중 오류가 발생했습니다."
    
    def calculate_confidence(self, retrieved_chunks: List[Dict]) -> float:
        """Calculate confidence score based on retrieval quality."""
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
        """Main chat function combining retrieval and generation."""
        retrieved_chunks, rewritten_query = self.retrieve_context(
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
                    "metadata": chunk["metadata"]
                }
                for chunk in retrieved_chunks
            ],
            "confidence": confidence,
            "rewritten_query": rewritten_query
        }
