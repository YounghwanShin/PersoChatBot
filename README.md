# Perso.ai Knowledge-Based Chatbot

Vector database를 활용한 RAG 기반 지식 챗봇 시스템

## 프로젝트 설명

Q&A 데이터셋을 기반으로 Hallucination 없이 정확한 응답을 제공하는 RAG(Retrieval-Augmented Generation) 챗봇입니다. 벡터 데이터베이스를 통해 관련 정보를 검색하고, 검색된 컨텍스트를 활용하여 LLM이 정확한 답변을 생성합니다.

## 시스템 아키텍처

```
User Query → Query Rewriter → Vector DB Search → 
Context Retrieval → LLM Generation → Response
```

### 주요 모듈들

1. **Query Rewriter (Gemini)**: Gemini API를 사용하여 사용자 쿼리를 검색에 최적화된 형태로 재작성하는 모듈
2. **Vector Store (Qdrant)**: 문서 임베딩을 저장하고 유사도 검색을 수행하는 모듈
3. **Embedding (Gemini)**: 텍스트를 벡터로 변환하는 모듈
4. **LLM (Gemini)**: 검색된 컨텍스트를 기반으로 답변을 생성하는 모듈

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
   응답 속도가 빠르고 높은 성능을 가지고 있어서 사용하였습니다.
   본래, 임베딩의 경우엔 huggingface에서 모델을 불러와 구현하였지만,
   로컬 모델 로딩과 임베딩 계산시간이 render 무료티어로는 불가능하여 Gemini Embedding API를 사용하게 되었습니다.
   
2. **Qdrant (Vector Database)**
   RAG 시스템에서는 정확한 문맥 검색이 중요하다고 생각합니다.
   이를 위해 고성능 벡터 데이터베이스인 Qdrant를 도입했습니다.
   Qdrant는 대규모 데이터에서도 코사인 유사도 기반의 고속 검색을 지원하며,
   Docker 컨테이너 환경에서의 배포가 매우 용이합니다.
   또한 Python 클라이언트와의 유연한 연동성을 갖추고 있어,
   복잡한 설정 없이도 안정적인 지식 저장소를 구축할 수 있어 채택했습니다.

3. FastAPI (Backend Framework)
   LLM 및 벡터 DB와의 통신 과정에서 발생할 수 있는 지연 시간을 효율적으로 관리하기 위해
   Python의 최신 웹 프레임워크인 FastAPI를 사용했습니다.
   FastAPI는 Async 처리를 기본적으로 지원하여 다수의 요청을 병목 없이 처리할 수 있으며,
   Pydantic을 이용한 데이터 검증과 Swagger UI 자동 생성 기능을 통해
   개발 생산성과 API 신뢰성을 동시에 확보할 수 있었습니다.

4. Next.js 14 & Tailwind CSS (Frontend)
   사용자에게 끊김 없는 채팅 경험을 제공하기 위해 React 기반의 Next.js 14를 프론트엔드 프레임워크로 선정했습니다.
   서버 사이드 렌더링(SSR) 지원으로 초기 로딩 속도를 최적화하였으며,
   TypeScript와 Tailwind CSS를 결합하여 타입 안정성을 보장하면서도 모던하고 반응형인 UI를 구현했습니다.

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
