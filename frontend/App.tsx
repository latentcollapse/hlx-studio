
import React, { useState } from 'react';
import { Terminal, Code, TerminalSquare, Archive as ArchiveIcon, Cpu, Brain } from 'lucide-react';
import { ViewMode } from './types';
import HelixCLI from './views/HelixCLI';
import Crucible from './views/Crucible';
import TTY1 from './views/TTY1';
import TrainingCenter from './views/TrainingCenter';
import Archive from './views/Archive';
import { BRAND } from './config/branding';

function App() {
  const [currentView, setCurrentView] = useState<ViewMode>(ViewMode.HELIX);

  const renderView = () => {
    switch (currentView) {
      case ViewMode.HELIX: return <HelixCLI />;
      case ViewMode.CRUCIBLE: return <Crucible />;
      case ViewMode.TTY1: return <TTY1 />;
      case ViewMode.TRAINING_CENTER: return <TrainingCenter />;
      case ViewMode.ARCHIVE: return <Archive />;
      default: return <HelixCLI />;
    }
  };


  return (
    <div className="min-h-screen bg-hlx-bg text-hlx-text font-sans selection:bg-hlx-accent/20 selection:text-white flex flex-col bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-violet-950/20 via-hlx-bg to-hlx-bg">
      {/* Top Navigation Bar */}
      <nav className="h-14 border-b border-hlx-border/40 bg-hlx-panel/90 backdrop-blur-xl flex items-center px-6 justify-between flex-shrink-0 z-50 sticky top-0">
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
                 active={currentView === ViewMode.TRAINING_CENTER}
                 onClick={() => setCurrentView(ViewMode.TRAINING_CENTER)}
                 icon={<Brain size={15} />}
                 label="TRAINING"
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
      flex items-center gap-2 px-3 py-1.5 rounded-md text-xs font-semibold tracking-wide transition-all duration-200
      ${active
        ? 'bg-hlx-accent/10 text-hlx-glow border border-hlx-accent/30 shadow-lg shadow-hlx-accent/10'
        : 'text-hlx-muted hover:text-hlx-text hover:bg-hlx-surface/50 border border-transparent hover:border-hlx-border/30'}
    `}
  >
    {icon}
    {label}
  </button>
);

export default App;
