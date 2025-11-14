# Perso.ai Knowledge-Based Chatbot

Vector database를 활용한 RAG 기반 지식 챗봇 시스템

## 프로젝트 설명

Q&A 데이터셋을 기반으로 Hallucination 없이 정확한 응답을 제공하는 RAG(Retrieval-Augmented Generation) 챗봇입니다. 벡터 데이터베이스를 통해 관련 정보를 검색하고, 검색된 컨텍스트를 활용하여 LLM이 정확한 답변을 생성합니다.

## 시스템 아키텍처

```
User Query → Query Rewriter → Vector DB Search → 
Context Retrieval → LLM Generation → Response
```

### 주요 구성요소

1. **Query Rewriter (Gemini)**: Gemini API를 사용하여 사용자 쿼리를 검색에 최적화된 형태로 재작성
2. **Vector Store (Qdrant)**: 문서 임베딩을 저장하고 유사도 검색 수행
3. **Embedding (Gemini)**: 텍스트를 벡터로 변환
4. **LLM (Gemini)**: 검색된 컨텍스트 기반 답변 생성

## 기술 스택

### Backend
- **Framework**: FastAPI
- **Vector DB**: Qdrant
- **Embedding**: Google Gemini Embedding API
- **LLM**: Google Gemini API
- **Language**: Python 3.11

### Frontend
- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS

### 기술 선택 이유

1. **Gemini API (Query Rewriting, Embedding & LLM)**
   - 빠른 응답 속도와 안정적인 성능
   - 무료 티어로 충분한 사용량 제공
   - 로컬 모델 로딩 시간 없이 즉시 사용 가능
   - 배포 환경에서 리소스 부담 최소화
   - LLM 기반 쿼리 재작성으로 검색 정확도 향상

2. **Qdrant**
   - 빠른 벡터 검색 성능
   - 간단한 설치 및 관리
   - Docker 기반 배포 용이

3. **FastAPI**
   - 높은 성능과 간결한 코드
   - 자동 API 문서화
   - 비동기 처리 지원

4. **Next.js**
   - 서버 사이드 렌더링 지원
   - 우수한 개발 경험
   - Vercel 배포 최적화

## 실행 방법

### 1. 사전 요구사항

- Docker & Docker Compose
- Google Gemini API Key ([발급 링크](https://aistudio.google.com/apikey))

### 2. 설치 및 실행

```bash
# 저장소 클론
git clone <repository-url>
cd perso-ai-chatbot

# 환경 변수 설정
cp backend/.env.example backend/.env
# backend/.env 파일에서 GEMINI_API_KEY 설정

# 서비스 시작
docker-compose up -d

# 데이터 전처리 및 인덱싱
docker-compose exec backend python scripts/preprocess_data.py

# 접속
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Qdrant Dashboard: http://localhost:6333/dashboard
```

### 3. 로컬 개발 환경

```bash
# Qdrant 시작
docker run -d -p 6333:6333 qdrant/qdrant

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# .env 파일에서 GEMINI_API_KEY 설정
python scripts/preprocess_data.py
uvicorn app.main:app --reload

# Frontend (새 터미널)
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

## 프로젝트 구조

```
perso-ai-chatbot/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI 엔트리포인트
│   │   ├── config.py            # 설정 관리
│   │   ├── dependencies.py      # 의존성 주입
│   │   ├── models/
│   │   │   └── schemas.py       # API 스키마
│   │   ├── routers/
│   │   │   └── chat.py          # 채팅 라우터
│   │   └── services/
│   │       ├── preprocessing.py # 데이터 전처리
│   │       ├── embedding.py     # 임베딩 서비스
│   │       ├── llm_client.py    # LLM 클라이언트
│   │       ├── vector_store.py  # Qdrant 관리
│   │       ├── query_rewriter.py# 쿼리 최적화
│   │       └── rag_service.py   # RAG 통합
│   ├── scripts/
│   │   └── preprocess_data.py   # 전처리 스크립트
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── app/
│       ├── components/
│       │   └── ChatInterface.tsx
│       └── lib/
│           └── api.ts
└── docker-compose.yml
```

## API 명세

### POST /api/v1/chat
채팅 메시지 전송 및 응답 생성

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
서비스 상태 확인

## 배포

### Backend (Railway/Render)
1. GitHub 저장소 푸시
2. Railway/Render에서 프로젝트 생성
3. 환경 변수 설정 (GEMINI_API_KEY 등)
4. 자동 배포

### Frontend (Vercel)
1. GitHub 저장소 푸시
2. Vercel에서 프로젝트 임포트
3. 환경 변수 설정 (NEXT_PUBLIC_API_URL)
4. 자동 배포

### 필수 환경 변수

**Backend:**
- `GEMINI_API_KEY`: Gemini API 키
- `QDRANT_HOST`: Qdrant 호스트
- `QDRANT_PORT`: Qdrant 포트

**Frontend:**
- `NEXT_PUBLIC_API_URL`: Backend API URL

## 라이선스

MIT License
