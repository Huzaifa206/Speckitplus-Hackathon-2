/**
 * API client for chat functionality
 */
import { apiClient } from './api';

interface ChatRequest {
  user_input: string;
  conversation_id?: string;
  user_id: string;
}

interface ChatResponse {
  conversation_id: string;
  response: string;
  tool_calls: Array<any>;
  timestamp: string;
}

interface Conversation {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

interface Message {
  id: number;
  role: string;
  content: string;
  timestamp: string;
  tool_calls?: any[];
}

class ChatApi {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';
  }

  /**
   * Helper function to get auth token
   */
  private getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('auth_token');
    }
    return null;
  }

  /**
   * Send a message to the chat API
   */
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    try {
      const token = this.getToken();

      const response = await fetch(`${this.baseUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  /**
   * Get list of conversations for a user
   */
  async getConversations(userId: string): Promise<Conversation[]> {
    try {
      const token = this.getToken();

      const response = await fetch(`${this.baseUrl}/chat/conversations?user_id=${userId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting conversations:', error);
      throw error;
    }
  }

  /**
   * Get messages for a specific conversation
   */
  async getConversationMessages(conversationId: string, userId: string): Promise<Message[]> {
    try {
      const token = this.getToken();

      const response = await fetch(`${this.baseUrl}/chat/conversations/${conversationId}/messages?user_id=${userId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting conversation messages:', error);
      throw error;
    }
  }
}

export const chatApi = new ChatApi();

export type { ChatRequest, ChatResponse, Conversation, Message };