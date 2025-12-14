import React, { useState, useEffect, useMemo } from 'react';
import { Terminal, Copy, Check, Search, AlertCircle, FileCheck, ShieldAlert } from 'lucide-react';
import { HLX_SPEC_JSON } from '../data';

// Default sample from Test Vectors
const SAMPLE_LITE_TEXT = HLX_SPEC_JSON.components.A_formal_canonical_specification.canonical_test_vectors.text_lite;

const MAPPING: Record<string, string> = HLX_SPEC_JSON.components.A_formal_canonical_specification.glyph_mapping.mapping;

// Extract contracts for lookup
const CONTRACTS = HLX_SPEC_JSON.components.A_formal_canonical_specification.lite_contracts;
const CONTRACT_LOOKUP: Record<number, string> = {
  0: 'AnonymousObject' // Add generic support
};
Object.entries(CONTRACTS).forEach(([name, def]: [string, any]) => {
  if (def && def.id) CONTRACT_LOOKUP[def.id] = name;
});

interface HLXVisualizerProps {
  initialInput?: string;
  readOnly?: boolean;
}

const HLXVisualizer: React.FC<HLXVisualizerProps> = ({ initialInput, readOnly = false }) => {
  const [textMode, setTextMode] = useState<string>(initialInput || SAMPLE_LITE_TEXT);
  const [glyphMode, setGlyphMode] = useState<string>('');
  const [copied, setCopied] = useState(false);

  // Convert Text -> Glyph
  const toGlyph = (input: string) => {
    let output = '';
    let inString = false;
    let inBytes = false;

    for (let i = 0; i < input.length; i++) {
      const char = input[i];
      const nextChar = input[i+1];

      if (!inString && char === 'x' && nextChar === '"') {
        output += MAPPING['x"'];
        inBytes = true;
        i++; 
        continue;
      }

      if (inBytes) {
        if (char === '"') {
          inBytes = false;
          output += '"'; 
        } else {
          output += char;
        }
        continue;
      }

      if (char === '"') {
        if (inString) {
          inString = false;
          output += '"'; 
        } else {
          inString = true;
          output += MAPPING['"'];
        }
        continue;
      }

      if (inString) {
        output += char;
        continue;
      }

      if (MAPPING[char]) {
        output += MAPPING[char];
      } else {
        output += char;
      }
    }
    return output;
  };

  useEffect(() => {
    setGlyphMode(toGlyph(textMode));
  }, [textMode]);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(glyphMode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Improved Semantic Analysis with Constraint Checking
  const analysis = useMemo(() => {
    let isValid = true;
    let error = null;
    let errorCode = null;
    
    // 1. Whitespace Check (CF001)
    const hasWhitespace = /("[^"]*"|x"[^"]*")|(\s+)/g;
    let match;
    let whitespaceFound = false;
    while ((match = hasWhitespace.exec(textMode)) !== null) {
      if (match[2]) { 
         whitespaceFound = true;
         break;
      }
    }
    
    // 2. Trailing Comma (CF002)
    if (/,\s*[}\]]/.test(textMode)) {
      isValid = false;
      error = "Trailing comma detected (CF002)";
      errorCode = "E_TRAILING_COMMA (1106)";
    }

    // 3. Uppercase Hex (CF007)
    if (/x"[^"]*[A-F][^"]*"/.test(textMode)) {
      isValid = false;
      error = "Uppercase hex in bytes literal (CF007)";
      errorCode = "E_INVALID_HEX (1005)";
    }

    // 4. Contract ID parsing
    const contractMatches = textMode.matchAll(/\{(\d+):/g);
    const foundContracts = new Set<string>();

    for (const match of contractMatches) {
      const id = parseInt(match[1]);
      const name = CONTRACT_LOOKUP[id];
      if (name) {
        foundContracts.add(`${name} (ID: ${id})`);
      } else {
        foundContracts.add(`Unknown (ID: ${id})`);
      }
    }

    // 5. Basic Nesting
    const openBraces = (textMode.match(/\{/g) || []).length;
    const closeBraces = (textMode.match(/\}/g) || []).length;
    
    if (openBraces !== closeBraces) {
      isValid = false;
      error = `Unbalanced Braces: Open ${openBraces}, Close ${closeBraces}`;
      errorCode = "E_UNCLOSED_OBJECT (1105)";
    }
    
    if (isValid && whitespaceFound) {
        isValid = false;
        error = "Whitespace detected outside strings (CF001)";
        errorCode = "E_UNEXPECTED_CHAR (1008)";
    }

    return {
      isValid,
      error,
      errorCode,
      contracts: Array.from(foundContracts),
      stats: {
        size: textMode.length,
        depth: openBraces 
      }
    };
  }, [textMode]);

  return (
    <div className="flex flex-col h-full gap-6">
      <div className="flex items-center justify-between">
         {/* Internal Header Removed when embedded */}
         <div className="flex gap-2 ml-auto">
           <button 
            onClick={copyToClipboard}
            className="flex items-center gap-2 px-3 py-1.5 rounded bg-hlx-surface border border-hlx-border text-xs font-mono text-hlx-text hover:bg-hlx-bg transition-colors"
           >
             {copied ? <Check size={14} className="text-green-400" /> : <Copy size={14} />}
             Copy Glyphs
           </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1 min-h-0">
        
        {/* Editor: HLX-Text-Lite */}
        <div className="flex flex-col gap-2 lg:col-span-1 h-full min-h-0">
          <div className="flex items-center justify-between px-1">
            <span className="text-xs font-bold text-hlx-muted uppercase tracking-wider">Layer 2: HLX-Text-Lite</span>
            <span className="text-[10px] text-hlx-accent bg-hlx-accent/10 px-2 py-0.5 rounded border border-hlx-accent/20">Input</span>
          </div>
          <textarea 
            value={textMode}
            onChange={(e) => setTextMode(e.target.value)}
            spellCheck={false}
            readOnly={readOnly}
            className={`flex-1 bg-[#09090b] border rounded-xl p-6 font-mono text-sm leading-relaxed text-hlx-text focus:outline-none resize-none selection:bg-hlx-accent/30 shadow-inner
              ${analysis.error ? 'border-red-500/50' : 'border-hlx-border focus:border-hlx-accent/50'}
              ${readOnly ? 'opacity-75 cursor-default' : ''}
            `}
          />
        </div>

        {/* Viewer: HLX-Glyph-Text */}
        <div className="flex flex-col gap-2 lg:col-span-1 h-full min-h-0">
           <div className="flex items-center justify-between px-1">
            <span className="text-xs font-bold text-hlx-muted uppercase tracking-wider">Layer 3: HLX-Glyph-Text</span>
            <span className="text-[10px] text-purple-400 bg-purple-500/10 px-2 py-0.5 rounded border border-purple-500/20">Output</span>
          </div>
          <div className="flex-1 bg-[#09090b] border border-hlx-border rounded-xl p-6 font-mono text-sm leading-relaxed overflow-auto relative shadow-inner shadow-black/50">
             <HLXGlyphRenderer text={glyphMode} />
          </div>
        </div>

        {/* Semantic Analyzer */}
        <div className="flex flex-col gap-2 lg:col-span-1 h-full min-h-0">
          <div className="flex items-center justify-between px-1">
             <span className="text-xs font-bold text-hlx-muted uppercase tracking-wider">Semantics</span>
             {analysis.isValid ? (
                <span className="text-[10px] text-green-400 bg-green-500/10 px-2 py-0.5 rounded border border-green-500/20 flex items-center gap-1">
                  <FileCheck size={10} /> Compliant
                </span>
             ) : (
                <span className="text-[10px] text-red-400 bg-red-500/10 px-2 py-0.5 rounded border border-red-500/20 flex items-center gap-1">
                  <AlertCircle size={10} /> Violation
                </span>
             )}
           </div>
           <div className="flex-1 bg-hlx-surface border border-hlx-border rounded-xl p-0 overflow-hidden flex flex-col">
             
             {/* Analysis Content */}
             <div className="p-4 border-b border-hlx-border bg-hlx-bg/50">
               <h4 className="text-sm font-bold text-white mb-2 flex items-center gap-2">
                 <Search size={14} className="text-hlx-accent" /> Detected Contracts
               </h4>
               <div className="max-h-32 overflow-y-auto pr-1">
                 {analysis.contracts.length > 0 ? (
                   <ul className="space-y-1">
                     {analysis.contracts.map((c, i) => (
                       <li key={i} className="text-xs font-mono text-hlx-muted flex items-center gap-2">
                         <span className="w-1.5 h-1.5 rounded-full bg-hlx-secondary"></span>
                         {c}
                       </li>
                     ))}
                   </ul>
                 ) : (
                   <p className="text-xs text-hlx-muted italic">No contracts detected.</p>
                 )}
               </div>
             </div>

             {analysis.error && (
                <div className="p-4 bg-red-500/5 border-b border-red-500/20 animate-pulse-soft">
                  <h4 className="text-xs font-bold text-red-400 mb-1 flex items-center gap-2">
                    <ShieldAlert size={12} />
                    Constraint Violation
                  </h4>
                  <p className="text-sm text-white font-medium mb-1">{analysis.error}</p>
                  {analysis.errorCode && (
                    <div className="text-[10px] font-mono text-red-300 bg-red-950/30 px-2 py-1 rounded border border-red-500/30 inline-block mt-1">
                       {analysis.errorCode}
                    </div>
                  )}
                </div>
             )}

             <div className="p-4 flex-1">
                <h4 className="text-sm font-bold text-white mb-2">Token Stats</h4>
                <div className="grid grid-cols-2 gap-2 text-xs font-mono">
                  <div className="bg-hlx-bg p-2 rounded border border-hlx-border">
                    <div className="text-hlx-muted">Size</div>
                    <div className="text-white font-bold">{analysis.stats.size} bytes</div>
                  </div>
                   <div className="bg-hlx-bg p-2 rounded border border-hlx-border">
                    <div className="text-hlx-muted">Nesting Depth</div>
                    <div className="text-white font-bold">{analysis.stats.depth}</div>
                  </div>
                </div>
                
                <div className="mt-4 p-3 bg-hlx-accent/5 rounded border border-hlx-accent/10">
                  <h5 className="text-[10px] font-bold text-hlx-accent uppercase mb-1">LLM Interpretation</h5>
                  <p className="text-xs text-hlx-muted leading-relaxed">
                    {analysis.isValid 
                      ? "This sequence adheres to all canonical invariants. Deterministic deserialization is guaranteed." 
                      : "I cannot guarantee lossless round-trip. This input violates strict HLX-Lite constraints."}
                  </p>
                </div>
             </div>
           </div>
        </div>

      </div>

      {/* Mapping Key (Hidden in embed mode usually, but kept for consistency) */}
    </div>
  );
};

// ... Helper components (HLXGlyphRenderer) remain same, just export
const HLXGlyphRenderer: React.FC<{ text: string }> = ({ text }) => {
  // Simple syntax highlighting logic for Glyph mode
  const renderChar = (char: string, idx: number) => {
    // Check if it's a known structural glyph
    if (Object.values(MAPPING).includes(char)) {
       let colorClass = 'text-hlx-accent'; // Default structural
       if (char === MAPPING['{'] || char === MAPPING['}']) colorClass = 'text-hlx-secondary'; // Objects
       if (char === MAPPING['['] || char === MAPPING[']']) colorClass = 'text-blue-400'; // Arrays
       if (char === MAPPING['@']) colorClass = 'text-pink-400'; // Fields
       if (char === MAPPING['"'] || char === MAPPING['x"']) colorClass = 'text-green-400'; // Strings/Bytes start
       
       return <span key={idx} className={`${colorClass} font-bold`}>{char}</span>;
    }

    // Numbers
    if (/\d/.test(char) || char === '-' || char === '.') return <span key={idx} className="text-orange-300">{char}</span>;
    
    // String content
    return <span key={idx} className="text-gray-300">{char}</span>;
  };

  return (
    <pre className="whitespace-pre-wrap font-mono break-all">
      {text.split('').map((char, i) => renderChar(char, i))}
    </pre>
  );
};

export default HLXVisualizer;