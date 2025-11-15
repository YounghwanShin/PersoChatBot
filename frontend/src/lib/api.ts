import axios, { AxiosInstance, AxiosError } from 'axios';
import { retryWithBackoff, DEFAULT_RETRY_CONFIG } from './retry';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatRequest {
  message: string;
  conversation_history: ChatMessage[];
}

export interface RetrievedChunk {
  content: string;
  score: number;
  metadata: Record<string, any>;
}

export interface ChatResponse {
  answer: string;
  retrieved_chunks: RetrievedChunk[];
  confidence: number;
}

export interface HealthResponse {
  status: string;
  version: string;
  qdrant_connected: boolean;
}

export class ApiError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public originalError?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError;
    if (axiosError.response) {
      return `Server error: ${axiosError.response.status}`;
    } else if (axiosError.request) {
      return 'No response from server. Please check your connection.';
    }
  }
  return 'An unexpected error occurred.';
}

function getStatusCode(error: unknown): number | undefined {
  if (axios.isAxiosError(error)) {
    return (error as AxiosError).response?.status;
  }
  return undefined;
}

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 120000,
    });
  }

  async sendMessage(
    message: string,
    conversationHistory: ChatMessage[] = []
  ): Promise<ChatResponse> {
    try {
      const response = await retryWithBackoff(
        () => this.client.post<ChatResponse>('/chat/', {
          message,
          conversation_history: conversationHistory,
        }),
        DEFAULT_RETRY_CONFIG
      );

      return response.data;
    } catch (error) {
      console.error('Failed to send message:', error);
      throw new ApiError(
        getErrorMessage(error),
        getStatusCode(error),
        error
      );
    }
  }

  async checkHealth(): Promise<HealthResponse> {
    try {
      const response = await this.client.get<HealthResponse>('/health');
      return response.data;
    } catch (error) {
      console.error('Failed to check health:', error);
      throw new ApiError(
        getErrorMessage(error),
        getStatusCode(error),
        error
      );
    }
  }
}

export const apiClient = new ApiClient();
