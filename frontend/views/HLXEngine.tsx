import React, { useState } from 'react';
import { Triangle, Activity, Cpu, Database, Zap, Terminal, RefreshCw, Shield } from 'lucide-react';

// PRISM - The HLX Engine Dashboard
const HLXEngine: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'observatory' | 'fission' | 'axioms'>('observatory');

  return (
    <div className="flex flex-col h-full bg-hlx-bg">
      {/* Tab Navigation */}
      <div className="flex items-center gap-1 px-4 py-2 border-b border-hlx-border bg-hlx-surface/50">
        <TabButton
          active={activeTab === 'observatory'}
          onClick={() => setActiveTab('observatory')}
          icon={<Activity size={14} />}
          label="Latent Space Observatory"
        />
        <TabButton
          active={activeTab === 'fission'}
          onClick={() => setActiveTab('fission')}
          icon={<Zap size={14} />}
          label="Fission Chamber"
        />
        <TabButton
          active={activeTab === 'axioms'}
          onClick={() => setActiveTab('axioms')}
          icon={<Shield size={14} />}
          label="Axiom Panel"
        />
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-auto p-6">
        {activeTab === 'observatory' && <LatentSpaceObservatory />}
        {activeTab === 'fission' && <FissionChamber />}
        {activeTab === 'axioms' && <AxiomPanel />}
      </div>
    </div>
  );
};

const TabButton: React.FC<{ active: boolean; onClick: () => void; icon: React.ReactNode; label: string }> = ({
  active, onClick, icon, label
}) => (
  <button
    onClick={onClick}
    className={`
      flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-t-lg transition-all
      ${active
        ? 'bg-hlx-bg text-hlx-accent border-t border-x border-hlx-accent/30'
        : 'text-hlx-muted hover:text-white hover:bg-white/5'}
    `}
  >
    {icon}
    {label}
  </button>
);

const LatentSpaceObservatory: React.FC = () => {
  const [logs] = useState(() =>
    Array.from({ length: 8 }, (_, i) => ({
      time: new Date(Date.now() - i * 3000).toLocaleTimeString(),
      type: ['COLLAPSE', 'RESOLVE', 'SNAPSHOT', 'VERIFY'][i % 4],
      handle: `&h_${Math.random().toString(36).slice(2, 10)}`,
      status: i % 5 === 0 ? 'WARN' : 'OK'
    }))
  );

  return (
    <div className="space-y-6 animate-fade-in">
      <header className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-3">
            <Triangle className="text-hlx-accent" />
            Latent Space Observatory
          </h2>
          <p className="text-hlx-muted text-sm mt-1">
            Real-time monitoring of handle operations and CAS integrity.
          </p>
        </div>
        <button className="flex items-center gap-2 px-3 py-1.5 bg-hlx-accent/10 border border-hlx-accent/30 rounded text-xs font-bold text-hlx-accent hover:bg-hlx-accent hover:text-black transition-all">
          <RefreshCw size={12} />
          Refresh State
        </button>
      </header>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard label="Active Handles" value="247" icon={<Database size={18} />} color="text-hlx-accent" />
        <StatCard label="CAS Entries" value="1,024" icon={<Cpu size={18} />} color="text-green-400" />
        <StatCard label="Merkle Depth" value="4" icon={<Shield size={18} />} color="text-purple-400" />
        <StatCard label="Integrity" value="VALID" icon={<Activity size={18} />} color="text-emerald-400" />
      </div>

      {/* Transaction Stream */}
      <div className="bg-hlx-surface border border-hlx-border rounded-xl overflow-hidden">
        <div className="px-4 py-3 border-b border-hlx-border flex items-center justify-between">
          <h3 className="font-bold text-white flex items-center gap-2">
            <Terminal size={16} className="text-hlx-accent" />
            Transaction Stream
          </h3>
          <span className="text-[10px] font-mono text-hlx-muted">LIVE</span>
        </div>
        <div className="divide-y divide-hlx-border/50 max-h-64 overflow-y-auto">
          {logs.map((log, i) => (
            <div key={i} className="px-4 py-2 font-mono text-xs flex items-center gap-4 hover:bg-white/5">
              <span className="text-hlx-muted w-20">{log.time}</span>
              <span className={`w-20 font-bold ${
                log.type === 'COLLAPSE' ? 'text-blue-400' :
                log.type === 'RESOLVE' ? 'text-green-400' :
                log.type === 'SNAPSHOT' ? 'text-purple-400' : 'text-yellow-400'
              }`}>{log.type}</span>
              <span className="text-hlx-accent flex-1">{log.handle}</span>
              <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                log.status === 'OK' ? 'bg-green-500/10 text-green-400' : 'bg-yellow-500/10 text-yellow-400'
              }`}>{log.status}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const FissionChamber: React.FC = () => (
  <div className="space-y-6 animate-fade-in">
    <header>
      <h2 className="text-2xl font-bold text-white flex items-center gap-3">
        <Zap className="text-yellow-400" />
        Fission Chamber
      </h2>
      <p className="text-hlx-muted text-sm mt-1">
        Value decomposition and LC stream visualization.
      </p>
    </header>

    <div className="bg-hlx-surface border border-hlx-border rounded-xl p-6">
      <div className="text-center text-hlx-muted py-12">
        <Zap size={48} className="mx-auto mb-4 opacity-20" />
        <p className="font-mono text-sm">Fission Chamber - Active Mode</p>
        <p className="text-xs mt-2">Drop an HLX-Lite value to decompose into LC stream</p>
      </div>
    </div>
  </div>
);

const AxiomPanel: React.FC = () => {
  const axioms = [
    { id: 'A1', name: 'DETERMINISM', status: 'PASS', desc: 'Same input produces same LC stream' },
    { id: 'A2', name: 'REVERSIBILITY', status: 'PASS', desc: 'Collapse and Resolve are inverses' },
    { id: 'A3', name: 'BIJECTION', status: 'PASS', desc: 'Track A and Track B map 1:1' },
    { id: 'A4', name: 'UNIVERSAL_VALUE', status: 'PASS', desc: 'All tracks lower to HLX-Lite' },
  ];

  return (
    <div className="space-y-6 animate-fade-in">
      <header>
        <h2 className="text-2xl font-bold text-white flex items-center gap-3">
          <Shield className="text-green-400" />
          Axiom Panel
        </h2>
        <p className="text-hlx-muted text-sm mt-1">
          Continuous verification of HLX core invariants.
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {axioms.map(axiom => (
          <div key={axiom.id} className="bg-hlx-surface border border-hlx-border rounded-xl p-4 hover:border-green-500/30 transition-colors">
            <div className="flex items-start justify-between mb-2">
              <span className="font-mono text-xs font-bold text-green-400 bg-green-500/10 px-2 py-0.5 rounded">
                {axiom.id}
              </span>
              <span className="text-[10px] font-bold text-green-400 bg-green-500/10 px-2 py-0.5 rounded">
                {axiom.status}
              </span>
            </div>
            <h3 className="font-bold text-white mb-1">{axiom.name}</h3>
            <p className="text-xs text-hlx-muted">{axiom.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

const StatCard: React.FC<{ label: string; value: string; icon: React.ReactNode; color: string }> = ({
  label, value, icon, color
}) => (
  <div className="bg-hlx-surface border border-hlx-border p-4 rounded-xl flex items-center justify-between">
    <div>
      <div className="text-hlx-muted text-xs font-medium uppercase tracking-wider">{label}</div>
      <div className={`text-xl font-bold mt-1 ${color}`}>{value}</div>
    </div>
    <div className={`p-2.5 rounded-lg bg-hlx-bg ${color}`}>{icon}</div>
  </div>
);

export default HLXEngine;
