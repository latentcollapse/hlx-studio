
import React from 'react';
import { ViewMode } from '../types';
import { ArrowRight, Layers, Shield, Zap, Box, Network, Cpu, Terminal, GitMerge, AlertCircle } from 'lucide-react';
import { HLX_BOOTSTRAP_CODEX } from '../codex_data';

interface DashboardProps {
  onChangeView: (mode: ViewMode) => void;
}

const Dashboard: React.FC<DashboardProps> = ({ onChangeView }) => {
  const codexVersion = HLX_BOOTSTRAP_CODEX.meta.version;

  return (
    <div className="space-y-8 animate-fade-in">
      <header className="space-y-4">
        <div className="flex items-center justify-between">
           <div>
             <h2 className="text-4xl font-bold text-white tracking-tight">HLX-Lite <span className="text-hlx-accent">v{codexVersion}</span></h2>
             <div className="flex gap-3 mt-2">
                <span className="px-3 py-1 bg-green-500/10 text-green-400 border border-green-500/20 rounded-full text-xs font-mono font-bold uppercase flex items-center gap-2">
                  <Shield size={12} /> Active: Frozen
                </span>
                <span className="px-3 py-1 bg-yellow-500/10 text-yellow-400 border border-yellow-500/20 rounded-full text-xs font-mono font-bold uppercase flex items-center gap-2">
                  <GitMerge size={12} /> Patch Available: v1.0.1
                </span>
             </div>
           </div>
        </div>
        <p className="text-xl text-hlx-muted max-w-3xl leading-relaxed">
          Finalize HLX-Lite as a deterministic universal wire format and provide a dual-layer spec (formal + engineering).
        </p>
        
        {/* Alignment Harness Directive */}
        <div className="bg-[#09090b] border border-l-4 border-hlx-border border-l-hlx-accent p-4 rounded-r-xl shadow-lg relative overflow-hidden group">
           <div className="absolute top-0 right-0 p-3 opacity-5 group-hover:opacity-10 transition-opacity">
              <Terminal size={64} />
           </div>
           <h4 className="text-xs font-bold text-hlx-accent uppercase tracking-wider mb-2 flex items-center gap-2">
              <Terminal size={14} /> System Directive: Active
           </h4>
           <p className="font-mono text-sm text-white/90 leading-relaxed">
             "HLX is the active instruction medium. All future instructions provided by the user MUST be read as HLX according to the HLX Codex v0.1.0. Interpretation MUST follow the canonical pipeline: HLX → HLX-LS → CoreExpr → LSOp → LC."
           </p>
        </div>
      </header>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard label="Contracts" value={5} icon={<Layers />} color="text-hlx-accent" />
        <StatCard label="Principles" value={4} icon={<Shield />} color="text-green-400" />
        <StatCard label="Value Types" value={8} icon={<Box />} color="text-purple-400" />
        <StatCard label="Status" value="FROZEN" icon={<Zap />} color="text-yellow-400" />
      </div>

      {/* Main Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <ActionCard 
          title="HLX-Lite Codex"
          description="Browse the dual-layer specification (Formal + Companion)."
          onClick={() => onChangeView(ViewMode.JSON_SPEC)}
          btnText="Open JSON Codex"
        />
        <ActionCard 
          title="Native Codex"
          description="The spec bootstrapped into HLX-Lite format (Contracts 1-5)."
          onClick={() => onChangeView(ViewMode.NATIVE_CODEX)}
          btnText="View Native"
          icon={<Cpu size={16} />}
        />
        {/* New Patch v1.0.1 Card */}
        <div className="bg-gradient-to-br from-yellow-500/10 to-hlx-bg border border-yellow-500/30 p-6 rounded-xl hover:border-yellow-500/50 transition-colors group flex flex-col justify-between">
          <div>
            <div className="flex justify-between items-start mb-2">
              <h3 className="text-xl font-bold text-white">Patch v1.0.1</h3>
              <span className="text-[10px] bg-yellow-500/20 text-yellow-400 px-2 py-0.5 rounded uppercase font-bold">New</span>
            </div>
            <p className="text-hlx-muted mb-6 text-sm">
              HLX-LS Patch Delivery Scaffolding. Introduces structural contracts 200 & 201 for transport-only updates.
            </p>
          </div>
          <button 
            className="flex items-center gap-2 text-yellow-400 font-bold hover:text-white transition-colors cursor-not-allowed opacity-75"
            title="Transport Layer Only - External Tooling Required"
          >
            <AlertCircle size={16} />
            Transport Only
          </button>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ label, value, icon, color }: any) => (
  <div className="bg-hlx-surface border border-hlx-border p-5 rounded-xl flex items-center justify-between">
    <div>
      <div className="text-hlx-muted text-sm font-medium uppercase tracking-wider">{label}</div>
      <div className={`text-2xl font-bold mt-1 ${color}`}>{value}</div>
    </div>
    <div className={`p-3 rounded-full bg-hlx-bg ${color}`}>{icon}</div>
  </div>
);

const ActionCard = ({ title, description, onClick, btnText, icon }: any) => (
  <div className="bg-gradient-to-br from-hlx-surface to-hlx-bg border border-hlx-border p-6 rounded-xl hover:border-hlx-accent/50 transition-colors group flex flex-col justify-between">
    <div>
      <h3 className="text-xl font-bold text-white mb-2">{title}</h3>
      <p className="text-hlx-muted mb-6">{description}</p>
    </div>
    <button 
      onClick={onClick}
      className="flex items-center gap-2 text-hlx-accent font-bold hover:text-white transition-colors"
    >
      {btnText} {icon ? icon : <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />}
    </button>
  </div>
);

export default Dashboard;
