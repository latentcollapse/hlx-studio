
import React from 'react';
import { HLX_BOOTSTRAP_CODEX } from '../codex_data';
import { ChevronRight, ChevronDown, FileJson, Download } from 'lucide-react';

const JSONSpecViewer: React.FC = () => {
  const downloadSpec = () => {
    const jsonString = JSON.stringify(HLX_BOOTSTRAP_CODEX, null, 2);
    // FIX: Use TextEncoder to guarantee UTF-8 bytes, avoiding Data URI encoding issues
    const encoder = new TextEncoder();
    const utf8Bytes = encoder.encode(jsonString);
    const blob = new Blob([utf8Bytes], { type: 'application/json;charset=utf-8' });
    
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = "hlx_codex_v0.1.0.json";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6 h-[calc(100vh-4rem)] flex flex-col">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-3">
            <FileJson className="text-hlx-secondary" />
            HLX-Lite Codex v0.1.0
          </h2>
          <p className="text-hlx-muted text-sm mt-1">Full hierarchical definition of the v0.1 Foundation (Bootstrap).</p>
        </div>
        <button 
          onClick={downloadSpec}
          className="flex items-center gap-2 px-4 py-2 bg-hlx-surface border border-hlx-border rounded-lg text-sm font-medium text-hlx-text hover:bg-hlx-bg hover:text-white transition-colors"
        >
          <Download size={16} />
          Download JSON
        </button>
      </div>
      
      <div className="flex-1 overflow-auto rounded-xl border border-hlx-border bg-[#0d0d0d] p-6 font-mono text-sm">
        <JSONNode data={HLX_BOOTSTRAP_CODEX} label="root" expand={true} />
      </div>
    </div>
  );
};

interface JSONNodeProps {
  data: any;
  label?: string;
  expand?: boolean;
}

const JSONNode: React.FC<JSONNodeProps> = ({ data, label, expand = false }) => {
  const [isOpen, setIsOpen] = React.useState(expand);

  if (data === null) return <div className="ml-4"><span className="text-hlx-muted">{label}:</span> <span className="text-red-400">null</span></div>;
  if (typeof data !== 'object') {
    let valueColor = 'text-green-400';
    if (typeof data === 'number') valueColor = 'text-blue-400';
    if (typeof data === 'boolean') valueColor = 'text-purple-400';
    
    return (
      <div className="ml-4 hover:bg-white/5 py-0.5 rounded px-1">
        <span className="text-hlx-muted">{label}:</span> <span className={`${valueColor} break-all`}>{JSON.stringify(data)}</span>
      </div>
    );
  }

  const isArray = Array.isArray(data);
  const keys = Object.keys(data);
  const isEmpty = keys.length === 0;

  return (
    <div className="ml-4">
      <div 
        className="flex items-center gap-1 cursor-pointer hover:text-white text-hlx-muted select-none py-0.5"
        onClick={() => setIsOpen(!isOpen)}
      >
        {isEmpty ? (
           <div className="w-4" />
        ) : (
          isOpen ? <ChevronDown size={14} /> : <ChevronRight size={14} />
        )}
        <span className="text-hlx-secondary">{label}</span>
        <span className="text-gray-600">{isArray ? '[' : '{'}</span>
        {!isOpen && !isEmpty && <span className="text-gray-600 text-xs">...</span>}
        {!isOpen && !isEmpty && <span className="text-gray-600">{isArray ? ']' : '}'}</span>}
      </div>

      {isOpen && !isEmpty && (
        <div className="border-l border-hlx-border/30 ml-2 pl-2">
          {keys.map(key => (
            <JSONNode key={key} data={data[key]} label={isArray ? '' : key} />
          ))}
        </div>
      )}
      
      {isOpen && !isEmpty && (
        <div className="ml-6 text-gray-600">
           {isArray ? ']' : '}'}
        </div>
      )}
    </div>
  );
};

export default JSONSpecViewer;
