# Perso.ai Chatbot - Backend

FastAPI 기반 RAG 챗봇 백엔드

## 실행 방법

### 1. 환경 설정

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 환경 변수

```bash
cp .env.example .env
# .env 파일에서 GEMINI_API_KEY 설정
```

### 3. Qdrant 시작

```bash
docker run -p 6333:6333 qdrant/qdrant
```

### 4. 데이터 준비

`data/Q&A.xlsx` 파일을 준비합니다.

### 5. 데이터 전처리 및 인덱싱

```bash
python scripts/preprocess_data.py
```

### 6. 서버 시작

```bash
uvicorn app.main:app --reload --port 8000
```

서버는 http://localhost:8000 에서 실행됩니다.

## API 문서

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 아키텍처

```
app/
├── main.py              # FastAPI 엔트리포인트
├── config.py            # 설정 관리
├── dependencies.py      # 의존성 주입
├── models/
│   └── schemas.py       # Pydantic 스키마
├── routers/
│   └── chat.py          # 채팅 API 라우터
└── services/
    ├── preprocessing.py # 데이터 전처리
    ├── embedding.py     # 임베딩 서비스 (Gemini)
    ├── vector_store.py  # Qdrant 벡터 저장소
    ├── query_rewriter.py# 쿼리 재작성
    └── rag_service.py   # RAG 통합 서비스
```

## 주요 엔드포인트

### POST /api/v1/chat
질문에 대한 답변 생성

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

## 모듈 설명

### Embedding Service
- Gemini API를 사용한 텍스트 임베딩
- 모듈화된 설계로 다른 임베딩 모델로 교체 가능

### Vector Store Service
- Qdrant 벡터 데이터베이스 관리
- 문서 인덱싱 및 유사도 검색
- Cosine similarity 기반 검색

### Query Rewriter Service
- Gemini API를 사용한 지능형 쿼리 재작성
- 동의어 확장 및 검색 최적화
- 빠른 응답을 위한 짧은 토큰 제한

### RAG Service
- 전체 RAG 파이프라인 통합
- 컨텍스트 검색 및 LLM 응답 생성

## 배포

### Railway
1. GitHub 저장소 푸시
2. Railway 프로젝트 생성
3. 환경 변수 설정
4. 자동 배포

### Render
1. GitHub 저장소 연결
2. Web Service 생성
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## 트러블슈팅

### Qdrant 연결 실패
```bash
docker ps | grep qdrant
docker restart <container_id>
```

### API 키 오류
.env 파일에서 GEMINI_API_KEY가 올바르게 설정되었는지 확인
