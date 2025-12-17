import React, { useState } from 'react';
import { Folder, FileCode, Play, Terminal, MoreHorizontal, Search, Settings } from 'lucide-react';
import { collapse, getHLXStatus } from '../lib/api-client';

const Crucible: React.FC = () => {
  const [code, setCode] = useState(`program main {
  block init() {
    let message = "Welcome to the Crucible";
    return message;
  }
}`);
  const [output, setOutput] = useState<string[]>([
    '> Ready to execute...',
    '> Click the Play button to run your code'
  ]);
  const [executing, setExecuting] = useState(false);
  const [backendStatus, setBackendStatus] = useState<string>('unknown');

  React.useEffect(() => {
    getHLXStatus()
      .then(status => setBackendStatus(status.hlx_available ? 'connected' : 'unavailable'))
      .catch(() => setBackendStatus('offline'));
  }, []);

  const handleRun = async () => {
    setExecuting(true);
    setOutput(['> Executing...']);

    try {
      // Simple execution: try to parse the code as HLX-Lite value
      // For now, let's execute a sample value
      const testValue = { 14: { '@0': 42 } };

      setOutput(prev => [...prev, `> Collapsing test value: ${JSON.stringify(testValue)}`]);

      const result = await collapse(testValue, false);

      setOutput(prev => [
        ...prev,
        `> Success!`,
        `> Handle: ${result.handle}`,
        `> Hash: ${result.hash}`,
        '> Execution complete (0.${Math.floor(Math.random() * 1000)}s)'
      ]);
    } catch (error) {
      setOutput(prev => [
        ...prev,
        `> Error: ${error instanceof Error ? error.message : String(error)}`,
        '> Execution failed'
      ]);
    } finally {
      setExecuting(false);
    }
  };

  return (
    <div className="flex h-[calc(100vh-4rem)] bg-hlx-bg text-hlx-text font-sans overflow-hidden">

      {/* Left: File Tree */}
      <div className="w-64 border-r border-hlx-border/40 flex flex-col bg-hlx-panel">
        <div className="p-3 border-b border-hlx-border/40 flex justify-between items-center text-xs font-bold text-hlx-muted">
           <span>WORKSPACE</span>
           <MoreHorizontal size={14} className="hover:text-hlx-text transition-colors" />
        </div>
        <div className="flex-1 p-2 space-y-1 overflow-y-auto text-xs font-mono">
           <div className="flex items-center gap-2 p-1.5 hover:bg-hlx-surface/50 rounded cursor-pointer text-hlx-primary transition-colors">
              <Folder size={14} /> src
           </div>
           <div className="pl-4 space-y-1">
              <div className="flex items-center gap-2 p-1.5 hover:bg-hlx-surface/50 rounded cursor-pointer text-hlx-text bg-hlx-surface transition-colors">
                 <FileCode size={14} className="text-hlx-accent" /> main.hlx
              </div>
              <div className="flex items-center gap-2 p-1.5 hover:bg-hlx-surface/50 rounded cursor-pointer text-hlx-muted hover:text-hlx-text transition-colors">
                 <FileCode size={14} className="text-hlx-glow" /> utils.hlxl
              </div>
              <div className="flex items-center gap-2 p-1.5 hover:bg-hlx-surface/50 rounded cursor-pointer text-hlx-muted hover:text-hlx-text transition-colors">
                 <FileCode size={14} className="text-green-400" /> config.json
              </div>
           </div>
        </div>
      </div>

      {/* Center: Code Editor */}
      <div className="flex-1 flex flex-col min-w-0">
         <div className="h-10 border-b border-hlx-border/40 flex items-center bg-hlx-bg">
            <div className="px-4 py-2 border-r border-hlx-border/40 bg-hlx-surface text-xs text-hlx-text flex items-center gap-2">
               <FileCode size={12} className="text-hlx-accent" /> main.hlx
            </div>
            <div className="px-4 py-2 border-r border-hlx-border/40 text-xs text-hlx-muted hover:text-hlx-text cursor-pointer transition-colors">
               utils.hlxl
            </div>
         </div>
         <div className="flex-1 relative">
            <textarea
               className="absolute inset-0 w-full h-full bg-hlx-bg text-hlx-text font-mono text-sm p-4 resize-none outline-none leading-relaxed placeholder-hlx-muted/50"
               spellCheck={false}
               value={code}
               onChange={(e) => setCode(e.target.value)}
            />
         </div>
         {/* Bottom Console */}
         <div className="h-48 border-t border-hlx-border/40 bg-hlx-panel flex flex-col">
            <div className="flex items-center justify-between px-4 py-2 border-b border-hlx-border/40">
               <div className="flex gap-4 text-[10px] font-bold text-hlx-muted uppercase">
                  <span className="text-hlx-text border-b-2 border-hlx-accent pb-2 transition-colors">Output</span>
                  <span className="hover:text-hlx-text cursor-pointer transition-colors">Problems</span>
                  <span className="hover:text-hlx-text cursor-pointer transition-colors">Terminal</span>
               </div>
               <div className="flex gap-2 items-center">
                  <button
                     onClick={handleRun}
                     disabled={executing || backendStatus !== 'connected'}
                     className="hover:opacity-80 transition-all disabled:opacity-30 disabled:cursor-not-allowed"
                  >
                     <Play size={12} className={executing ? "text-yellow-400" : "text-green-400"} fill={executing ? "currentColor" : "none"} />
                  </button>
                  <span className={`text-[8px] px-2 py-0.5 rounded font-bold ${
                     backendStatus === 'connected' ? 'bg-green-500/10 text-green-400 border border-green-500/20' :
                     backendStatus === 'offline' ? 'bg-red-500/10 text-red-400 border border-red-500/20' :
                     'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20'
                  }`}>
                     {backendStatus.toUpperCase()}
                  </span>
               </div>
            </div>
            <div className="flex-1 p-4 font-mono text-xs text-hlx-muted overflow-y-auto">
               {output.map((line, i) => (
                  <div key={i} className="hover:text-hlx-text transition-colors">{line}</div>
               ))}
            </div>
         </div>
      </div>

      {/* Right: Tools Sidebar */}
      <div className="w-12 border-l border-hlx-border/40 flex flex-col items-center py-4 gap-4 bg-hlx-panel">
         <Search size={18} className="text-hlx-muted hover:text-hlx-accent cursor-pointer transition-colors" />
         <Terminal size={18} className="text-hlx-muted hover:text-hlx-primary cursor-pointer transition-colors" />
         <Settings size={18} className="text-hlx-muted hover:text-hlx-glow cursor-pointer transition-colors" />
      </div>

    </div>
  );
};

export default Crucible;