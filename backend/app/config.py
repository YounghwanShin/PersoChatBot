"""Configuration management for the Perso.ai chatbot backend."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    app_name: str = "Perso.ai Knowledge Chatbot"
    app_version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # CORS Configuration
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    # Qdrant Configuration
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection_name: str = "perso_ai_qa"
    qdrant_api_key: Optional[str] = None
    
    # Embedding Configuration
    embedding_model: str = "gemini-embedding-001"
    embedding_dimension: int = 768
    
    # Retrieval Configuration
    top_k_retrieval: int = 3
    similarity_threshold: float = 0.5
    
    # LLM Configuration
    gemini_api_key: str
    llm_model: str = "gemini-2.0-flash"
    llm_temperature: float = 0.1
    llm_max_tokens: int = 512

    # Query Rewriter Configuration
    query_rewriter_model: str = "gemini-2.0-flash"
    query_rewriter_temperature: float = 0.3
    query_rewriter_max_tokens: int = 100
    
    # Data Configuration
    data_file: str = "data/Q&A.xlsx"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
