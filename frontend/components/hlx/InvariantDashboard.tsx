import React from 'react';
import { ShieldCheck, AlertTriangle } from 'lucide-react';

interface InvariantDashboardProps {
  invariants: Record<string, boolean>;
}

const InvariantDashboard: React.FC<InvariantDashboardProps> = ({ invariants }) => {
  return (
    <div className="grid grid-cols-1 gap-2">
      {Object.entries(invariants).map(([name, passed]) => (
        <div 
          key={name} 
          className={`flex items-center justify-between p-2 rounded text-[10px] font-bold font-mono border ${
            passed 
              ? 'bg-green-500/10 border-green-500/20 text-green-400' 
              : 'bg-red-500/10 border-red-500/20 text-red-400'
          }`}
        >
          <span>{name}</span>
          {passed ? <ShieldCheck size={12} /> : <AlertTriangle size={12} />}
        </div>
      ))}
    </div>
  );
};

export default InvariantDashboard;