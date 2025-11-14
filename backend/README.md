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
├── main.py                          # FastAPI 엔트리포인트
├── core/                            # 핵심 레이어
│   ├── config.py                    # 설정 관리
│   ├── exceptions.py                # 커스텀 예외
│   └── interfaces/                  # Protocol 기반 인터페이스
├── infrastructure/                  # 인프라 레이어
│   ├── embedding/                   # Gemini 임베딩 구현체
│   ├── llm/                         # Gemini LLM 구현체
│   ├── vector_store/                # Qdrant 구현체
│   └── query_processor/             # 쿼리 재작성 구현체
├── domain/                          # 도메인 레이어
│   ├── models/
│   │   └── schemas.py               # Pydantic 스키마
│   └── services/
│       └── rag_service.py           # RAG 비즈니스 로직
├── application/                     # 응용 레이어
│   └── dependencies.py              # 의존성 주입
├── presentation/                    # 표현 레이어
│   └── routers/
│       └── chat.py                  # 채팅 API 라우터
└── services/
    └── preprocessing.py             # 데이터 전처리 유틸리티
```
