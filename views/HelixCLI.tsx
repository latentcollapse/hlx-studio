
import React, { useState, useEffect, useRef } from 'react';
import { Terminal, Send, Cpu, Command, ChevronRight, Sparkles } from 'lucide-react';

interface Message {
  id: string;
  sender: 'user' | 'helix';
  text: string;
  timestamp: Date;
}

const HelixCLI: React.FC = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'init',
      sender: 'helix',
      text: 'Helix Studio initialized. HLX Runtime Environment active.\nWaiting for instructions...',
      timestamp: new Date()
    }
  ]);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;
    
    const userMsg: Message = {
      id: Date.now().toString(),
      sender: 'user',
      text: input,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMsg]);
    setInput('');

    // Simulated Helix Response
    setTimeout(() => {
      const responseText = `Received: "${userMsg.text}"\nDispatching to orchestrator... OK.`;
      const helixMsg: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'helix',
        text: responseText,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, helixMsg]);
    }, 600);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-3.5rem)] bg-[#020617] text-hlx-text font-mono">
      {/* Main Terminal Area */}
      <div className="flex-1 overflow-y-auto p-8 space-y-6">
        <div className="flex justify-center mb-8">
           <div className="px-4 py-2 rounded-full bg-hlx-surface border border-hlx-border flex items-center gap-2 text-xs text-hlx-muted shadow-lg">
              <Sparkles size={12} className="text-hlx-primary" />
              <span>Conversation Mode Active</span>
           </div>
        </div>
        
        {messages.map(msg => (
          <div key={msg.id} className={`flex gap-4 animate-fade-in ${msg.sender === 'helix' ? 'max-w-4xl mr-auto' : 'max-w-3xl ml-auto flex-row-reverse'}`}>
            <div className={`shrink-0 w-8 h-8 rounded-full flex items-center justify-center border ${msg.sender === 'helix' ? 'bg-hlx-surface border-hlx-border text-hlx-primary' : 'bg-hlx-primary/10 border-hlx-primary/20 text-hlx-primary'}`}>
              {msg.sender === 'helix' ? <Cpu size={16} /> : <Command size={16} />}
            </div>
            <div className={`rounded-xl p-4 border text-sm leading-relaxed whitespace-pre-wrap shadow-sm ${msg.sender === 'helix' ? 'bg-hlx-surface/50 border-hlx-border text-hlx-text' : 'bg-hlx-primary/5 border-hlx-primary/10 text-white'}`}>
              {msg.text}
            </div>
          </div>
        ))}
        <div ref={endRef} />
      </div>

      {/* Input Area */}
      <div className="p-6 border-t border-hlx-border bg-hlx-bg/80 backdrop-blur-sm">
        <div className="max-w-4xl mx-auto relative">
          <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none">
             <ChevronRight size={18} className="text-hlx-muted" />
          </div>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Talk to Helix..."
            className="w-full bg-hlx-surface border border-hlx-border rounded-xl pl-12 pr-12 py-4 text-sm text-white placeholder-hlx-muted focus:outline-none focus:border-hlx-primary/50 focus:ring-1 focus:ring-hlx-primary/50 transition-all shadow-lg"
            autoFocus
          />
          <button 
            onClick={handleSend}
            className="absolute inset-y-2 right-2 px-3 flex items-center justify-center rounded-lg bg-hlx-primary/10 hover:bg-hlx-primary/20 text-hlx-primary transition-colors"
          >
            <Send size={16} />
          </button>
        </div>
        <div className="text-center mt-3 text-[10px] text-hlx-muted uppercase tracking-widest opacity-50">
           Press Enter to send
        </div>
      </div>
    </div>
  );
};

export default HelixCLI;
