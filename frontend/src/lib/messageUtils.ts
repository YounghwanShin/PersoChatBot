import { ApiError } from './api';
import { ERROR_MESSAGES } from './constants';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  confidence?: number;
}

export function createMessage(
  role: 'user' | 'assistant',
  content: string,
  confidence?: number
): Message {
  return {
    id: Date.now().toString() + Math.random(),
    role,
    content,
    timestamp: new Date(),
    confidence,
  };
}

export function getErrorMessage(error: unknown): string {
  if (error instanceof ApiError) {
    if (error.statusCode && error.statusCode >= 500) {
      return ERROR_MESSAGES.SERVER_ERROR;
    } else if (error.statusCode === 429) {
      return ERROR_MESSAGES.RATE_LIMIT;
    }
    return error.message;
  }
  return ERROR_MESSAGES.DEFAULT;
}
