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
