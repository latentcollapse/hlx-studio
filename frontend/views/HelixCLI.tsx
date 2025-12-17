
import React, { useState, useEffect, useRef } from 'react';
import { Terminal, Send, Cpu, Command, ChevronRight, Sparkles, Brain, AlertCircle } from 'lucide-react';
import { askBrain, getBrainStatus, BrainStatus } from '../lib/brain-client';
import { getAIBackendStatus, AIBackendStatus } from '../lib/ai-context';
import AIBackendSettings from '../components/AIBackendSettings';

interface Message {
  id: string;
  sender: 'user' | 'helix' | 'brain';
  text: string;
  timestamp: Date;
  source?: 'command' | 'ai'; // 'command' for HLX commands, 'ai' for Brain responses
}

const HelixCLI: React.FC = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'init',
      sender: 'helix',
      text: 'Helix Studio initialized. HLX Runtime Environment active.\nBrain engaged (Qwen3 8B + RAG).\nWaiting for instructions...',
      timestamp: new Date()
    }
  ]);
  const [aiStatus, setAiStatus] = useState<AIBackendStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);

  // Load AI backend status on mount
  useEffect(() => {
    loadAIStatus();
    const interval = setInterval(loadAIStatus, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadAIStatus = async () => {
    try {
      const status = await getAIBackendStatus();
      setAiStatus(status);
    } catch (error) {
      console.error('Failed to load AI status:', error);
    }
  };

  // Determine if input is asking Brain for help (starts with ? or ! or contains certain keywords)
  const isAIQuery = (text: string): boolean => {
    const lower = text.toLowerCase();
    return (
      text.startsWith('?') ||
      text.startsWith('!') ||
      text.startsWith('explain ') ||
      text.startsWith('debug ') ||
      text.startsWith('help ') ||
      text.startsWith('what is ') ||
      text.startsWith('how do ') ||
      text.startsWith('tell me ') ||
      lower.includes('brain:') ||
      lower.includes('[brain]')
    );
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    setLoading(true);
    const userMsg: Message = {
      id: Date.now().toString(),
      sender: 'user',
      text: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMsg]);
    const userInput = input;
    setInput('');

    const isAI = isAIQuery(userInput);

    if (isAI && aiStatus?.isHealthy) {
      // Query the Brain for AI-powered help
      try {
        // Remove command prefixes for cleaner query
        let query = userInput.replace(/^[?!]\s*/, '');
        query = query.replace(/\[brain\]|brain:/gi, '').trim();

        const response = await askBrain({
          question: query,
          use_rag: true,
          temperature: 0.7,
        });

        const brainMsg: Message = {
          id: (Date.now() + 1).toString(),
          sender: 'brain',
          text: response,
          timestamp: new Date(),
          source: 'ai'
        };
        setMessages(prev => [...prev, brainMsg]);
      } catch (error) {
        const errorMsg: Message = {
          id: (Date.now() + 1).toString(),
          sender: 'helix',
          text: `Brain Error: ${error instanceof Error ? error.message : 'Failed to process query'}`,
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, errorMsg]);
      } finally {
        setLoading(false);
      }
    } else {
      // Standard Helix command response
      setTimeout(() => {
        const responseText = `Received: "${userMsg.text}"\nDispatching to orchestrator... OK.`;
        const helixMsg: Message = {
          id: (Date.now() + 1).toString(),
          sender: 'helix',
          text: responseText,
          timestamp: new Date(),
          source: 'command'
        };
        setMessages(prev => [...prev, helixMsg]);
        setLoading(false);
      }, 600);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-3.5rem)] bg-hlx-bg text-hlx-text font-mono">
      {/* Header with Status and Settings */}
      <div className="border-b border-hlx-border/30 bg-hlx-bg/50 px-8 py-3 flex items-center justify-between flex-shrink-0">
        <div className="flex items-center gap-3">
          <div className="px-3 py-1 rounded-full bg-hlx-surface/30 border border-hlx-border/30 flex items-center gap-2 text-xs text-hlx-muted">
            <Sparkles size={12} className="text-hlx-primary" />
            <span>Conversation Mode</span>
          </div>

          {/* AI Status Indicator */}
          {aiStatus && (
            <div
              className={`px-3 py-1 rounded-full border text-xs font-mono flex items-center gap-2 ${
                aiStatus.isHealthy
                  ? 'bg-green-500/5 border-green-500/30 text-green-400'
                  : 'bg-yellow-500/5 border-yellow-500/30 text-yellow-400'
              }`}
            >
              <div
                className={`w-1.5 h-1.5 rounded-full ${aiStatus.isHealthy ? 'bg-green-400' : 'bg-yellow-400'}`}
              />
              <span>{aiStatus.model || 'Brain'}</span>
            </div>
          )}
        </div>

        {/* Settings Button */}
        <div className="flex items-center gap-2">
          <AIBackendSettings onClose={() => loadAIStatus()} />
        </div>
      </div>

      {/* Main Terminal Area */}
      <div className="flex-1 overflow-y-auto p-8 space-y-6">
        {messages.map(msg => {
          const isBrain = msg.sender === 'brain';
          const isUser = msg.sender === 'user';
          const isHelix = msg.sender === 'helix';

          return (
            <div
              key={msg.id}
              className={`flex gap-4 animate-fade-in ${isUser ? 'max-w-3xl ml-auto flex-row-reverse' : 'max-w-4xl mr-auto'}`}
            >
              <div
                className={`shrink-0 w-8 h-8 rounded-full flex items-center justify-center border ${
                  isBrain
                    ? 'bg-purple-500/10 border-purple-500/30 text-purple-400'
                    : isHelix
                    ? 'bg-hlx-surface border-hlx-border text-hlx-primary'
                    : 'bg-hlx-primary/10 border-hlx-primary/20 text-hlx-primary'
                }`}
              >
                {isBrain ? <Brain size={16} /> : isHelix ? <Cpu size={16} /> : <Command size={16} />}
              </div>
              <div
                className={`rounded-xl p-4 border text-sm leading-relaxed whitespace-pre-wrap shadow-sm ${
                  isBrain
                    ? 'bg-purple-500/5 border-purple-500/20 text-white'
                    : isHelix
                    ? 'bg-hlx-surface/50 border-hlx-border text-hlx-text'
                    : 'bg-hlx-primary/5 border-hlx-primary/10 text-white'
                }`}
              >
                {msg.text}
              </div>
            </div>
          );
        })}

        {/* Loading Indicator */}
        {loading && (
          <div className="flex gap-4 max-w-4xl mr-auto animate-fade-in">
            <div className="shrink-0 w-8 h-8 rounded-full flex items-center justify-center border bg-purple-500/10 border-purple-500/30 text-purple-400">
              <Brain size={16} />
            </div>
            <div className="rounded-xl p-4 border bg-purple-500/5 border-purple-500/20">
              <div className="flex items-center gap-2">
                <div className="flex gap-1">
                  <div className="w-2 h-2 rounded-full bg-purple-400 animate-bounce" style={{ animationDelay: '0ms' }} />
                  <div className="w-2 h-2 rounded-full bg-purple-400 animate-bounce" style={{ animationDelay: '150ms' }} />
                  <div className="w-2 h-2 rounded-full bg-purple-400 animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
                <span className="text-xs text-purple-300 ml-2">Brain processing...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={endRef} />
      </div>

      {/* Input Area */}
      <div className="p-6 border-t border-hlx-border bg-hlx-bg/80 backdrop-blur-sm">
        <div className="max-w-4xl mx-auto space-y-3">
          {/* Help Text */}
          <div className="text-[10px] text-hlx-muted/60 space-y-1">
            <p>
              Prefix with <span className="text-hlx-primary font-mono">?</span> or{' '}
              <span className="text-hlx-primary font-mono">!</span> for Brain assistance. Examples:{' '}
              <span className="text-hlx-primary font-mono">? what is HLX collapse</span> or{' '}
              <span className="text-hlx-primary font-mono">! explain this HLXL code</span>
            </p>
          </div>

          {/* Input Field */}
          <div className="relative">
            <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none">
              <ChevronRight size={18} className="text-hlx-muted" />
            </div>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && !loading && handleSend()}
              placeholder={aiStatus?.isHealthy ? 'Talk to Helix... (prefix with ? for Brain)' : 'Talk to Helix...'}
              disabled={loading}
              className="w-full bg-hlx-surface border border-hlx-border rounded-xl pl-12 pr-12 py-4 text-sm text-white placeholder-hlx-muted focus:outline-none focus:border-hlx-primary/50 focus:ring-1 focus:ring-hlx-primary/50 transition-all shadow-lg disabled:opacity-50"
              autoFocus
            />
            <button
              onClick={handleSend}
              disabled={loading || !input.trim()}
              className="absolute inset-y-2 right-2 px-3 flex items-center justify-center rounded-lg bg-hlx-primary/10 hover:bg-hlx-primary/20 text-hlx-primary transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send size={16} />
            </button>
          </div>

          <div className="text-center text-[10px] text-hlx-muted uppercase tracking-widest opacity-50">
            Press Enter to send
          </div>
        </div>
      </div>

      {/* Settings Modal */}
      {showSettings && (
        <div className="fixed inset-0 z-50">
          <AIBackendSettings onClose={() => setShowSettings(false)} />
        </div>
      )}
    </div>
  );
};

export default HelixCLI;
