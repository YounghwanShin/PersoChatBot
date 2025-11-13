# Perso.ai Chatbot - Frontend

Next.js 기반 채팅 인터페이스

## 🚀 빠른 시작

### 1. 의존성 설치

```bash
npm install
```

### 2. 환경 변수 설정

```bash
# .env.local 파일 생성
cp .env.example .env.local

# 필요한 경우 API URL 수정
# NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### 3. 개발 서버 실행

```bash
npm run dev
```

브라우저에서 http://localhost:3000 을 열어 확인합니다.

## 🏗️ 프로젝트 구조

```
src/
├── app/
│   ├── page.tsx           # 메인 페이지
│   ├── layout.tsx         # 루트 레이아웃
│   └── globals.css        # 글로벌 스타일
├── components/
│   └── ChatInterface.tsx  # 채팅 인터페이스 컴포넌트
└── lib/
    └── api.ts             # API 클라이언트
```

## 🎨 기술 스택

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **Markdown**: React Markdown

## 🔑 주요 기능

### ChatInterface 컴포넌트
- ChatGPT 스타일의 UI
- 실시간 메시지 전송
- 대화 이력 관리
- 로딩 상태 표시
- 신뢰도 점수 표시

### API 클라이언트
- TypeScript로 타입 안전성 보장
- Axios 기반 HTTP 통신
- 에러 핸들링
- 타임아웃 설정

## 🎯 컴포넌트 설명

### ChatInterface
채팅 인터페이스의 메인 컴포넌트입니다.

**주요 기능:**
- 메시지 입력 및 전송
- 대화 이력 표시
- 샘플 질문 제공
- 자동 스크롤
- 반응형 디자인

**상태 관리:**
- `messages`: 채팅 메시지 목록
- `inputMessage`: 입력 중인 메시지
- `isLoading`: 로딩 상태

## 🌐 배포

### Vercel 배포

```bash
# Vercel CLI 설치
npm i -g vercel

# 배포
vercel
```

또는 GitHub 연동:
1. GitHub 저장소에 푸시
2. Vercel에서 프로젝트 import
3. 환경 변수 설정
4. 자동 배포

### 환경 변수 (Vercel)
배포 시 다음 환경 변수를 설정하세요:
- `NEXT_PUBLIC_API_URL`: 백엔드 API URL

## 🎨 스타일 커스터마이징

### Tailwind 색상 변경
`tailwind.config.js` 파일에서 primary 색상을 수정:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // 원하는 색상으로 변경
      },
    },
  },
}
```

### 채팅 버블 스타일
`ChatInterface.tsx`에서 클래스명 수정:

```typescript
className={`max-w-2xl px-6 py-4 rounded-2xl ${
  message.role === 'user'
    ? 'bg-primary-500 text-white'  // 사용자 메시지
    : 'bg-white border border-gray-200'  // AI 응답
}`}
```

## 📱 반응형 디자인

- 모바일: 세로 레이아웃, 버튼 크기 조정
- 태블릿: 중간 크기 레이아웃
- 데스크톱: 최대 너비 제한 (max-w-3xl)

## 🐛 트러블슈팅

### API 연결 실패
```typescript
// lib/api.ts 에서 baseURL 확인
const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
```

### CORS 에러
백엔드의 CORS 설정을 확인하세요:
```python
# backend/app/config.py
cors_origins: list[str] = [
    "http://localhost:3000",
    "https://your-domain.vercel.app",
]
```

### 빌드 에러
```bash
# 캐시 삭제 후 재빌드
rm -rf .next
npm run build
```

## 📝 개발 가이드

### 새 컴포넌트 추가
```typescript
// src/components/NewComponent.tsx
'use client';

import React from 'react';

export default function NewComponent() {
  return <div>New Component</div>;
}
```

### API 클라이언트 확장
```typescript
// src/lib/api.ts
async newApiMethod(): Promise<ResponseType> {
  const response = await this.client.get<ResponseType>('/endpoint');
  return response.data;
}
```
