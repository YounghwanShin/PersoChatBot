# 빠른 시작 가이드 ⚡

Perso.ai 지식 챗봇을 5분 안에 실행하는 방법입니다.

## 🎯 필요한 것

1. **Google Gemini API Key** (필수)
   - https://aistudio.google.com/api-keys 에서 무료 발급
   
2. **Docker** (권장) 또는 Python 3.11+ & Node.js 18+

---

## 🚀 Option 1: Docker로 실행 (가장 쉬움!)

```bash
# 1. 프로젝트 압축 해제
tar -xzf perso-ai-chatbot.tar.gz
cd perso-ai-chatbot

# 2. 환경 변수 설정
cp backend/.env.example backend/.env

# 3. backend/.env 파일 열어서 GEMINI_API_KEY 입력
# GEMINI_API_KEY=your_api_key_here

# 4. 실행 (모든 서비스 자동 시작)
docker-compose up -d

# 5. 데이터 전처리 (최초 1회만)
# Q&A.xlsx 파일을 backend/data/ 폴더에 배치한 후:
docker-compose exec backend python scripts/preprocess_data.py

# 6. 접속!
# 🌐 Frontend: http://localhost:3000
# 🔧 Backend API: http://localhost:8000
# 📊 Qdrant: http://localhost:6333/dashboard
```

---

## 🛠️ Option 2: 수동 설치

### 1단계: Qdrant 실행
```bash
docker run -d -p 6333:6333 qdrant/qdrant
```

### 2단계: 백엔드 실행
```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일에서 GEMINI_API_KEY 입력

# 데이터 준비
# Q&A.xlsx를 data/ 폴더에 배치
python scripts/preprocess_data.py

# 서버 실행
uvicorn app.main:app --reload
```

### 3단계: 프론트엔드 실행 (새 터미널)
```bash
cd frontend

# 의존성 설치
npm install

# 환경 변수 설정
cp .env.example .env.local

# 개발 서버 실행
npm run dev
```

### 4단계: 접속
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

---

## 📊 Q&A 데이터 준비

### 방법 1: CSV를 Excel로 변환
```bash
cd backend/data
# Q&A_sample.csv를 Excel에서 열기
# 다른 이름으로 저장 → Q&A.xlsx
```

### 방법 2: Python으로 변환
```python
import pandas as pd
df = pd.read_csv('backend/data/Q&A_sample.csv')
df.to_excel('backend/data/Q&A.xlsx', index=False)
```

---

## ✅ 테스트

### 백엔드 테스트
```bash
# Health check
curl http://localhost:8000/api/v1/health

# API 문서
open http://localhost:8000/docs
```

### 프론트엔드 테스트
1. http://localhost:3000 접속
2. "Perso.ai는 어떤 서비스인가요?" 질문
3. 응답 확인!

---

## 🆘 문제 해결

### "Qdrant 연결 실패"
```bash
# Qdrant 실행 확인
docker ps | grep qdrant

# 재시작
docker restart <container_id>
```

### "Gemini API 에러"
- API Key가 .env 파일에 올바르게 입력되었는지 확인
- https://aistudio.google.com/api-keys 에서 Key 활성화 확인

### "CORS 에러"
```python
# backend/app/config.py
cors_origins: list[str] = [
    "http://localhost:3000",
    # 프론트엔드 URL 추가
]
```

---

## 📚 더 알아보기

- **전체 문서**: README.md
- **배포 가이드**: DEPLOYMENT.md
- **백엔드 상세**: backend/README.md
- **프론트엔드 상세**: frontend/README.md

---

## 🎉 완료!

챗봇이 실행되었다면:
1. 샘플 질문을 클릭해보세요
2. 직접 질문을 입력해보세요
3. 응답 품질을 확인하세요

문제가 있다면 각 폴더의 README.md를 참고하세요!
