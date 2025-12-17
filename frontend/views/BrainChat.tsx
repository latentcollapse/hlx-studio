import React, { useState, useEffect, useRef } from 'react';
import { Brain, Send, Trash2, MessageCircle, Activity, Copy, Check } from 'lucide-react';
import { askBrain, getBrainStatus, BrainStatus } from '../lib/brain-client';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const BrainChat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '0',
      role: 'assistant',
      content: 'Hello! I am HLX Brain, an AI assistant specialized in HLX (Helix) development. I can help you understand HLX concepts, explain code, debug issues, and answer questions about the HLX ecosystem. How can I assist you today?',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [useRAG, setUseRAG] = useState(true);
  const [brainStatus, setBrainStatus] = useState<BrainStatus | null>(null);
  const [statusLoading, setStatusLoading] = useState(true);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Fetch brain status on mount
  useEffect(() => {
    const checkStatus = async () => {
      try {
        const status = await getBrainStatus();
        setBrainStatus(status);
      } catch (error) {
        console.error('Failed to fetch brain status:', error);
        setBrainStatus(null);
      } finally {
        setStatusLoading(false);
      }
    };

    checkStatus();
    const interval = setInterval(checkStatus, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, []);

  // Auto-scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Auto-resize textarea
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.style.height = 'auto';
      inputRef.current.style.height = Math.min(inputRef.current.scrollHeight, 120) + 'px';
    }
  }, [input]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading || !brainStatus?.ollama_healthy) return;

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
      const response = await askBrain({
        question: userMessage.content,
        use_rag: useRAG,
        temperature: 0.7,
      });

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `Error: ${error instanceof Error ? error.message : 'Failed to get response from brain'}`,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setMessages([
      {
        id: '0',
        role: 'assistant',
        content: 'Hello! I am HLX Brain, an AI assistant specialized in HLX (Helix) development. I can help you understand HLX concepts, explain code, debug issues, and answer questions about the HLX ecosystem. How can I assist you today?',
        timestamp: new Date(),
      },
    ]);
  };

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopiedId(id);
      setTimeout(() => setCopiedId(null), 2000);
    });
  };

  const formatMessage = (content: string) => {
    // Simple code block detection and formatting
    const parts: (string | React.ReactNode)[] = [];
    const lines = content.split('\n');
    let inCodeBlock = false;
    let codeContent = '';

    lines.forEach((line, idx) => {
      if (line.startsWith('```')) {
        if (inCodeBlock) {
          // End code block
          parts.push(
            <pre key={`code-${idx}`} className="bg-hlx-bg border border-hlx-border rounded p-3 overflow-x-auto my-2 font-mono text-sm text-hlx-text">
              <code>{codeContent}</code>
            </pre>
          );
          codeContent = '';
          inCodeBlock = false;
        } else {
          // Start code block
          inCodeBlock = true;
        }
      } else if (inCodeBlock) {
        codeContent += (codeContent ? '\n' : '') + line;
      } else {
        parts.push(line + '\n');
      }
    });

    return parts;
  };

  const isHealthy = brainStatus?.ollama_healthy === true;

  return (
    <div className="h-[calc(100vh-3.5rem)] flex flex-col bg-hlx-bg text-hlx-text font-sans">
      {/* Header */}
      <div className="border-b border-hlx-border bg-hlx-panel/30 px-6 py-4 flex items-center justify-between flex-shrink-0">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-hlx-primary/10 rounded-lg border border-hlx-primary/20">
            <Brain size={20} className="text-hlx-primary" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white tracking-tight">HLX Brain</h1>
            <p className="text-xs text-hlx-muted">AI Assistant for HLX Development</p>
          </div>
        </div>

        {/* Status Indicator */}
        <div className="flex items-center gap-3">
          {statusLoading ? (
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-hlx-surface border border-hlx-border">
              <div className="w-2 h-2 rounded-full bg-yellow-400 animate-pulse" />
              <span className="text-xs text-hlx-muted font-mono">CHECKING...</span>
            </div>
          ) : isHealthy ? (
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-green-500/10 border border-green-500/30">
              <Activity size={14} className="text-green-400" />
              <span className="text-xs text-green-400 font-mono font-bold">READY</span>
              <span className="text-[10px] text-green-400/70 ml-1">{brainStatus?.model}</span>
            </div>
          ) : (
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-red-500/10 border border-red-500/30">
              <Activity size={14} className="text-red-400" />
              <span className="text-xs text-red-400 font-mono font-bold">OFFLINE</span>
            </div>
          )}

          {/* RAG Toggle */}
          <button
            onClick={() => setUseRAG(!useRAG)}
            className={`px-3 py-1.5 rounded-lg border text-xs font-mono font-bold transition-all ${
              useRAG
                ? 'bg-hlx-primary/10 border-hlx-primary/30 text-hlx-primary'
                : 'bg-hlx-surface border-hlx-border text-hlx-muted hover:text-white hover:border-hlx-border/50'
            }`}
            title={useRAG ? 'RAG Enabled (using context)' : 'RAG Disabled (no context)'}
          >
            RAG: {useRAG ? 'ON' : 'OFF'}
          </button>

          {/* Clear Button */}
          <button
            onClick={handleClear}
            className="p-2 rounded-lg bg-hlx-surface border border-hlx-border text-hlx-muted hover:text-white hover:border-hlx-accent/30 transition-colors"
            title="Clear chat history"
          >
            <Trash2 size={16} />
          </button>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-6 py-6 space-y-4">
        {messages.map((msg, idx) => (
          <div
            key={msg.id}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}
          >
            <div
              className={`max-w-2xl rounded-lg px-4 py-3 relative group ${
                msg.role === 'user'
                  ? 'bg-hlx-primary/20 border border-hlx-primary/30 text-white rounded-br-none'
                  : 'bg-hlx-surface border border-hlx-border text-hlx-text rounded-bl-none'
              }`}
            >
              {/* Message Content */}
              <div className="text-sm leading-relaxed whitespace-pre-wrap break-words">
                {msg.role === 'assistant' ? (
                  <div className="space-y-2">
                    {formatMessage(msg.content)}
                  </div>
                ) : (
                  msg.content
                )}
              </div>

              {/* Timestamp */}
              <div className={`text-[10px] mt-2 ${msg.role === 'user' ? 'text-hlx-primary/60' : 'text-hlx-muted/60'}`}>
                {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </div>

              {/* Copy Button */}
              <button
                onClick={() => copyToClipboard(msg.content, msg.id)}
                className={`absolute top-2 right-2 p-1.5 rounded opacity-0 group-hover:opacity-100 transition-opacity ${
                  msg.role === 'user'
                    ? 'bg-hlx-primary/30 text-hlx-primary hover:bg-hlx-primary/50'
                    : 'bg-hlx-border text-hlx-muted hover:bg-hlx-border/80 hover:text-white'
                }`}
              >
                {copiedId === msg.id ? <Check size={14} /> : <Copy size={14} />}
              </button>
            </div>
          </div>
        ))}

        {/* Loading Indicator */}
        {loading && (
          <div className="flex justify-start animate-fade-in">
            <div className="bg-hlx-surface border border-hlx-border rounded-lg rounded-bl-none px-4 py-3">
              <div className="flex items-center gap-2">
                <div className="flex gap-1">
                  <div className="w-2 h-2 rounded-full bg-hlx-primary animate-bounce" style={{ animationDelay: '0ms' }} />
                  <div className="w-2 h-2 rounded-full bg-hlx-primary animate-bounce" style={{ animationDelay: '150ms' }} />
                  <div className="w-2 h-2 rounded-full bg-hlx-primary animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
                <span className="text-xs text-hlx-muted ml-2">Thinking...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-hlx-border bg-hlx-panel/30 px-6 py-4 flex-shrink-0 sticky bottom-0">
        {/* Status Message */}
        {!isHealthy && (
          <div className="mb-3 p-2 bg-red-500/10 border border-red-500/30 rounded text-xs text-red-400 flex items-center gap-2">
            <MessageCircle size={14} />
            <span>HLX Brain is offline. Please check if the brain service is running.</span>
          </div>
        )}

        {/* Input Form */}
        <form onSubmit={handleSend} className="flex gap-3">
          <div className="flex-1 flex flex-col">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend(e as any);
                }
              }}
              placeholder={isHealthy ? 'Ask me about HLX... (Shift+Enter for new line)' : 'Brain offline...'}
              disabled={loading || !isHealthy}
              className="w-full bg-hlx-bg border border-hlx-border rounded-lg px-4 py-3 text-hlx-text placeholder-hlx-muted/50 focus:outline-none focus:border-hlx-primary/50 focus:ring-1 focus:ring-hlx-primary/20 resize-none disabled:opacity-50 disabled:cursor-not-allowed font-mono text-sm"
              rows={1}
            />
          </div>
          <button
            type="submit"
            disabled={loading || !isHealthy || !input.trim()}
            className={`px-4 py-3 rounded-lg font-bold transition-all flex items-center gap-2 flex-shrink-0 ${
              isHealthy && !loading && input.trim()
                ? 'bg-hlx-primary text-white hover:bg-hlx-primary/90 cursor-pointer'
                : 'bg-hlx-surface text-hlx-muted border border-hlx-border cursor-not-allowed opacity-50'
            }`}
          >
            <Send size={16} />
            <span className="hidden sm:inline">Ask</span>
          </button>
        </form>

        {/* Help Text */}
        <div className="mt-2 text-[10px] text-hlx-muted/60 flex items-center gap-4">
          <span>RAG: Retrieval-Augmented Generation provides context from documentation</span>
          {brainStatus?.rag_documents && (
            <span>{brainStatus.rag_documents} documents in corpus</span>
          )}
        </div>
      </div>
    </div>
  );
};

export default BrainChat;
