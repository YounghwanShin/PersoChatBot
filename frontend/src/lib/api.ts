/**
 * API client for communicating with the backend.
 * 
 * This module provides typed functions for making API calls
 * to the FastAPI backend.
 */

import axios, { AxiosInstance } from 'axios';

// Types
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

/**
 * API Client class for backend communication.
 */
class ApiClient {
  private client: AxiosInstance;

  constructor() {
    const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
    
    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000, // 30 seconds
    });
  }

  /**
   * Send a chat message and get a response.
   * 
   * @param message - User's message
   * @param conversationHistory - Previous conversation history
   * @returns Chat response with answer and retrieved chunks
   */
  async sendMessage(
    message: string,
    conversationHistory: ChatMessage[] = []
  ): Promise<ChatResponse> {
    try {
      const response = await this.client.post<ChatResponse>('/chat', {
        message,
        conversation_history: conversationHistory,
      });
      
      return response.data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw new Error('Failed to send message. Please try again.');
    }
  }

  /**
   * Check the health status of the backend.
   * 
   * @returns Health status information
   */
  async checkHealth(): Promise<HealthResponse> {
    try {
      const response = await this.client.get<HealthResponse>('/health');
      return response.data;
    } catch (error) {
      console.error('Error checking health:', error);
      throw new Error('Failed to check backend health.');
    }
  }
}

// Export singleton instance
export const apiClient = new ApiClient();
