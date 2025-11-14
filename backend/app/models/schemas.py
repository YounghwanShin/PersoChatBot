"""Pydantic models for request/response validation."""

from pydantic import BaseModel, Field
from typing import List


class ChatMessage(BaseModel):
    """Single chat message."""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., min_length=1, description="User's question")
    conversation_history: List[ChatMessage] = Field(
        default=[],
        description="Previous conversation history"
    )


class RetrievedChunk(BaseModel):
    """Retrieved knowledge chunk with metadata."""
    content: str = Field(..., description="Chunk content")
    score: float = Field(..., description="Similarity score")
    metadata: dict = Field(default={}, description="Additional metadata")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    answer: str = Field(..., description="Generated answer")
    retrieved_chunks: List[RetrievedChunk] = Field(
        default=[],
        description="Retrieved knowledge chunks used"
    )
    confidence: float = Field(..., description="Response confidence score")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    qdrant_connected: bool
