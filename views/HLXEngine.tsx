
import React, { useState, useEffect } from 'react';
import { Terminal, Play, Layers, Monitor, Network, Activity, Sparkles, Code, HardDrive, Download, Zap } from 'lucide-react';
import { HLXEngineService, ExecutionResult } from '../services/hlxEngine';
import LcStreamView from '../components/hlx/LcStreamView';
import InvariantDashboard from '../components/hlx/InvariantDashboard';
import HlxCrossInspector from '../components/hlx/CrossInspector';

// --- SUB-COMPONENTS ---

// 1. Sessions Sidebar (Left)
const HlxSessionsSidebar: React.FC<{ onRunTask: (id: string) => void }> = ({ onRunTask }) => {
  const tasks = [
    { id: 'sys-lc12-bootstrap', label: 'GEN: LC_12 Bootstrap', icon: <Download size={14} className="text-green-400" /> },
    { id: 'sys-executor', label: 'SYS: Enable Executor', icon: <Terminal size={14} /> },
    { id: 'sys-sd8-hotfix', label: 'HOTFIX: SD8 (Canonical)', icon: <Sparkles size={14} /> },
    { id: 'sys-sd9-synthesis', label: 'SYNTHESIS: SD9 (Grok)', icon: <Sparkles size={14} /> },
    { id: 'lc_test_basic_v2', label: 'TEST: LC Basic v2', icon: <Network size={14} /> },
    { id: 'lc_test_positional_v2', label: 'TEST: LC Positional v2', icon: <Network size={14} /> },
    { id: 'delta_promote_hlxls', label: 'DELTA: Promote HLX-LS', icon: <Activity size={14} /> },
    { id: 'delta_tune_lc', label: 'DELTA: Tune LC', icon: <Activity size={14} /> },
  ];

  return (
    <div className="flex flex-col h-full bg-hlx-bg border-r border-hlx-border w-64 glass-panel">
      <div className="p-4 border-b border-hlx-border flex items-center gap-2">
        <Zap className="text-hlx-primary" size={18} />
        <span className="font-bold text-white tracking-widest text-xs">RUNTIME SESSIONS</span>
      </div>
      <div className="flex-1 p-2 space-y-1 overflow-y-auto">
        <div className="px-2 py-1 text-[10px] font-bold text-hlx-accent opacity-50 mb-1 tracking-wider">TASKS</div>
        {tasks.map(task => (
          <button
            key={task.id}
            onClick={() => onRunTask(task.id)}
            className="w-full flex items-center gap-3 px-3 py-2 rounded-md hover:bg-hlx-accent/10 hover:text-hlx-accent text-hlx-muted transition-all text-xs font-mono text-left group border border-transparent hover:border-hlx-accent/20"
          >
            <span className="group-hover:scale-110 transition-transform">{task.icon}</span>
            {task.label}
          </button>
        ))}
      </div>
      <div className="p-4 border-t border-hlx-border text-[10px] text-hlx-muted font-mono">
        SESSION: ACTIVE<br/>
        ID: 0x8F2A...
      </div>
    </div>
  );
};

// 2. Editor Panel (Center)
interface HlxEditorPanelProps {
  program: string;
  onChange: (val: string) => void;
  onRun: () => void;
  isExecuting: boolean;
  mode: 'HLXL' | 'HLX';
  setMode: (m: 'HLXL' | 'HLX') => void;
}

const HlxEditorPanel: React.FC<HlxEditorPanelProps> = ({ program, onChange, onRun, isExecuting, mode, setMode }) => {
  const insertGlyph = (g: string) => onChange(program + g);

  return (
    <div className="flex flex-col h-full bg-hlx-bg relative min-w-0 flex-1 border-r border-hlx-border">
      {/* Background Grid FX */}
      <div className="absolute inset-0 pointer-events-none opacity-5 bg-[linear-gradient(rgba(129,140,248,0.1)_1px,transparent_1px),linear-gradient(90deg,rgba(129,140,248,0.1)_1px,transparent_1px)] bg-[size:40px_40px]"></div>

      {/* Toolbar */}
      <div className="flex items-center border-b border-hlx-border bg-hlx-panel/50 backdrop-blur-sm px-4 py-2 justify-between shrink-0 z-10">
         <div className="flex items-center gap-2">
            <Code size={14} className="text-hlx-muted" />
            <span className="text-xs font-bold text-white tracking-wider">SOURCE EDITOR</span>
         </div>
         <div className="flex items-center gap-1 bg-hlx-surface rounded-lg p-0.5 border border-hlx-border">
             <button
                className={`text-[10px] px-3 py-1 rounded-md transition-all font-bold ${mode === 'HLXL' ? 'bg-hlx-primary text-white shadow-sm' : 'text-hlx-muted hover:text-white'}`}
                onClick={() => setMode('HLXL')}
             >HLXL</button>
             <button
                className={`text-[10px] px-3 py-1 rounded-md transition-all font-bold ${mode === 'HLX' ? 'bg-hlx-primary text-white shadow-sm' : 'text-hlx-muted hover:text-white'}`}
                onClick={() => setMode('HLX')}
             >HLX</button>
         </div>
      </div>

      {/* Glyph Bar */}
      <div className="p-2 border-b border-hlx-border bg-hlx-surface/30 flex gap-1 overflow-x-auto shrink-0 z-10 scrollbar-hide">
        {['⟠','◇','⊢','⊡','↩','❓','❗','⟳','⟲','⚳','⚯','⚶','⚿','⌸⑂','⌸⊕'].map(g => (
          <button 
            key={g} 
            onClick={() => insertGlyph(g)}
            className="w-8 h-8 flex items-center justify-center rounded hover:bg-white/10 text-hlx-text font-mono text-sm border border-transparent hover:border-hlx-border transition-colors shrink-0"
          >
            {g}
          </button>
        ))}
      </div>

      {/* Text Area */}
      <textarea
        value={program}
        onChange={(e) => onChange(e.target.value)}
        className="flex-1 bg-transparent p-6 font-mono text-sm text-hlx-text focus:outline-none resize-none leading-relaxed z-0"
        spellCheck={false}
      />

      {/* Footer */}
      <div className="p-4 border-t border-hlx-border flex justify-end shrink-0 z-10 bg-hlx-bg/50 backdrop-blur-sm">
        <button 
          onClick={onRun}
          disabled={isExecuting}
          className="flex items-center gap-2 px-6 py-2 bg-hlx-primary hover:bg-hlx-primary/90 text-white rounded-lg font-bold text-xs tracking-wider transition-all shadow-lg shadow-hlx-primary/20 disabled:opacity-50 disabled:shadow-none"
        >
          {isExecuting ? <Activity size={14} className="animate-spin" /> : <Play size={14} fill="currentColor" />}
          {isExecuting ? 'EXECUTING...' : 'EXECUTE'}
        </button>
      </div>
    </div>
  );
};

// 3. Output Panel (Right)
interface HlxOutputPanelProps {
  result: ExecutionResult | null;
}

const HlxOutputPanel: React.FC<HlxOutputPanelProps> = ({ result }) => {
  const [activeTab, setActiveTab] = useState<'HLXL' | 'HLXL_LS' | 'HLX' | 'HLX_LS' | 'LC'>('LC');

  return (
    <div className="flex flex-col h-full bg-hlx-panel border-l border-hlx-border w-96 glass-panel">
      <div className="p-4 border-b border-hlx-border flex items-center gap-2 justify-between">
        <div className="flex items-center gap-2">
           <Monitor className="text-hlx-accent" size={18} />
           <span className="font-bold text-white tracking-widest text-xs">OUTPUT STREAM</span>
        </div>
        {result && (
           <span className="text-[10px] text-hlx-primary font-mono border border-hlx-primary/30 px-2 py-0.5 rounded bg-hlx-primary/10">
             {result.provenance.codex_version}
           </span>
        )}
      </div>

      {result ? (
        <div className="flex-1 flex flex-col min-h-0">
           {/* Cross Inspector (Pipeline) */}
           <div className="p-4 border-b border-hlx-border bg-hlx-bg/50">
              <div className="text-[10px] text-hlx-muted uppercase font-bold mb-2">Pipeline Inspector</div>
              <HlxCrossInspector activeStage={activeTab} onStageSelect={setActiveTab} />
           </div>

           {/* Content Area */}
           <div className="flex-1 overflow-y-auto p-4 space-y-4">
              
              {/* Main Output */}
              <div className="rounded-lg bg-hlx-bg border border-hlx-border p-4 min-h-[120px] shadow-inner">
                 <div className="text-[10px] text-hlx-muted uppercase font-bold mb-2 flex justify-between">
                    <span>{activeTab} View</span>
                    <span className="text-hlx-muted font-mono">RO</span>
                 </div>
                 {activeTab === 'LC' ? (
                    <LcStreamView stream={result.lc_stream} />
                 ) : (
                    <pre className="font-mono text-xs text-hlx-text whitespace-pre-wrap break-all">
                      {activeTab === 'HLX' ? result.hlx :
                       activeTab === 'HLXL' ? result.hlxl :
                       activeTab === 'HLX_LS' ? result.hlx_ls :
                       activeTab === 'HLXL_LS' ? result.hlxl_ls :
                       JSON.stringify(result.hlx_lite, null, 2)}
                    </pre>
                 )}
              </div>

              {/* Runtime Memory */}
              {result.runtime_state && (
                <div className="rounded-lg bg-hlx-bg border border-hlx-primary/20 p-3 relative overflow-hidden">
                   <div className="text-[10px] text-hlx-primary uppercase font-bold mb-2 flex items-center gap-2">
                      <HardDrive size={12} /> Runtime Memory (CAS)
                   </div>
                   <div className="space-y-1">
                      {result.runtime_state.table_entries.map((entry, i) => (
                        <div key={i} className="flex justify-between items-center text-[10px] font-mono border-b border-hlx-border/50 pb-1 last:border-0">
                           <span className="text-green-400">{entry.handle}</span>
                           <span className="text-hlx-muted">{entry.type} ({entry.size}b)</span>
                        </div>
                      ))}
                   </div>
                   <div className="mt-2 text-[9px] text-hlx-muted text-right">
                      {result.runtime_state.active_handles} Handles Active
                   </div>
                </div>
              )}

              {/* Logs */}
              {result.output_log && (
                <div className="rounded-lg bg-hlx-bg border border-hlx-border p-3">
                   <div className="text-[10px] text-hlx-muted uppercase font-bold mb-1">Execution Log</div>
                   <pre className="font-mono text-[10px] text-hlx-text whitespace-pre-wrap">
                     {result.output_log}
                   </pre>
                </div>
              )}

              {/* Invariants */}
              <div>
                <div className="text-[10px] font-bold text-hlx-muted uppercase mb-2 flex items-center gap-2">
                  <Layers size={12} /> Invariants
                </div>
                <InvariantDashboard invariants={result.invariants} />
              </div>

              {/* Provenance Footer */}
              <div className="border-t border-hlx-border pt-2 mt-2">
                 <div className="flex justify-between text-[10px] text-hlx-muted font-mono">
                    <span>Engine: {result.provenance.engine_id}</span>
                    <span>{result.provenance.collapse_version}</span>
                 </div>
                 <div className="text-[10px] text-hlx-muted/50 font-mono truncate mt-1">
                    {result.provenance.provenance_fp}
                 </div>
              </div>
           </div>
        </div>
      ) : (
        <div className="flex items-center justify-center flex-1 text-hlx-muted text-xs uppercase tracking-widest">
           System Idle
        </div>
      )}
    </div>
  );
};

// 4. Main Component (Engine Layout)
const HLXEngine: React.FC = () => {
  const [program, setProgram] = useState(`⟠ runtime_test {
  ◇ main() {
    ⊢ data = {14:{@0:"Hello Runtime"}};
    ⊢ h = ⚳ data; // Collapse to Runtime Memory
    ⊢ v = ⚯ h;    // Resolve from Runtime Memory
    ↩ v;
  }
}`);
  const [mode, setMode] = useState<'HLXL' | 'HLX'>('HLX');
  const [result, setResult] = useState<ExecutionResult | null>(null);
  const [isExecuting, setIsExecuting] = useState(false);

  useEffect(() => {
    handleRun();
  }, []);

  const handleRunTask = async (taskId: string) => {
    setIsExecuting(true);
    const { program: newProg, result: newRes } = await HLXEngineService.runSystemTask(taskId);
    setProgram(newProg);
    setResult(newRes);
    setIsExecuting(false);
  };

  const handleRun = async () => {
    setIsExecuting(true);
    const res = await HLXEngineService.execute(mode, program);
    setResult(res);
    setIsExecuting(false);
  };

  return (
    <div className="flex h-[calc(100vh-3.5rem)] bg-hlx-bg text-hlx-text font-sans overflow-hidden">
      <HlxSessionsSidebar onRunTask={handleRunTask} />
      <HlxEditorPanel 
         program={program} 
         onChange={setProgram} 
         onRun={handleRun} 
         isExecuting={isExecuting} 
         mode={mode} 
         setMode={setMode} 
      />
      <HlxOutputPanel result={result} />
    </div>
  );
};

export default HLXEngine;
