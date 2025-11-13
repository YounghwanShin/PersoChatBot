# Perso.ai Knowledge-Based Chatbot

벡터 데이터베이스(Qdrant)를 활용한 지식기반 챗봇 시스템

## 🎯 프로젝트 개요

Perso.ai의 Q&A 데이터를 기반으로 Hallucination 없이 정확한 응답을 제공하는 RAG(Retrieval-Augmented Generation) 챗봇 시스템입니다.

## 🏗️ 시스템 아키텍처

```
사용자 질문 → Query Rewriter → Vector DB 검색 → 
Top-K 선택 → LLM 응답 생성 → UI 출력
```

### 주요 기술 스택

- **Backend**: FastAPI (Python)
- **Frontend**: Next.js (Node.js/React)
- **Vector DB**: Qdrant
- **Embedding**: Sentence-Transformers (모듈화로 교체 가능)
- **LLM**: Google Gemini API

## 📁 프로젝트 구조

```
perso-ai-chatbot/
├── backend/              # FastAPI 백엔드
│   ├── app/
│   │   ├── main.py      # FastAPI 메인 앱
│   │   ├── config.py    # 설정 관리
│   │   ├── models/      # Pydantic 스키마
│   │   ├── services/    # 비즈니스 로직
│   │   └── routers/     # API 라우터
│   ├── data/            # Q&A 데이터
│   └── requirements.txt
├── frontend/            # Next.js 프론트엔드
│   ├── src/
│   │   ├── app/        # Next.js 앱 라우터
│   │   └── components/ # React 컴포넌트
│   └── package.json
└── README.md
```

## 🚀 설치 및 실행

### 1. Backend 설정

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# .env 파일 생성 및 설정
cp .env.example .env
# .env 파일에 API 키 입력
```

### 2. Frontend 설정

```bash
cd frontend
npm install

# .env.local 파일 생성
cp .env.example .env.local
```

### 3. Qdrant 실행 (Docker)

```bash
docker run -p 6333:6333 qdrant/qdrant
```

### 4. 데이터 전처리 및 임베딩

```bash
cd backend
python -m app.scripts.preprocess_data
```

### 5. 서버 실행

**Backend:**
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm run dev
```

## 🌐 배포

### Backend (Railway/Render)
- `backend` 폴더를 Git 저장소에 푸시
- Railway/Render에서 자동 배포 설정

### Frontend (Vercel)
- `frontend` 폴더를 Git 저장소에 푸시
- Vercel에서 Next.js 프로젝트로 배포

## 📊 평가 기준

- **정확성 (40%)**: 데이터셋 내 답변 정확 반환
- **기술 설계 (30%)**: Vector DB 및 임베딩 구조
- **완성도 (20%)**: UI/UX 및 시스템 안정성
- **문서/논리성 (10%)**: 기술 선택 이유 명확성

## 🔑 주요 특징

1. **모듈화된 임베딩 시스템**: 임베딩 모델 쉽게 교체 가능
2. **Query Rewriter**: 사용자 질문을 검색에 최적화
3. **Hallucination 방지**: 벡터 DB 기반 정확한 응답
4. **직관적인 UI**: ChatGPT 스타일 인터페이스

## 📝 라이선스

MIT License
