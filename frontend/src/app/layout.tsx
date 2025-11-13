/**
 * Root layout for the application.
 * 
 * This layout wraps all pages and provides global styles.
 */

import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Perso.ai 지식 챗봇',
  description: '벡터 데이터베이스를 활용한 Perso.ai 지식기반 챗봇',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
