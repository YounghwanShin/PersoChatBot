# 배포 가이드

Perso.ai 챗봇 시스템의 배포 방법을 설명합니다.

## 목차
1. [로컬 배포](#로컬-배포)
2. [Railway 배포 (백엔드)](#railway-배포-백엔드)
3. [Vercel 배포 (프론트엔드)](#vercel-배포-프론트엔드)
4. [Qdrant Cloud 사용](#qdrant-cloud-사용)

---

## 로컬 배포

### Docker Compose 사용 (권장)

```bash
# 1. 환경 변수 설정
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# 2. backend/.env 파일 편집 (GEMINI_API_KEY 필수)

# 3. Docker Compose 실행
docker-compose up -d

# 4. 데이터 전처리 (최초 1회)
docker-compose exec backend python scripts/preprocess_data.py

# 5. 접속
# - Frontend: http://localhost:3000
# - Backend: http://localhost:8000
# - Qdrant: http://localhost:6333/dashboard
```

### 수동 설치

```bash
# 1. Qdrant 실행
docker run -d -p 6333:6333 qdrant/qdrant

# 2. 백엔드 실행
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# .env 편집
python scripts/preprocess_data.py
uvicorn app.main:app --reload

# 3. 프론트엔드 실행 (새 터미널)
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

---

## Railway 배포 (백엔드)

Railway는 Python 앱을 쉽게 배포할 수 있는 플랫폼입니다.

### 1. Railway 계정 생성
- https://railway.app 에서 계정 생성
- GitHub 계정으로 로그인

### 2. 새 프로젝트 생성
```bash
# Railway CLI 설치 (선택사항)
npm i -g @railway/cli

# 로그인
railway login

# 프로젝트 초기화
cd backend
railway init
```

### 3. 환경 변수 설정
Railway 대시보드에서 다음 환경 변수 추가:

```
GEMINI_API_KEY=your_gemini_api_key
QDRANT_HOST=your_qdrant_cloud_url
QDRANT_PORT=6333
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=perso_ai_qa
```

### 4. 배포
```bash
# Git으로 배포
git add .
git commit -m "Deploy to Railway"
railway up

# 또는 GitHub 연동
# Railway 대시보드에서 GitHub 저장소 연결
```

### 5. 데이터 전처리
Railway 대시보드에서 Shell을 열어 실행:
```bash
python scripts/preprocess_data.py
```

---

## Vercel 배포 (프론트엔드)

Vercel은 Next.js 앱을 위한 최적의 플랫폼입니다.

### 1. Vercel 계정 생성
- https://vercel.com 에서 계정 생성
- GitHub 계정으로 로그인

### 2. 프로젝트 Import
```bash
# Vercel CLI 설치
npm i -g vercel

# 프론트엔드 폴더에서
cd frontend
vercel
```

또는 웹 UI에서:
1. "New Project" 클릭
2. GitHub 저장소 Import
3. Framework Preset: Next.js 선택
4. Root Directory: `frontend` 설정

### 3. 환경 변수 설정
Vercel 대시보드 → Settings → Environment Variables:

```
NEXT_PUBLIC_API_URL=https://your-backend.railway.app/api/v1
```

### 4. 배포
```bash
# Git push로 자동 배포
git push origin main

# 또는 수동 배포
vercel --prod
```

---

## Qdrant Cloud 사용

로컬 Qdrant 대신 Qdrant Cloud를 사용할 수 있습니다.

### 1. Qdrant Cloud 계정 생성
- https://cloud.qdrant.io 에서 가입
- 무료 티어 사용 가능

### 2. 클러스터 생성
1. "Create Cluster" 클릭
2. 지역 선택 (가까운 지역 권장)
3. 클러스터 이름 입력

### 3. API Key 생성
1. 클러스터 대시보드에서 "API Keys" 탭
2. "Create API Key" 클릭
3. API Key 복사

### 4. 환경 변수 설정
```env
QDRANT_HOST=your-cluster-url.qdrant.io
QDRANT_PORT=6333
QDRANT_API_KEY=your_api_key
```

---

## 배포 후 체크리스트

### 백엔드 확인
- [ ] Health check: `https://your-backend-url/api/v1/health`
- [ ] Qdrant 연결 확인
- [ ] API 문서 접근: `https://your-backend-url/docs`

### 프론트엔드 확인
- [ ] 웹사이트 로딩 확인
- [ ] 채팅 메시지 전송 테스트
- [ ] 샘플 질문 클릭 테스트

### 보안 설정
- [ ] CORS origins 업데이트
- [ ] API Keys 환경 변수로 관리
- [ ] HTTPS 사용 확인

---

## 트러블슈팅

### 백엔드 배포 실패
```bash
# 로그 확인
railway logs

# 또는
heroku logs --tail
```

**일반적인 문제:**
- Python 버전 불일치 → `runtime.txt` 추가
- 의존성 설치 실패 → `requirements.txt` 확인
- 환경 변수 누락 → 대시보드에서 확인

### 프론트엔드 빌드 실패
```bash
# 로컬에서 빌드 테스트
npm run build

# 캐시 삭제
rm -rf .next
rm -rf node_modules
npm install
```

### Qdrant 연결 실패
- 호스트 URL 확인 (https:// 포함 여부)
- API Key 확인
- 방화벽 설정 확인

### CORS 에러
백엔드 `config.py`에서 프론트엔드 URL 추가:
```python
cors_origins: list[str] = [
    "http://localhost:3000",
    "https://your-frontend.vercel.app",
]
```

---

## 비용 최적화

### 무료 티어 활용
- **Qdrant Cloud**: 1GB 무료
- **Railway**: 월 $5 크레딧
- **Vercel**: 무제한 개인 프로젝트
- **Google Gemini**: 무료 티어 사용

### 프로덕션 권장사항
- Qdrant: Cloud 유료 플랜
- Backend: Railway Pro ($20/월)
- Frontend: Vercel Pro ($20/월)
- LLM: Gemini Pro 또는 GPT-4

---

## 모니터링

### 로그 확인
```bash
# Railway
railway logs

# Vercel
vercel logs

# Docker
docker-compose logs -f
```

### 성능 모니터링
- Railway Dashboard
- Vercel Analytics
- Qdrant Dashboard

---

## 업데이트 배포

### 백엔드 업데이트
```bash
cd backend
git pull
railway up
```

### 프론트엔드 업데이트
```bash
cd frontend
git pull
# Vercel은 자동으로 재배포됨
```

### 데이터 업데이트
```bash
# 새로운 Q&A 데이터 추가 후
python scripts/preprocess_data.py
```
