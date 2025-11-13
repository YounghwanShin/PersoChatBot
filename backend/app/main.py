"""
FastAPI main application.

This is the entry point for the Perso.ai chatbot backend API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import chat
from .models.schemas import HealthResponse
from .dependencies import get_vector_store

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="벡터 데이터베이스를 활용한 Perso.ai 지식 챗봇 API"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix=settings.api_prefix)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }


@app.get(f"{settings.api_prefix}/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        HealthResponse with service status
    """
    try:
        vector_store = get_vector_store()
        qdrant_connected = vector_store.health_check()
        
        return HealthResponse(
            status="healthy" if qdrant_connected else "degraded",
            version=settings.app_version,
            qdrant_connected=qdrant_connected
        )
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            version=settings.app_version,
            qdrant_connected=False
        )


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    print(f"Starting {settings.app_name} v{settings.app_version}")
    print(f"Qdrant: {settings.qdrant_host}:{settings.qdrant_port}")
    print(f"Collection: {settings.qdrant_collection_name}")
    
    # Verify Qdrant connection
    try:
        vector_store = get_vector_store()
        if vector_store.health_check():
            print("✓ Qdrant connection successful")
            info = vector_store.get_collection_info()
            if info:
                print(f"✓ Collection info: {info}")
        else:
            print("✗ Qdrant connection failed")
    except Exception as e:
        print(f"✗ Error connecting to Qdrant: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    print(f"Shutting down {settings.app_name}")
