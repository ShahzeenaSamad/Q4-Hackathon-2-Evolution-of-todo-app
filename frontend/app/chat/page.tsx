'use client';

/**
 * AI Chat Interface for Phase 3
 * Natural language task management
 */

import { useState, useEffect, useRef } from 'react';
import { useAuth } from '@/lib/auth';
import AuthGuard from '@/components/auth-guard';
import { useRouter } from 'next/navigation';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatResponse {
  success: boolean;
  data?: {
    response: string;
    conversation_id: string;
    tool_calls?: Array<{
      tool: string;
      success: boolean;
    }>;
  };
  error?: {
    message: string;
  };
}

export default function ChatPage() {
  const { user } = useAuth();
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const chatApiUrl = process.env.NEXT_PUBLIC_CHAT_API_URL || 'http://localhost:8001';
      const response = await fetch(`${chatApiUrl}/api/v1/chat/${user?.id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage.content,
          conversation_id: conversationId,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ChatResponse = await response.json();

      if (data.success && data.data) {
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: data.data.response,
          timestamp: new Date(),
        };

        setMessages(prev => [...prev, assistantMessage]);

        // Update conversation ID
        if (data.data.conversation_id) {
          setConversationId(data.data.conversation_id);
        }
      } else {
        throw new Error(data.error?.message || 'Failed to get response');
      }
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `Sorry, I encountered an error: ${error instanceof Error ? error.message : 'Unknown error'}`,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const suggestedPrompts = [
    "Add workout",
    "Show my tasks",
    "Complete workout",
    "Delete all groceries",
    "Update meeting to call",
  ];

  return (
    <AuthGuard>
      <div className="min-h-screen" style={{ background: '#000000' }}>
        {/* Header */}
        <header className="sticky top-0 z-50 backdrop-blur-xl border-b border-white/10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex justify-between items-center">
              <div className="flex items-center space-x-4">
                <button
                  onClick={() => router.push('/dashboard')}
                  className="p-2 text-white/60 hover:text-white border border-white/20 hover:border-white/30 rounded-lg transition-all duration-200 hover:bg-white/10"
                  title="Back to Dashboard"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                  </svg>
                </button>
                <div className="rounded-xl p-2.5" style={{ background: 'rgba(0,255,255,0.3)' }}>
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                  </svg>
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-white">AI Assistant</h1>
                  <p className="text-sm text-white/60">
                    Manage tasks with natural language
                  </p>
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Chat Container */}
          <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl flex flex-col" style={{ minHeight: 'calc(100vh - 200px)' }}>
            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              {messages.length === 0 && (
                <div className="text-center py-16">
                  <div className="inline-flex items-center justify-center w-20 h-20 bg-white/10 rounded-full mb-6">
                    <svg className="w-10 h-10" style={{ color: '#00FFFF' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                    </svg>
                  </div>
                  <h2 className="text-2xl font-bold text-white mb-3">
                    AI Task Assistant - Your Smart Todo Manager! 🤖✨
                  </h2>
                  <p className="text-white/60 mb-8 max-w-md mx-auto">
                    Simply type what you want - Add, Show, Complete, Delete, or Update tasks naturally!
                  </p>

                  {/* Suggested Prompts */}
                  <div className="flex flex-wrap justify-center gap-3 max-w-2xl mx-auto">
                    {suggestedPrompts.map((prompt, index) => (
                      <button
                        key={index}
                        onClick={() => setInput(prompt)}
                        className="px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/20 hover:border-white/30 rounded-xl text-white text-sm transition-all duration-200 hover:scale-105"
                      >
                        {prompt}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                      message.role === 'user'
                        ? 'text-black'
                        : 'text-white'
                    }`}
                    style={{
                      background: message.role === 'user'
                        ? 'rgba(0, 255, 255, 0.8)'
                        : 'rgba(255, 255, 255, 0.1)',
                      border: message.role === 'assistant' ? '1px solid rgba(255, 255, 255, 0.2)' : 'none',
                    }}
                  >
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                    <p className="text-xs mt-1 opacity-60">
                      {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </p>
                  </div>
                </div>
              ))}

              {loading && (
                <div className="flex justify-start">
                  <div className="bg-white/10 border border-white/20 rounded-2xl px-4 py-3">
                    <div className="flex items-center space-x-2">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                        <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                        <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                      </div>
                      <span className="text-sm text-white/60">AI is thinking...</span>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="border-t border-white/10 p-4">
              <div className="flex space-x-3">
                <input
                  ref={inputRef}
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Type your message... (e.g., 'Add buy groceries')"
                  disabled={loading}
                  className="flex-1 px-4 py-3 bg-white/5 backdrop-blur-sm border-2 border-white/20 rounded-2xl text-white placeholder-white/40 focus:border-white/30 focus:outline-none transition-all disabled:opacity-50"
                />
                <button
                  onClick={sendMessage}
                  disabled={loading || !input.trim()}
                  className="px-6 py-3 rounded-2xl text-black font-medium transition-all duration-200 hover:scale-105 disabled:opacity-50 disabled:hover:scale-100"
                  style={{ background: '#00FFFF' }}
                >
                  {loading ? (
                    <svg className="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                  ) : (
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                    </svg>
                  )}
                </button>
              </div>
              <p className="text-xs text-white/40 mt-2 text-center">
                Press Enter to send • Try natural language like "Add task for meeting tomorrow"
              </p>
            </div>
          </div>
        </main>
      </div>
    </AuthGuard>
  );
}
