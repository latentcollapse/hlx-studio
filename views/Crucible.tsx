import React from 'react';
import { Folder, FileCode, Play, Terminal, MoreHorizontal, Search, Settings } from 'lucide-react';

const Crucible: React.FC = () => {
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
               defaultValue={`program main {
  block init() {
    let message = "Welcome to the Crucible";
    return message;
  }
}`}
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
               <div className="flex gap-2">
                  <Play size={12} className="text-green-400 cursor-pointer" />
               </div>
            </div>
            <div className="flex-1 p-4 font-mono text-xs text-gray-400 overflow-y-auto">
               {'>'} Build started...<br/>
               {'>'} Compiling main.hlx...<br/>
               {'>'} Success (0.4s)
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