
import React from 'react';
import { Layers, Activity, Box, Database, Network, Server, Zap, Package, Download, Cpu, Code, ArrowDown, Type, Terminal, Hash } from 'lucide-react';
import { HLX_BOOTSTRAP_CODEX } from '../codex_data';

const ArchitectureMap: React.FC = () => {
  const version = HLX_BOOTSTRAP_CODEX.meta.version;

  const handleExportCodex = () => {
    const jsonString = JSON.stringify(HLX_BOOTSTRAP_CODEX, null, 2);
    const encoder = new TextEncoder();
    const utf8Bytes = encoder.encode(jsonString);
    const blob = new Blob([utf8Bytes], { type: 'application/json;charset=utf-8' });
    
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'hlx_codex_v0.1.0.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-8 animate-fade-in pb-12">
      <header className="flex items-start justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-3">
            <Network className="text-hlx-accent" />
            Unified Codex Architecture
          </h2>
          <p className="text-hlx-muted text-sm mt-1">
            Visualizing the Dual-Track Protocol Stack (Lite + Runic).
          </p>
        </div>
        <div className="flex gap-2 items-center">
           <button 
             onClick={handleExportCodex}
             className="flex items-center gap-2 px-3 py-1.5 bg-hlx-accent/10 border border-hlx-accent/30 rounded text-xs font-bold text-hlx-accent hover:bg-hlx-accent hover:text-black transition-all mr-2 group"
           >
             <Package size={14} className="group-hover:scale-110 transition-transform" />
             Export HLX Codex v{version}
             <Download size={12} className="opacity-50" />
           </button>

           <div className="px-3 py-1 rounded border border-hlx-border bg-hlx-surface text-xs font-mono text-hlx-muted">
             v{version}
           </div>
        </div>
      </header>

      {/* DUAL TRACK VISUALIZATION */}
      <div className="relative">
        
        {/* Track Headers */}
        <div className="grid grid-cols-2 gap-8 mb-4">
            <div className="bg-[#0C0713] border border-blue-500/30 rounded-t-xl p-4 border-b-0 relative">
               <div className="absolute top-0 left-0 w-full h-1 bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.5)]"></div>
               <h3 className="text-blue-400 font-bold flex items-center gap-2">
                  <Code size={18} /> TRACK A: HELIX LITE
               </h3>
               <p className="text-xs text-hlx-muted mt-1">Engineering Standard (ASCII)</p>
            </div>
            <div className="bg-[#0C0713] border border-[#A44DFB]/30 rounded-t-xl p-4 border-b-0 relative">
               <div className="absolute top-0 left-0 w-full h-1 bg-[#A44DFB] shadow-[0_0_10px_rgba(164,77,251,0.5)]"></div>
               <h3 className="text-[#A44DFB] font-bold flex items-center gap-2">
                  <SparklesIcon /> TRACK B: HELIX RUNIC
               </h3>
               <p className="text-xs text-hlx-muted mt-1">Model Standard (Glyphs)</p>
            </div>
        </div>

        {/* Parallel Lanes */}
        <div className="grid grid-cols-2 gap-8 relative z-10">
            {/* Lane A: Lite */}
            <div className="space-y-4">
                <LayerCard 
                   title="HLXL Surface" 
                   desc="Human-Readable ASCII Syntax" 
                   version="v2.5" 
                   icon={<Terminal size={16} />}
                   color="border-blue-500/30 bg-blue-500/5 text-blue-400"
                />
                <div className="flex justify-center"><ArrowDown size={16} className="text-blue-500/50" /></div>
                <LayerCard 
                   title="HLXL-LS Latent" 
                   desc="ASCII Handle Space (&h_tag)" 
                   version="v2.0" 
                   icon={<Hash size={16} />}
                   color="border-blue-500/30 bg-blue-500/5 text-blue-400"
                />
                <div className="flex justify-center"><ArrowDown size={16} className="text-blue-500/50" /></div>
            </div>

            {/* Lane B: Runic */}
            <div className="space-y-4">
                <LayerCard 
                   title="HLX Surface" 
                   desc="LLM-Optimized Glyph Syntax" 
                   version="v2.0" 
                   icon={<Type size={16} />}
                   color="border-[#A44DFB]/30 bg-[#A44DFB]/5 text-[#A44DFB]"
                />
                <div className="flex justify-center"><ArrowDown size={16} className="text-[#A44DFB]/50" /></div>
                <LayerCard 
                   title="HLX-LS Latent" 
                   desc="Glyph Handle Space (⟁tag)" 
                   version="v2.0" 
                   icon={<Layers size={16} />}
                   color="border-[#A44DFB]/30 bg-[#A44DFB]/5 text-[#A44DFB]"
                />
                <div className="flex justify-center"><ArrowDown size={16} className="text-[#A44DFB]/50" /></div>
            </div>
        </div>

        {/* Convergence Zone */}
        <div className="relative mt-4">
            {/* Connecting Lines (Visual Hack) */}
            <div className="absolute -top-4 left-1/4 w-0.5 h-4 bg-blue-500/30"></div>
            <div className="absolute -top-4 right-1/4 w-0.5 h-4 bg-[#A44DFB]/30"></div>
            
            <div className="absolute -top-0 left-1/4 w-1/2 h-0.5 bg-gradient-to-r from-blue-500/30 to-[#A44DFB]/30"></div>
            <div className="absolute top-0 left-1/2 w-0.5 h-4 bg-gradient-to-b from-white/30 to-[#39F5E5]/50"></div>

            <div className="pt-4 space-y-4">
                <div className="w-full max-w-2xl mx-auto">
                    <LayerCard 
                       title="LC (Latent Collapse)" 
                       desc="Universal Wire Format (Binary Stream)" 
                       version="v1.0 (FROZEN)" 
                       icon={<Database size={16} />}
                       color="border-[#39F5E5]/30 bg-[#39F5E5]/5 text-[#39F5E5] shadow-[0_0_20px_rgba(57,245,229,0.1)]"
                       center
                    />
                </div>
                
                <div className="flex justify-center"><ArrowDown size={16} className="text-[#39F5E5]/50" /></div>

                <div className="w-full max-w-2xl mx-auto">
                    <LayerCard 
                       title="HLX CORE KERNEL" 
                       desc="Deterministic Execution Engine (AST)" 
                       version="v2.0" 
                       icon={<Cpu size={16} />}
                       color="border-white/20 bg-white/5 text-white"
                       center
                    />
                </div>
            </div>
        </div>

      </div>
    </div>
  );
};

const LayerCard: React.FC<{title: string, desc: string, version: string, icon: React.ReactNode, color: string, center?: boolean}> = ({title, desc, version, icon, color, center}) => (
    <div className={`p-4 rounded-xl border flex items-center justify-between transition-all hover:scale-[1.01] ${color} ${center ? 'text-center' : ''}`}>
        <div className={`flex items-center gap-4 ${center ? 'mx-auto' : ''}`}>
            <div className="p-2 rounded-lg bg-black/20 backdrop-blur-sm">
                {icon}
            </div>
            <div className={center ? 'text-left' : ''}>
                <h3 className="font-bold text-lg">{title}</h3>
                <p className="text-xs opacity-70 font-mono uppercase tracking-wide">{desc}</p>
            </div>
        </div>
        <div className="text-right pl-4 border-l border-white/10 ml-4">
            <span className="text-[10px] font-bold opacity-50 block">VERSION</span>
            <span className="font-mono text-xs">{version}</span>
        </div>
    </div>
);

const SparklesIcon = () => (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z" />
    </svg>
);

export default ArchitectureMap;
