
import React, { useState, useEffect, useRef } from 'react';
import { Terminal, Plus, Square, Circle } from 'lucide-react';

interface TerminalLine {
  text: string;
  color: string;
}

interface Session {
  id: string;
  name: string;
  active: boolean;
  lines: TerminalLine[];
  booted: boolean;
  loggedIn: boolean;
}

const TTY1: React.FC = () => {
  const [sessions, setSessions] = useState<Session[]>([
    { id: '1', name: 'New Session', active: true, lines: [], booted: false, loggedIn: false }
  ]);
  const [activeSessionId, setActiveSessionId] = useState('1');
  const [input, setInput] = useState('');
  const [linkMode, setLinkMode] = useState<'SIMULATION' | 'BRIDGE'>('SIMULATION');
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const activeSession = sessions.find(s => s.id === activeSessionId);

  // Boot sequence on session activation
  useEffect(() => {
    if (activeSession && !activeSession.booted) {
      bootSession(activeSessionId);
    }
  }, [activeSessionId]);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [activeSession?.lines]);

  const bootSession = (sessionId: string) => {
    const bootSequence = [
      { delay: 100, text: '[    0.000000] Linux version 6.8.9-helinux (architect@helix) (gcc (GCC) 13.2.1 20230801) #1 SMP PREEMPT_DYNAMIC', color: 'text-green-400' },
      { delay: 200, text: '[    0.000211] Command line: BOOT_IMAGE=/vmlinuz-linux root=UUID=helix-core rw quiet splash', color: 'text-green-400' },
      { delay: 300, text: '[    0.043220] Kernel command line: BOOT_IMAGE=/vmlinuz-linux root=UUID=helix-core rw quiet splash', color: 'text-green-400' },
      { delay: 400, text: '[    0.210032] Run /init as init process', color: 'text-green-400' },
      { delay: 600, text: '' },
      { delay: 700, text: '[  OK  ] Started Helix Runtime Bridge.', color: 'text-green-400' },
      { delay: 800, text: '[  OK  ] Reached target Local File Systems.', color: 'text-green-400' },
      { delay: 900, text: '[  OK  ] Started Network Manager.', color: 'text-green-400' },
      { delay: 1000, text: '[  OK  ] Reached target Multi-User System.', color: 'text-green-400' },
      { delay: 1100, text: '[  OK  ] Started Helix Studio TUI Service.', color: 'text-green-400' },
      { delay: 1300, text: '' },
      { delay: 1400, text: 'Arch Linux 6.8.9-helinux (tty1)', color: 'text-cyan-400' },
      { delay: 1500, text: '' },
      { delay: 1600, text: 'helinux login: architect', color: 'text-white' },
      { delay: 1700, text: 'Password:', color: 'text-white' },
      { delay: 2000, text: '' },
      { delay: 2100, text: 'Last login: Sun Dec  7 04:20:00 on tty1', color: 'text-gray-400' },
    ];

    bootSequence.forEach(({ delay, text, color }) => {
      setTimeout(() => {
        setSessions(prev => prev.map(s =>
          s.id === sessionId
            ? { ...s, lines: [...s.lines, { text, color: color || 'text-gray-300' }] as TerminalLine[] }
            : s
        ));
      }, delay);
    });

    setTimeout(() => {
      setSessions(prev => prev.map(s =>
        s.id === sessionId ? { ...s, booted: true, loggedIn: true } : s
      ));
    }, 2200);
  };

  const handleCommand = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && input.trim() && activeSession?.loggedIn) {
      const cmd = input.trim();
      const newLines: TerminalLine[] = [...activeSession.lines, { text: `[architect@helinux ~]$ ${cmd}`, color: 'text-cyan-400' }];

      let output = '';
      if (cmd === 'uname -a') {
        output = 'Linux helinux 6.8.9-helinux x86_64 GNU/Linux';
      } else if (cmd === 'whoami') {
        output = 'architect';
      } else if (cmd === 'pwd') {
        output = '/home/architect';
      } else if (cmd === 'ls') {
        output = 'Documents  Downloads  helix-studio  .hlx';
      } else if (cmd === 'neofetch') {
        output = `                   -\`                    architect@helinux
                  .o+\`                   -----------------
                 \`ooo/                   OS: Arch Helinux x86_64
                \`+oooo:                  Kernel: 6.8.9-helinux
               \`+oooooo:                 Shell: hlx-sh 1.0
               -+oooooo+:                Terminal: TTY1
             \`/:-:++oooo+:               CPU: HLX Virtual (4) @ 3.50GHz
            \`/++++/+++++++:              Memory: 128MiB / 4096MiB
           \`/++++++++++++++:
          \`/+++ooooooooooooo/\`
         ./ooosssso++osssssso+\`
        .oossssso-\`\`\`\`/ossssss+\`
       -osssssso.      :ssssssso.
      :osssssss/        osssso+++.
     /ossssssss/        +ssssooo/-
   \`/ossssso+/:-        -:/+osssso+-
  \`+sso+:-\`                 \`.-/+oso:
 \`++:.                           \`-/+/
 .\`                                 \`/`;
      } else if (cmd === 'pacman -Syu') {
        output = ':: Synchronizing package databases...\n core is up to date\n extra is up to date\n:: Starting full system upgrade...\n there is nothing to do';
      } else if (cmd === 'make') {
        output = 'make: *** No targets specified and no makefile found. Stop.';
      } else if (cmd === 'clear') {
        setSessions(prev => prev.map(s =>
          s.id === activeSessionId ? { ...s, lines: [] } : s
        ));
        setInput('');
        return;
      } else if (cmd === 'exit') {
        setSessions(prev => prev.map(s =>
          s.id === activeSessionId ? { ...s, loggedIn: false, lines: [...newLines, { text: 'logout', color: 'text-gray-500' }] } : s
        ));
        setInput('');
        return;
      } else {
        output = `bash: ${cmd}: command not found`;
      }

      if (output) {
        newLines.push({ text: output, color: 'text-gray-300' });
      }

      setSessions(prev => prev.map(s =>
        s.id === activeSessionId ? { ...s, lines: newLines } : s
      ));
      setInput('');
    }
  };

  const createNewSession = () => {
    const newId = (sessions.length + 1).toString();
    setSessions(prev => [...prev, {
      id: newId,
      name: 'New Session',
      active: false,
      lines: [],
      booted: false,
      loggedIn: false
    }]);
    setActiveSessionId(newId);
  };

  return (
    <div className="flex h-[calc(100vh-3.5rem)] bg-hlx-bg text-hlx-text font-sans">
      {/* Sessions Sidebar */}
      <div className="w-56 border-r border-hlx-border flex flex-col bg-hlx-panel/30">
        <div className="p-4 border-b border-hlx-border flex items-center gap-2">
          <Terminal size={18} className="text-hlx-primary" />
          <span className="font-bold text-white tracking-wide text-sm">SESSIONS</span>
        </div>

        <div className="p-3 flex-1">
          <div className="flex items-center gap-2 text-hlx-muted mb-3">
            <Square size={14} className="opacity-50" />
            <Circle size={14} className="opacity-50" />
            <Circle size={14} className="opacity-50" />
          </div>

          <div className="space-y-2">
            {sessions.map(session => (
              <button
                key={session.id}
                onClick={() => setActiveSessionId(session.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs font-medium transition-all ${
                  activeSessionId === session.id
                    ? 'bg-hlx-primary/20 text-white border border-hlx-primary/30'
                    : 'text-hlx-muted hover:text-white hover:bg-white/5 border border-transparent'
                }`}
              >
                <Square size={14} className={activeSessionId === session.id ? 'text-hlx-primary' : ''} />
                {session.name}
              </button>
            ))}
          </div>
        </div>

        <div className="p-3 border-t border-hlx-border">
          <button
            onClick={createNewSession}
            className="w-full flex items-center justify-center gap-2 px-3 py-2.5 rounded-lg text-xs font-medium bg-hlx-surface border border-hlx-border text-hlx-muted hover:text-white hover:border-hlx-primary/30 transition-all"
          >
            <Plus size={14} />
            NEW THREAD
          </button>
        </div>
      </div>

      {/* Terminal */}
      <div className="flex-1 flex flex-col bg-black">
        {activeSession && (
          <>
            <div
              className="flex-1 p-4 overflow-y-auto font-mono text-sm cursor-text"
              onClick={() => inputRef.current?.focus()}
            >
              {activeSession.lines.map((line, i) => (
                <div key={i} className={`whitespace-pre-wrap ${line.color || 'text-gray-300'}`}>
                  {line.text}
                </div>
              ))}

              {activeSession.loggedIn && (
                <div className="flex items-center">
                  <span className="text-cyan-400">[architect@helinux ~]$</span>
                  <input
                    ref={inputRef}
                    type="text"
                    className="flex-1 bg-transparent border-none outline-none ml-2 text-gray-300 font-mono"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleCommand}
                    autoFocus
                  />
                </div>
              )}

              <div ref={scrollRef} />
            </div>

            {/* Status Bar */}
            <div className="h-6 bg-[#111] border-t border-[#333] flex items-center justify-between px-4 text-[10px] font-mono text-gray-500">
              <span>/DEV/TTY1</span>
              <button
                onClick={() => setLinkMode(m => m === 'SIMULATION' ? 'BRIDGE' : 'SIMULATION')}
                className="hover:text-white transition-colors"
              >
                LINK: {linkMode}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default TTY1;
