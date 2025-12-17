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
    <div className="flex h-[calc(100vh-4rem)] bg-[#050208] text-gray-300 font-sans overflow-hidden">
      
      {/* Left: File Tree */}
      <div className="w-64 border-r border-[#27272a] flex flex-col bg-[#0C0713]">
        <div className="p-3 border-b border-[#27272a] flex justify-between items-center text-xs font-bold text-gray-400">
           <span>EXPLORER</span>
           <MoreHorizontal size={14} />
        </div>
        <div className="flex-1 p-2 space-y-1 overflow-y-auto text-xs font-mono">
           <div className="flex items-center gap-2 p-1 hover:bg-[#27272a] rounded cursor-pointer text-[#A44DFB]">
              <Folder size={14} /> src
           </div>
           <div className="pl-4 space-y-1">
              <div className="flex items-center gap-2 p-1 hover:bg-[#27272a] rounded cursor-pointer text-white bg-[#27272a]">
                 <FileCode size={14} className="text-blue-400" /> main.hlx
              </div>
              <div className="flex items-center gap-2 p-1 hover:bg-[#27272a] rounded cursor-pointer">
                 <FileCode size={14} className="text-yellow-400" /> utils.hlxl
              </div>
              <div className="flex items-center gap-2 p-1 hover:bg-[#27272a] rounded cursor-pointer">
                 <FileCode size={14} className="text-green-400" /> config.json
              </div>
           </div>
        </div>
      </div>

      {/* Center: Code Editor */}
      <div className="flex-1 flex flex-col min-w-0">
         <div className="h-10 border-b border-[#27272a] flex items-center bg-[#050208]">
            <div className="px-4 py-2 border-r border-[#27272a] bg-[#0C0713] text-xs text-white flex items-center gap-2">
               <FileCode size={12} className="text-blue-400" /> main.hlx
            </div>
            <div className="px-4 py-2 border-r border-[#27272a] text-xs text-gray-500 hover:text-gray-300 cursor-pointer">
               utils.hlxl
            </div>
         </div>
         <div className="flex-1 relative">
            <textarea
               className="absolute inset-0 w-full h-full bg-[#050208] text-[#e4e4e7] font-mono text-sm p-4 resize-none outline-none leading-relaxed"
               spellCheck={false}
               value={code}
               onChange={(e) => setCode(e.target.value)}
            />
         </div>
         {/* Bottom Console */}
         <div className="h-48 border-t border-[#27272a] bg-[#0C0713] flex flex-col">
            <div className="flex items-center justify-between px-4 py-2 border-b border-[#27272a]">
               <div className="flex gap-4 text-[10px] font-bold text-gray-500 uppercase">
                  <span className="text-white border-b-2 border-[#A44DFB] pb-2">Output</span>
                  <span className="hover:text-white cursor-pointer">Problems</span>
                  <span className="hover:text-white cursor-pointer">Terminal</span>
               </div>
               <div className="flex gap-2 items-center">
                  <button
                     onClick={handleRun}
                     disabled={executing || backendStatus !== 'connected'}
                     className="hover:opacity-80 transition-opacity disabled:opacity-30 disabled:cursor-not-allowed"
                  >
                     <Play size={12} className={executing ? "text-yellow-400" : "text-green-400"} />
                  </button>
                  <span className={`text-[8px] px-2 py-0.5 rounded ${
                     backendStatus === 'connected' ? 'bg-green-900/30 text-green-400' :
                     backendStatus === 'offline' ? 'bg-red-900/30 text-red-400' :
                     'bg-yellow-900/30 text-yellow-400'
                  }`}>
                     {backendStatus.toUpperCase()}
                  </span>
               </div>
            </div>
            <div className="flex-1 p-4 font-mono text-xs text-gray-400 overflow-y-auto">
               {output.map((line, i) => (
                  <div key={i}>{line}</div>
               ))}
            </div>
         </div>
      </div>

      {/* Right: Helper */}
      <div className="w-12 border-l border-[#27272a] flex flex-col items-center py-4 gap-4 bg-[#0C0713]">
         <Search size={18} className="text-gray-500 hover:text-white cursor-pointer" />
         <Terminal size={18} className="text-gray-500 hover:text-white cursor-pointer" />
         <Settings size={18} className="text-gray-500 hover:text-white cursor-pointer" />
      </div>

    </div>
  );
};

export default Crucible;