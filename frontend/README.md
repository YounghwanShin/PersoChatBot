# Perso.ai Chatbot - Frontend

Next.js 기반 채팅 인터페이스

## 실행 방법

### 1. 종속성 설치

```bash
npm install
```

### 2. 환경 변수

```bash
cp .env.example .env.local
# 필요시 NEXT_PUBLIC_API_URL 수정
```

### 3. 개발 서버 시작

```bash
npm run dev
```

http://localhost:3000 에서 실행됩니다.

## 프로젝트 구조

```
src/
├── app/
│   ├── page.tsx           # 메인 페이지
│   ├── layout.tsx         # 루트 레이아웃
│   └── globals.css        # 전역 스타일
├── components/
│   └── ChatInterface.tsx  # 채팅 인터페이스
└── lib/
    └── api.ts             # API 클라이언트
```

## 기술 스택

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **Markdown**: React Markdown

## 주요 기능

### ChatInterface 컴포넌트
- ChatGPT 스타일 UI
- 실시간 메시지 전송
- 대화 기록 관리
- 로딩 상태 표시
- 신뢰도 점수 표시

### API Client
- TypeScript 타입 안정성
- Axios 기반 HTTP 통신
- 에러 처리
- 타임아웃 설정

## 배포

### Vercel

```bash
npm i -g vercel
vercel
```

또는 GitHub 연동:
1. GitHub 저장소 푸시
2. Vercel에서 프로젝트 임포트
3. 환경 변수 설정
4. 자동 배포

### 환경 변수 (Vercel)
- `NEXT_PUBLIC_API_URL`: 백엔드 API URL

## 트러블슈팅

### API 연결 실패
```typescript
// lib/api.ts에서 baseURL 확인
const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
```

### CORS 오류
백엔드 CORS 설정 확인:
```python
# backend/app/config.py
cors_origins: str = "http://localhost:3000,https://your-domain.vercel.app"
```

### 빌드 오류
```bash
rm -rf .next
npm run build
```
