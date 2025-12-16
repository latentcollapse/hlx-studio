import React, { useState, useMemo } from 'react';
import { Search, Hash } from 'lucide-react';
import { CONTRACT_DB } from '../data';
import { HLXContract } from '../types';

const ContractExplorer: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  
  const filteredContracts = useMemo(() => {
    return CONTRACT_DB.filter(c => 
      c.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
      c.layer.toLowerCase().includes(searchTerm.toLowerCase()) ||
      c.id.toString().includes(searchTerm)
    );
  }, [searchTerm]);

  return (
    <div className="space-y-6 h-[calc(100vh-4rem)] flex flex-col">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white">Contract Registry</h2>
          <p className="text-hlx-muted text-sm mt-1">HLX-Lite Core Definitions ({CONTRACT_DB.length})</p>
        </div>
        <div className="relative w-96">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-hlx-muted w-4 h-4" />
          <input 
            type="text" 
            placeholder="Search contracts..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-hlx-surface border border-hlx-border rounded-lg pl-10 pr-4 py-2 text-sm text-hlx-text focus:outline-none focus:border-hlx-accent transition-colors"
          />
        </div>
      </div>

      <div className="flex-1 overflow-auto rounded-xl border border-hlx-border bg-hlx-surface">
        <table className="w-full text-left text-sm">
          <thead className="bg-hlx-bg border-b border-hlx-border sticky top-0 z-10">
            <tr>
              <th className="p-4 font-mono text-hlx-muted w-24">ID</th>
              <th className="p-4 font-mono text-hlx-muted">Name</th>
              <th className="p-4 font-mono text-hlx-muted">Layer</th>
              <th className="p-4 font-mono text-hlx-muted">Fields</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-hlx-border/50">
            {filteredContracts.map((contract) => (
              <ContractRow key={contract.id} contract={contract} />
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

const ContractRow: React.FC<{ contract: HLXContract }> = ({ contract }) => {
  const fields = Array.isArray(contract.fields) ? contract.fields : [];

  return (
    <tr className="hover:bg-hlx-bg/50 transition-colors group cursor-pointer">
      <td className="p-4 font-mono text-hlx-accent">
        <div className="flex items-center gap-1">
          <Hash size={12} className="opacity-50" />
          {contract.id}
        </div>
      </td>
      <td className="p-4 font-bold text-white">{contract.name}</td>
      <td className="p-4">
        <span className="px-2 py-1 rounded text-xs bg-hlx-bg border border-hlx-border text-hlx-muted font-mono">
          {contract.layer}
        </span>
      </td>
      <td className="p-4 font-mono text-xs text-hlx-muted">
        <div className="flex flex-wrap gap-2">
          {fields.map((f: any) => (
            <span key={f.index} className="flex items-center gap-1 bg-hlx-bg/30 px-1.5 py-0.5 rounded border border-hlx-border/30">
              <span className="text-hlx-secondary">{f.index}</span>
              <span>{f.name}</span>
              <span className="opacity-50 text-[10px]">: {f.type}</span>
            </span>
          ))}
        </div>
      </td>
    </tr>
  );
};

export default ContractExplorer;