# Perso.ai Chatbot - Backend

FastAPI 기반 RAG (Retrieval-Augmented Generation) 챗봇 백엔드

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집하여 API 키 입력
# 필수: GEMINI_API_KEY
```

### 3. Qdrant 실행

```bash
# Docker로 Qdrant 실행
docker run -p 6333:6333 qdrant/qdrant
```

### 4. 데이터 준비

Q&A 데이터 파일을 `data/Q&A.xlsx` 경로에 배치합니다.

### 5. 데이터 전처리 및 인덱싱

```bash
python scripts/preprocess_data.py
```

### 6. 서버 실행

```bash
uvicorn app.main:app --reload --port 8000
```

서버가 http://localhost:8000 에서 실행됩니다.

## 📚 API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🏗️ 아키텍처

```
app/
├── main.py              # FastAPI 앱 진입점
├── config.py            # 설정 관리
├── dependencies.py      # 의존성 주입
├── models/
│   └── schemas.py       # Pydantic 스키마
├── routers/
│   └── chat.py          # 채팅 API 라우터
└── services/
    ├── preprocessing.py # 데이터 전처리
    ├── embedding.py     # 임베딩 서비스
    ├── vector_store.py  # Qdrant 벡터 스토어
    ├── query_rewriter.py# 쿼리 재작성
    └── rag_service.py   # RAG 통합 서비스
```

## 🔑 주요 엔드포인트

### POST /api/v1/chat
질문에 대한 답변을 생성합니다.

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
  "answer": "Perso.ai는 이스트소프트가 개발한...",
  "retrieved_chunks": [...],
  "confidence": 0.85
}
```

### GET /api/v1/health
서비스 상태를 확인합니다.

## 🎯 모듈 설명

### Embedding Service
- 모듈화된 임베딩 시스템
- Sentence-Transformers 기본 지원
- OpenAI 등 다른 모델로 쉽게 교체 가능

### Vector Store Service
- Qdrant 벡터 데이터베이스 관리
- 문서 인덱싱 및 유사도 검색
- 코사인 유사도 기반 검색

### Query Rewriter Service
- 사용자 질문 최적화
- 동의어 확장
- 키워드 추출

### RAG Service
- 전체 RAG 파이프라인 통합
- 컨텍스트 검색
- LLM 응답 생성 (Google Gemini)

## 🌐 배포

### Railway 배포

1. GitHub 저장소에 푸시
2. Railway 프로젝트 생성
3. 환경 변수 설정
4. 자동 배포

### Render 배포

1. GitHub 저장소 연결
2. Web Service 생성
3. 빌드 명령: `pip install -r requirements.txt`
4. 시작 명령: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## 📝 개발 노트

### 코드 스타일
- Google Python Style Guide 준수
- Type hints 사용
- Docstring 필수

### 모듈화 원칙
- 단일 책임 원칙 (SRP)
- 의존성 주입 (DI)
- 인터페이스 분리 (ISP)

## 🐛 트러블슈팅

### Qdrant 연결 실패
```bash
# Qdrant가 실행 중인지 확인
docker ps | grep qdrant

# Qdrant 재시작
docker restart <container_id>
```

### 임베딩 모델 다운로드 실패
```bash
# 캐시 디렉토리 확인
echo $HF_HOME

# 수동 다운로드
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')"
```
