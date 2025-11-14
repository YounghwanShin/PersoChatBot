"""Chat API router."""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from ..models.schemas import ChatRequest, ChatResponse, RetrievedChunk
from ..services.rag_service import RAGService
from ..dependencies import get_rag_service
from ..config import settings

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    rag_service: RAGService = Depends(get_rag_service)
) -> ChatResponse:
    """Chat endpoint for question answering."""
    try:
        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in request.conversation_history
        ]
        
        result = rag_service.chat(
            query=request.message,
            conversation_history=conversation_history,
            top_k=settings.top_k_retrieval,
            score_threshold=settings.similarity_threshold
        )
        
        retrieved_chunks = [
            RetrievedChunk(
                content=chunk["content"],
                score=chunk["score"],
                metadata=chunk["metadata"]
            )
            for chunk in result["retrieved_chunks"]
        ]
        
        response = ChatResponse(
            answer=result["answer"],
            retrieved_chunks=retrieved_chunks,
            confidence=result["confidence"]
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )


@router.get("/health")
async def health_check(
    rag_service: RAGService = Depends(get_rag_service)
) -> Dict:
    """Health check endpoint for chat service."""
    try:
        is_healthy = rag_service.vector_store.health_check()
        
        return {
            "status": "healthy" if is_healthy else "degraded",
            "vector_store": "connected" if is_healthy else "disconnected"
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
