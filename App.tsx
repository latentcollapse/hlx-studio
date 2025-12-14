
import React, { useState } from 'react';
import { Terminal, Command, Code, TerminalSquare, Archive as ArchiveIcon, Cpu, Download, Lock, Package, Triangle } from 'lucide-react';
import { ViewMode } from './types';
import HelixCLI from './views/HelixCLI';
import HLXEngine from './views/HLXEngine';
import Crucible from './views/Crucible';
import TTY1 from './views/TTY1';
import Archive from './views/Archive';
import JSONSpecViewer from './views/JSONSpecViewer';
import NativeCodex from './views/NativeCodex';
import HLXVisualizer from './views/HLXVisualizer';
import { BRAND } from './config/branding';
import { generateBootstrapCapsule } from './utils/bootstrapFactory';

function App() {
  const [currentView, setCurrentView] = useState<ViewMode>(ViewMode.HELIX);
  const [isGenerating, setIsGenerating] = useState(false);

  const renderView = () => {
    switch (currentView) {
      case ViewMode.HELIX: return <HelixCLI />;
      case ViewMode.HLX_ENGINE: return <HLXEngine />;
      case ViewMode.CRUCIBLE: return <Crucible />;
      case ViewMode.TTY1: return <TTY1 />;
      case ViewMode.ARCHIVE: return <Archive />;
      case ViewMode.JSON_SPEC: return <JSONSpecViewer />;
      case ViewMode.NATIVE_CODEX: return <NativeCodex />;
      case ViewMode.HLX_NATIVE: return <HLXVisualizer />;
      default: return <HelixCLI />;
    }
  };

  const handleDownloadCapsule = async () => {
    if (isGenerating) return;
    setIsGenerating(true);
    try {
      const blob = await generateBootstrapCapsule();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'hlx_bootstrap_capsule_v1.2.zip';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error("Capsule generation failed:", e);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#020617] text-hlx-text font-sans selection:bg-hlx-primary/30 selection:text-white flex flex-col bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-[#020617] to-[#020617]">
      {/* Top Navigation Bar */}
      <nav className="h-14 border-b border-hlx-border/50 bg-[#020617]/80 backdrop-blur-md flex items-center px-6 justify-between flex-shrink-0 z-50 sticky top-0">
        <div className="flex items-center gap-6">
           <div className="flex items-center gap-3">
              <div className="p-1.5 bg-hlx-primary/10 rounded-lg border border-hlx-primary/20">
                <Cpu className="text-hlx-primary w-5 h-5" />
              </div>
              <span className="font-bold text-white tracking-tight text-lg">
                Helix<span className="text-hlx-primary">Studio</span>
              </span>
           </div>
           
           <div className="h-6 w-px bg-hlx-border/50"></div>
           
           {/* Navigation Tabs */}
           <div className="flex items-center gap-1">
              <NavTab 
                 active={currentView === ViewMode.HELIX} 
                 onClick={() => setCurrentView(ViewMode.HELIX)}
                 icon={<Terminal size={15} />}
                 label="HELIX"
              />
              <NavTab
                 active={currentView === ViewMode.HLX_ENGINE}
                 onClick={() => setCurrentView(ViewMode.HLX_ENGINE)}
                 icon={<Triangle size={15} />}
                 label="PRISM"
              />
              <NavTab 
                 active={currentView === ViewMode.CRUCIBLE} 
                 onClick={() => setCurrentView(ViewMode.CRUCIBLE)}
                 icon={<Code size={15} />}
                 label="CRUCIBLE"
              />
              <NavTab 
                 active={currentView === ViewMode.TTY1} 
                 onClick={() => setCurrentView(ViewMode.TTY1)}
                 icon={<TerminalSquare size={15} />}
                 label="TTY1"
              />
              <NavTab 
                 active={currentView === ViewMode.ARCHIVE} 
                 onClick={() => setCurrentView(ViewMode.ARCHIVE)}
                 icon={<ArchiveIcon size={15} />}
                 label="ARCHIVE"
              />
           </div>
        </div>

        <div className="flex items-center gap-4">
           {currentView === ViewMode.HLX_ENGINE && (
             <div className="flex gap-2">
               <button 
                 onClick={handleDownloadCapsule}
                 disabled={isGenerating}
                 className={`flex items-center gap-2 px-3 py-1.5 rounded-md bg-hlx-accent/10 border border-hlx-accent/20 text-hlx-accent text-xs font-semibold tracking-wide transition-all hover:bg-hlx-accent/20 ${isGenerating ? 'opacity-50 cursor-not-allowed' : ''}`}
               >
                 <Package size={14} className={isGenerating ? 'animate-spin' : ''} />
                 {isGenerating ? 'Generating...' : 'Bootstrap Capsule'}
               </button>
             </div>
           )}
           <div className="flex items-center gap-2 px-2 py-1 rounded bg-green-500/5 border border-green-500/10">
              <div className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse-slow"></div>
              <span className="text-[10px] font-bold text-green-400/80 uppercase tracking-wider">System Active</span>
           </div>
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="flex-1 overflow-hidden relative">
        {renderView()}
      </main>
    </div>
  );
}

const NavTab: React.FC<{ active: boolean, onClick: () => void, icon: React.ReactNode, label: string }> = ({ active, onClick, icon, label }) => (
  <button
    onClick={onClick}
    className={`
      flex items-center gap-2 px-3 py-1.5 rounded-md text-xs font-bold tracking-wide transition-all duration-200
      ${active 
        ? 'bg-white/5 text-white border border-white/10 shadow-sm' 
        : 'text-hlx-muted hover:text-white hover:bg-white/5 border border-transparent'}
    `}
  >
    {icon}
    {label}
  </button>
);

export default App;
