# Perso.ai Knowledge-Based Chatbot

Vector database (Qdrant) 기반 RAG 챗봇 시스템

## Overview

Perso.ai의 Q&A 데이터를 활용하여 Hallucination 없이 정확한 응답을 제공하는 Retrieval-Augmented Generation (RAG) 챗봇입니다.

## Architecture

```
User Query → Query Rewriter → Vector DB Search → 
Top-K Selection → LLM Response Generation → UI Output
```

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Next.js (React)
- **Vector DB**: Qdrant
- **Embedding**: Sentence-Transformers
- **LLM**: Google Gemini API

## Project Structure

```
perso-ai-chatbot/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/
│   │   ├── services/
│   │   └── routers/
│   ├── data/
│   └── scripts/
├── frontend/            # Next.js frontend
│   └── src/
│       ├── app/
│       └── components/
└── docker-compose.yml
```

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Google Gemini API Key

### Installation

```bash
# 1. Environment setup
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# 2. Edit backend/.env and add GEMINI_API_KEY

# 3. Start services
docker-compose up -d

# 4. Preprocess data
docker-compose exec backend python scripts/preprocess_data.py

# 5. Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Qdrant: http://localhost:6333/dashboard
```

### Manual Installation

```bash
# Start Qdrant
docker run -d -p 6333:6333 qdrant/qdrant

# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add GEMINI_API_KEY
python scripts/preprocess_data.py
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

## API Documentation

After starting the backend, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Key Features

- Modular embedding system (easy to switch models)
- Query rewriting for improved retrieval
- Hallucination prevention via vector DB
- ChatGPT-style interface

## Deployment

### Backend (Railway/Render)
Push backend folder to Git repository and configure auto-deployment

### Frontend (Vercel)
Push frontend folder to Git repository and deploy as Next.js project

### Environment Variables
- Backend: GEMINI_API_KEY, QDRANT_HOST, QDRANT_PORT
- Frontend: NEXT_PUBLIC_API_URL

## Evaluation Criteria

- Accuracy (40%): Precise answers from dataset
- Technical Design (30%): Vector DB and embedding architecture
- Completeness (20%): UI/UX and system stability
- Documentation (10%): Technical decision clarity

## License

MIT License
