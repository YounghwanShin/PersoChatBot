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
