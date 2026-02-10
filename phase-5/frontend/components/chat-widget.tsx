import React, { useState, useRef, useEffect } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send, Bot, User } from 'lucide-react';
import { chatApi, Message as ApiMessage } from '@/lib/chat-api';
import { useAuth } from '@/components/auth/auth-context';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  tool_calls?: any[];
}

interface ChatWidgetProps {
  userId?: string;
  onClose?: () => void;
  onTaskChange?: () => void; // Callback when tasks are modified
}

export const ChatWidget: React.FC<ChatWidgetProps> = ({ userId, onClose, onTaskChange }) => {
  const { user } = useAuth(); // Get the current user from auth context
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | undefined>(undefined);
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  // Use the provided userId, or fall back to the authenticated user's ID, or default to 'default_user'
  const effectiveUserId = userId || user?.id || 'default_user';

  // Log for debugging
  useEffect(() => {
    console.log('ChatWidget: Current user:', user);
    console.log('ChatWidget: Effective user ID:', effectiveUserId);
  }, [user, effectiveUserId]);

  // Load conversation history when component mounts
  useEffect(() => {
    loadConversationHistory();
  }, []);

  const loadConversationHistory = async () => {
    try {
      // For now, we'll initialize with a welcome message
      // In a full implementation, we would fetch the latest conversation
      setMessages([
        {
          id: '1',
          role: 'assistant',
          content: 'Hello! I\'m your AI task assistant. You can ask me to add, list, complete, or delete tasks.',
          timestamp: new Date().toISOString()
        }
      ]);
    } catch (error) {
      console.error('Error loading conversation history:', error);
      setMessages([
        {
          id: '1',
          role: 'assistant',
          content: 'Hello! I\'m your AI task assistant. You can ask me to add, list, complete, or delete tasks.',
          timestamp: new Date().toISOString()
        }
      ]);
    }
  };

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    // Add user message to the conversation
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the chat API using our chatApi client
      const response = await chatApi.sendMessage({
        user_input: inputValue,
        user_id: effectiveUserId,
        conversation_id: conversationId
      });

      // Add AI response to the conversation
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.response,
        timestamp: response.timestamp,
        tool_calls: response.tool_calls
      };

      setMessages(prev => [...prev, aiMessage]);
      // Update conversation ID if it changed
      if (response.conversation_id) {
        setConversationId(response.conversation_id);
      }

      // If any tool calls were executed (task added/deleted/completed), notify parent
      if (response.tool_calls && response.tool_calls.length > 0 && onTaskChange) {
        onTaskChange();
      }
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to the conversation
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-grow overflow-y-auto p-4" ref={scrollAreaRef as React.RefObject<HTMLDivElement>} style={{ maxHeight: 'calc(80vh - 150px)' }}>
        <div className="space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg p-3 ${
                  message.role === 'user'
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-muted'
                }`}
              >
                <div className="flex items-start gap-2">
                  {message.role === 'assistant' && (
                    <Bot className="h-4 w-4 mt-0.5 flex-shrink-0" />
                  )}
                  <div className="whitespace-pre-wrap break-words">
                    {message.content}
                  </div>
                  {message.role === 'user' && (
                    <User className="h-4 w-4 mt-0.5 flex-shrink-0" />
                  )}
                </div>
                {message.tool_calls && message.tool_calls.length > 0 && (
                  <div className="mt-2 text-xs opacity-70">
                    <details>
                      <summary>View tool calls</summary>
                      <pre className="mt-2 p-2 bg-background rounded text-xs overflow-x-auto">
                        {JSON.stringify(message.tool_calls, null, 2)}
                      </pre>
                    </details>
                  </div>
                )}
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="max-w-[80%] rounded-lg p-3 bg-muted">
                <div className="flex items-center gap-2">
                  <Bot className="h-4 w-4 mt-0.5" />
                  <div className="animate-pulse">Thinking...</div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="p-4 border-t">
        <div className="flex gap-2">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me to add, list, complete, or delete tasks..."
            disabled={isLoading}
            className="flex-1"
          />
          <Button
            onClick={handleSendMessage}
            disabled={isLoading || !inputValue.trim()}
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
};

export default ChatWidget;