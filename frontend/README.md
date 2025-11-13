# Perso.ai Chatbot - Frontend

Next.js-based chat interface

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Environment Variables

```bash
cp .env.example .env.local
# Edit NEXT_PUBLIC_API_URL if needed
```

### 3. Start Development Server

```bash
npm run dev
```

Open http://localhost:3000

## Project Structure

```
src/
├── app/
│   ├── page.tsx           # Main page
│   ├── layout.tsx         # Root layout
│   └── globals.css        # Global styles
├── components/
│   └── ChatInterface.tsx  # Chat interface component
└── lib/
    └── api.ts             # API client
```

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **Markdown**: React Markdown

## Key Features

### ChatInterface Component
- ChatGPT-style UI
- Real-time message sending
- Conversation history management
- Loading state display
- Confidence score display

### API Client
- Type safety with TypeScript
- Axios-based HTTP communication
- Error handling
- Timeout configuration

## Component Description

### ChatInterface
Main component for chat interface.

**Features:**
- Message input and sending
- Conversation history display
- Sample questions
- Auto-scroll
- Responsive design

**State Management:**
- `messages`: Chat message list
- `inputMessage`: Message being typed
- `isLoading`: Loading state

## Deployment

### Vercel Deployment

```bash
npm i -g vercel
vercel
```

Or via GitHub:
1. Push to GitHub repository
2. Import project in Vercel
3. Set environment variables
4. Auto-deploy

### Environment Variables (Vercel)
Set the following environment variable during deployment:
- `NEXT_PUBLIC_API_URL`: Backend API URL

## Style Customization

### Tailwind Color Change
Modify primary color in `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Change to desired color
      },
    },
  },
}
```

### Chat Bubble Style
Modify class names in `ChatInterface.tsx`:

```typescript
className={`max-w-2xl px-6 py-4 rounded-2xl ${
  message.role === 'user'
    ? 'bg-primary-500 text-white'
    : 'bg-white border border-gray-200'
}`}
```

## Responsive Design

- Mobile: Vertical layout, adjusted button sizes
- Tablet: Medium-sized layout
- Desktop: Max width constraint (max-w-3xl)

## Troubleshooting

### API Connection Failed
```typescript
// Check baseURL in lib/api.ts
const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
```

### CORS Error
Check backend CORS settings:
```python
# backend/app/config.py
cors_origins: list[str] = [
    "http://localhost:3000",
    "https://your-domain.vercel.app",
]
```

### Build Error
```bash
rm -rf .next
npm run build
```

## Development Guide

### Add New Component
```typescript
// src/components/NewComponent.tsx
'use client';

import React from 'react';

export default function NewComponent() {
  return <div>New Component</div>;
}
```

### Extend API Client
```typescript
// src/lib/api.ts
async newApiMethod(): Promise<ResponseType> {
  const response = await this.client.get<ResponseType>('/endpoint');
  return response.data;
}
```
