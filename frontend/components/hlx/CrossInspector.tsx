import React from 'react';
import { ArrowRight, Box, Terminal, Cpu, Layers } from 'lucide-react';

interface HlxCrossInspectorProps {
  activeStage: 'HLXL' | 'HLXL_LS' | 'HLX' | 'HLX_LS' | 'LC';
  onStageSelect: (stage: 'HLXL' | 'HLXL_LS' | 'HLX' | 'HLX_LS' | 'LC') => void;
}

const STAGES = [
  { id: 'HLXL', label: 'HLXL', icon: <Terminal size={14} />, color: 'text-purple-400', bg: 'bg-purple-500/10', border: 'border-purple-500/20' },
  { id: 'HLXL_LS', label: 'HLXL-LS', icon: <Box size={14} />, color: 'text-blue-400', bg: 'bg-blue-500/10', border: 'border-blue-500/20' },
  { id: 'HLX', label: 'HLX', icon: <Cpu size={14} />, color: 'text-[#A44DFB]', bg: 'bg-[#A44DFB]/10', border: 'border-[#A44DFB]/20' },
  { id: 'HLX_LS', label: 'HLX-LS', icon: <Layers size={14} />, color: 'text-pink-400', bg: 'bg-pink-500/10', border: 'border-pink-500/20' },
  { id: 'LC', label: 'LC', icon: <Box size={14} />, color: 'text-[#39F5E5]', bg: 'bg-[#39F5E5]/10', border: 'border-[#39F5E5]/20' },
] as const;

const HlxCrossInspector: React.FC<HlxCrossInspectorProps> = ({ activeStage, onStageSelect }) => {
  return (
    <div className="flex items-center gap-2 p-2 bg-[#050208] border border-[#27272a] rounded-lg overflow-x-auto">
      {STAGES.map((stage, index) => (
        <React.Fragment key={stage.id}>
          <button
            onClick={() => onStageSelect(stage.id)}
            className={`flex items-center gap-2 px-3 py-1.5 rounded transition-all border ${
              activeStage === stage.id 
                ? `${stage.bg} ${stage.border} ${stage.color} ring-1 ring-inset ring-white/10` 
                : 'bg-transparent border-transparent text-gray-500 hover:text-gray-300 hover:bg-white/5'
            }`}
          >
            {stage.icon}
            <span className="text-[10px] font-bold tracking-wider">{stage.label}</span>
          </button>
          {index < STAGES.length - 1 && (
            <ArrowRight size={12} className="text-gray-700 shrink-0" />
          )}
        </React.Fragment>
      ))}
    </div>
  );
};

export default HlxCrossInspector;