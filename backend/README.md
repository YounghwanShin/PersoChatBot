# Perso.ai Chatbot - Backend

FastAPI-based RAG (Retrieval-Augmented Generation) chatbot backend

## Quick Start

### 1. Environment Setup

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 2. Environment Variables

```bash
cp .env.example .env
# Edit .env and add GEMINI_API_KEY
```

### 3. Start Qdrant

```bash
docker run -p 6333:6333 qdrant/qdrant
```

### 4. Prepare Data

Place Q&A data file at `data/Q&A.xlsx`

### 5. Preprocess and Index Data

```bash
python scripts/preprocess_data.py
```

### 6. Start Server

```bash
uvicorn app.main:app --reload --port 8000
```

Server runs at http://localhost:8000

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Architecture

```
app/
├── main.py              # FastAPI app entry point
├── config.py            # Configuration management
├── dependencies.py      # Dependency injection
├── models/
│   └── schemas.py       # Pydantic schemas
├── routers/
│   └── chat.py          # Chat API router
└── services/
    ├── preprocessing.py # Data preprocessing
    ├── embedding.py     # Embedding service
    ├── vector_store.py  # Qdrant vector store
    ├── query_rewriter.py# Query rewriting
    └── rag_service.py   # RAG integration
```

## Key Endpoints

### POST /api/v1/chat
Generate answer for a question

**Request:**
```json
{
  "message": "Perso.ai는 무엇인가요?",
  "conversation_history": []
}
```

**Response:**
```json
{
  "answer": "Perso.ai는...",
  "retrieved_chunks": [...],
  "confidence": 0.85
}
```

### GET /api/v1/health
Check service status

## Module Description

### Embedding Service
- Modular embedding system
- Default: Sentence-Transformers
- Easy to switch to other models (OpenAI, etc.)

### Vector Store Service
- Qdrant vector database management
- Document indexing and similarity search
- Cosine similarity-based retrieval

### Query Rewriter Service
- User query optimization
- Synonym expansion
- Keyword extraction

### RAG Service
- Complete RAG pipeline integration
- Context retrieval
- LLM response generation (Google Gemini)

## Deployment

### Railway
1. Push to GitHub repository
2. Create Railway project
3. Set environment variables
4. Auto-deploy

### Render
1. Connect GitHub repository
2. Create Web Service
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Development Notes

### Code Style
- Follow Google Python Style Guide
- Use type hints
- Include docstrings

### Modularity Principles
- Single Responsibility Principle (SRP)
- Dependency Injection (DI)
- Interface Segregation Principle (ISP)

## Troubleshooting

### Qdrant Connection Failed
```bash
docker ps | grep qdrant
docker restart <container_id>
```

### Embedding Model Download Failed
```bash
echo $HF_HOME
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')"
```
