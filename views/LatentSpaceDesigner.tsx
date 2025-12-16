
import React, { useState } from 'react';
import { Network, FileText, Code, Box, GitBranch, ArrowRight, Shield, Search, AlertOctagon, CheckCircle, Sparkles, Database, Play, RefreshCw, Layers, Camera } from 'lucide-react';
import { STUDIO_LAYER_MAP } from '../data';

// Unicode Subscript Map
const SUBSCRIPT_MAP: Record<string, string> = {
  '₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4',
  '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9'
};

const ASCII_SUBSCRIPT_MAP_REV: Record<string, string> = Object.entries(SUBSCRIPT_MAP).reduce((acc, [k, v]) => ({...acc, [v]: k}), {});

const UNICODE_PREFIXES = ["⟁", "⚚", "◬", "⌬", "◆"];

// Payload Data for Pass 2.5
const SEED_TABLE = {
  table_id: "bootstrap_table",
  engine_id: "gemini_x",
  entries: [
    { handle: "&h_ast_1", value: "{14:{@0:123}}", fingerprint: "a1f3" },
    { handle: "&h_scene_2", value: "{15:{@0:\"hello\",@1:[1,2,3]}}", fingerprint: "b7e2" },
    { handle: "&h_kernel_9", value: "{16:{@0:\"k\",@1:42}}", fingerprint: "c9d0" }
  ]
};

// Helper: Convert ASCII digit string to Unicode Subscript
const toSubscript = (numStr: string) => {
    return numStr.split('').map(c => ASCII_SUBSCRIPT_MAP_REV[c] || c).join('');
};

// Helper: Convert ASCII Handle (&h_tag_id) to Unicode (⟁tag_id)
const toUnicodeHandle = (asciiHandle: string) => {
    const parts = asciiHandle.substring(3).split('_'); // remove &h_
    // Heuristic: If multiple parts, last is ID, rest is tag
    if (parts.length === 1) return `⟁${toSubscript(parts[0])}`;
    
    const id = parts.pop()!;
    const tag = parts.join('');
    return `⟁${tag}${toSubscript(id)}`;
};

const LatentSpaceDesigner: React.FC = () => {
  const lsLayer = STUDIO_LAYER_MAP._hlx_unified_codex.layers['4_hlx_core'] || { status: 'UNKNOWN', description: 'Core Layer', contracts: {} };
  const contracts = lsLayer?.contracts || {};
  
  // Playground State (ASCII)
  const [asciiHandleInput, setAsciiHandleInput] = useState('&h_ast_1');
  const [asciiValidation, setAsciiValidation] = useState<{valid: boolean, error?: string, parsed?: any} | null>(null);

  // Playground State (Unicode)
  const [unicodeHandleInput, setUnicodeHandleInput] = useState('⟁state₁');
  const [unicodeValidation, setUnicodeValidation] = useState<{valid: boolean, error?: string, parsed?: any} | null>(null);

  // Simulator State (Pass 2.5 & 3)
  const [simTable, setSimTable] = useState(SEED_TABLE.entries);
  const [collapseInput, setCollapseInput] = useState('{14:{@0:999}}');
  const [collapseTag, setCollapseTag] = useState('tmp');
  const [simLog, setSimLog] = useState<Array<{action: string, result: string, status: 'success' | 'info'}>>([
    { action: "INIT", result: "Bootstrap Table Loaded (3 entries)", status: 'info' }
  ]);
  const [resolveTarget, setResolveTarget] = useState(SEED_TABLE.entries[0].handle);
  
  // Instruction Envelope State (Pass 3)
  const [envelopeInspector, setEnvelopeInspector] = useState<{
      op: 'RESOLVE' | 'COLLAPSE' | 'SNAPSHOT',
      asciiEnv: object,
      unicodeEnv: string,
      hlxLiteEnv: string
  } | null>(null);


  // --- ASCII VALIDATION LOGIC ---
  const validateAsciiHandle = (str: string) => {
    if (!str.startsWith('&h_')) return { valid: false, error: 'Must start with "&h_"' };
    if (/\s/.test(str)) return { valid: false, error: 'Whitespace is forbidden (E_INVALID_CHAR)' };
    if (!/^&h_[a-zA-Z0-9_]+$/.test(str)) return { valid: false, error: 'Contains invalid characters (only alphanumeric + underscore)' };

    const content = str.substring(3);
    if (content.length === 0) return { valid: false, error: 'Handle ID/Tag cannot be empty' };

    const parts = content.split('_');
    const isExtended = parts.length > 1;
    if (parts.some(p => p.length === 0)) return { valid: false, error: 'Empty segment detected (consecutive underscores)' };

    return { 
        valid: true, 
        parsed: {
            tag: isExtended ? parts[0] : null,
            id: isExtended ? parts.slice(1).join('_') : parts[0],
            canonical: true
        }
    };
  };

  // --- UNICODE VALIDATION LOGIC ---
  const validateUnicodeHandle = (str: string) => {
    // 1. Prefix Check
    const prefix = UNICODE_PREFIXES.find(p => str.startsWith(p));
    if (!prefix) return { valid: false, error: 'Must start with valid glyph (⟁, ⚚, ◬, ⌬, ◆)' };
    
    // 2. Content Extraction
    const content = str.substring(prefix.length);
    if (content.length === 0) return { valid: false, error: 'Handle body cannot be empty' };

    // 3. Strict Character Constraint (Alpha + Digits + Subscripts only)
    if (/[^a-zA-Z0-9₀-₉]/.test(content)) return { valid: false, error: 'Contains invalid characters. Only Alphabets, Digits, and Subscripts allowed.' };

    // 4. Strict Regex Split: Microtag (Leading Alpha) | ID Core (Digits/Subscripts)
    const match = content.match(/^([a-zA-Z]*)([\d₀-₉]+)$/);
    
    if (!match) {
        if (/[a-zA-Z]$/.test(content)) return { valid: false, error: 'ID Core cannot contain letters (Microtag must be leading alphabetic segment).' };
        if (!/[\d₀-₉]/.test(content)) return { valid: false, error: 'ID Core is empty (Handle must contain digits or subscripts).' };
        return { valid: false, error: 'Malformed structure. Expected: <Prefix><Microtag?><ID_Core>.' };
    }

    const rawTag = match[1];
    const rawIdCore = match[2];

    // 5. Normalization
    let normalizedId = '';
    for (const char of rawIdCore) {
        if (SUBSCRIPT_MAP[char]) {
            normalizedId += SUBSCRIPT_MAP[char];
        } else {
            normalizedId += char;
        }
    }

    if (normalizedId.length === 0) return { valid: false, error: 'Normalized ID is empty.' };

    return {
        valid: true,
        parsed: {
            prefix,
            rawBody: content,
            microtag: rawTag || null,
            rawIdCore,
            normalizedId,
            asciiEquivalent: `&h_${rawTag ? rawTag + '_' : ''}${normalizedId}`
        }
    };
  };

  // --- SIMULATOR LOGIC ---
  const generateLSOp = (
      opCode: number, 
      tableId: string, 
      handle?: string, 
      value?: string, 
      hintTag?: string, 
      includeValues?: boolean
  ) => {
      // Contract 820: {820:{@0:op,@1:table,@2:handle,@3:value,@4:tag,@5:inc,@6:profile}}
      // Note: Values must be valid HLX-Lite strings. Nulls are simplified here for demo.
      const handleStr = handle ? `"${handle}"` : 'null';
      const valueStr = value ? value : 'null'; // Value is already HLX-Lite formatted usually
      const tagStr = hintTag ? `"${hintTag}"` : 'null';
      const incStr = includeValues !== undefined ? (includeValues ? 'true' : 'false') : 'null';
      
      return `{820:{@0:${opCode},@1:"${tableId}",@2:${handleStr},@3:${valueStr},@4:${tagStr},@5:${incStr},@6:"hlx-ls-op-0.1"}}`;
  };

  const handleResolve = () => {
    // 1. Envelope Generation
    const asciiEnv = { ls_op: "RESOLVE", table: SEED_TABLE.table_id, handle: resolveTarget };
    const unicodeEnv = `⚚RESOLVE ${toUnicodeHandle(resolveTarget)} IN ${SEED_TABLE.table_id}`;
    const hlxLiteEnv = generateLSOp(0, SEED_TABLE.table_id, resolveTarget);

    setEnvelopeInspector({ op: 'RESOLVE', asciiEnv, unicodeEnv, hlxLiteEnv });

    // 2. Logic
    const entry = simTable.find(e => e.handle === resolveTarget);
    if (entry) {
        setSimLog(prev => [{ 
            action: `RESOLVE ${resolveTarget}`, 
            result: `Found: ${entry.value} (fp: ${entry.fingerprint})`, 
            status: 'success' 
        }, ...prev]);
    } else {
        setSimLog(prev => [{ 
            action: `RESOLVE ${resolveTarget}`, 
            result: "Handle not found in active table.", 
            status: 'info' 
        }, ...prev]);
    }
  };

  const handleCollapse = () => {
    // 1. Envelope Generation
    const asciiEnv = { ls_op: "COLLAPSE", table: SEED_TABLE.table_id, value_hlx_lite: collapseInput, hint_class_tag: collapseTag };
    const unicodeEnv = `⚚COLLAPSE ⟪${collapseInput}⟫ INTO ${SEED_TABLE.table_id} AS ${collapseTag}`;
    const hlxLiteEnv = generateLSOp(1, SEED_TABLE.table_id, undefined, collapseInput, collapseTag);

    setEnvelopeInspector({ op: 'COLLAPSE', asciiEnv, unicodeEnv, hlxLiteEnv });

    // 2. Logic
    const existing = simTable.find(e => e.value === collapseInput);
    if (existing) {
        setSimLog(prev => [{ 
            action: "COLLAPSE", 
            result: `Value exists! Reusing handle: ${existing.handle}`, 
            status: 'success' 
        }, ...prev]);
        return;
    }

    const newId = Math.floor(Math.random() * 1000);
    const newHandle = `&h_${collapseTag}_${newId}`;
    const newFp = Math.random().toString(16).substr(2, 4);
    
    const newEntry = { handle: newHandle, value: collapseInput, fingerprint: newFp };
    setSimTable(prev => [...prev, newEntry]);
    
    setSimLog(prev => [{ 
        action: "COLLAPSE", 
        result: `New Entry Created: ${newHandle}`, 
        status: 'success' 
    }, ...prev]);
  };

  const handleSnapshot = () => {
     // 1. Envelope Generation
     const asciiEnv = { ls_op: "SNAPSHOT", table: SEED_TABLE.table_id, include_values: true };
     const unicodeEnv = `⚚SNAPSHOT TABLE ${SEED_TABLE.table_id} WITH_VALUES`;
     const hlxLiteEnv = generateLSOp(2, SEED_TABLE.table_id, undefined, undefined, undefined, true);

     setEnvelopeInspector({ op: 'SNAPSHOT', asciiEnv, unicodeEnv, hlxLiteEnv });

     setSimLog(prev => [{ 
        action: "SNAPSHOT", 
        result: `Generated snapshot of ${simTable.length} entries.`, 
        status: 'success' 
    }, ...prev]);
  };

  const handleVerify = () => {
     const count = simTable.length;
     setSimLog(prev => [{ 
        action: "VERIFY", 
        result: `Identity Persistence Check: ${count} handles valid. Table Integrity OK.`, 
        status: 'success' 
    }, ...prev]);
  };

  React.useEffect(() => {
    setAsciiValidation(validateAsciiHandle(asciiHandleInput));
  }, [asciiHandleInput]);

  React.useEffect(() => {
    setUnicodeValidation(validateUnicodeHandle(unicodeHandleInput));
  }, [unicodeHandleInput]);

  return (
    <div className="space-y-8 animate-fade-in pb-12">
      <header>
        <h2 className="text-3xl font-bold text-white flex items-center gap-3">
          <Network className="text-pink-500" />
          Latent Space Architecture
        </h2>
        <div className="flex gap-4 mt-2 items-center">
            <p className="text-hlx-muted text-sm max-w-2xl">
            {lsLayer.description}
            </p>
            <span className="px-3 py-1 rounded-full border border-pink-500/20 bg-pink-500/10 text-pink-400 text-xs font-mono font-bold uppercase">
                {lsLayer.status.replace('_', ' ')}
            </span>
        </div>
      </header>

      {/* 4-Lane Visualization */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Unicode Family */}
        <div className="space-y-4">
            <div className="flex items-center gap-2 text-hlx-accent font-bold uppercase text-xs tracking-wider">
                <FileText size={14} /> Unicode Family (LLM Native)
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <LaneCard 
                    title="HLX (Surface)" 
                    symbol="🜁"
                    desc="Glyph-based syntax for LLM authoring."
                    color="border-hlx-accent/50 bg-hlx-accent/5"
                />
                <LaneCard 
                    title="HLX-LS (Latent)" 
                    symbol="⟁state₁"
                    desc="Glyph handles for compressed references."
                    color="border-hlx-accent/50 bg-hlx-accent/5"
                    isLatent
                />
            </div>
        </div>

        {/* ASCII Family */}
        <div className="space-y-4">
            <div className="flex items-center gap-2 text-purple-400 font-bold uppercase text-xs tracking-wider">
                <Code size={14} /> ASCII Family (Runtime Native)
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <LaneCard 
                    title="HLXL (Surface)" 
                    symbol="{12:...}"
                    desc="ASCII syntax for tooling & interop."
                    color="border-purple-500/50 bg-purple-500/5"
                />
                <LaneCard 
                    title="HLXL-LS (Latent)" 
                    symbol="&h_a1"
                    desc="ASCII handles for stable caching."
                    color="border-purple-500/50 bg-purple-500/5"
                    isLatent
                />
            </div>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
          
          {/* HLX-LS (Unicode) Playground */}
          <section className="bg-hlx-surface/50 border border-hlx-border rounded-xl p-6 flex flex-col h-full">
            <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <Sparkles size={20} className="text-hlx-accent" />
                HLX-LS (Unicode Lane)
            </h3>
            
            <div className="space-y-6 flex-1">
                <div className="space-y-2">
                    <label className="text-xs font-bold text-hlx-muted uppercase tracking-wider">Unicode Handle Input</label>
                    <input 
                        type="text" 
                        value={unicodeHandleInput}
                        onChange={(e) => setUnicodeHandleInput(e.target.value)}
                        className={`w-full bg-hlx-bg border rounded px-4 py-3 font-mono text-lg text-white focus:outline-none 
                            ${unicodeValidation?.valid ? 'border-hlx-accent/50 focus:border-hlx-accent' : 'border-red-500/50 focus:border-red-500'}`}
                        placeholder="⟁state₁"
                    />
                    <div className="flex gap-2">
                        {UNICODE_PREFIXES.map(p => (
                            <button key={p} onClick={() => setUnicodeHandleInput(p + "item₁")} className="px-2 py-1 bg-hlx-bg border border-hlx-border rounded hover:border-hlx-accent text-xs font-mono text-hlx-accent">
                                {p}
                            </button>
                        ))}
                    </div>
                </div>

                <div className="bg-[#09090b] border border-hlx-border rounded p-4 font-mono text-sm min-h-[160px]">
                    {unicodeValidation?.valid ? (
                        <div className="space-y-3">
                             <div className="flex justify-between border-b border-hlx-border/50 pb-2">
                                <span className="text-hlx-muted">Structure:</span>
                                <span className="text-hlx-accent font-bold flex items-center gap-1"><CheckCircle size={12}/> VALID GLYPH</span>
                            </div>
                            
                            {/* Normalization Pipeline Viz */}
                            <div className="space-y-2 mt-4">
                                <div className="text-[10px] uppercase font-bold text-hlx-muted tracking-widest mb-1">Normalization Pipeline</div>
                                <div className="flex items-center gap-2 text-xs">
                                   <div className="px-2 py-1 bg-hlx-surface border border-hlx-border rounded text-white font-mono">{unicodeValidation.parsed.rawBody}</div>
                                   <ArrowRight size={12} className="text-hlx-muted" />
                                   <div className="flex gap-1">
                                      <span className="px-2 py-1 bg-purple-500/10 border border-purple-500/20 rounded text-purple-300 font-mono" title="Microtag">{unicodeValidation.parsed.microtag || '∅'}</span>
                                      <span className="px-2 py-1 bg-blue-500/10 border border-blue-500/20 rounded text-blue-300 font-mono" title="Raw ID Core">{unicodeValidation.parsed.rawIdCore}</span>
                                   </div>
                                   <ArrowRight size={12} className="text-hlx-muted" />
                                   <div className="px-2 py-1 bg-green-500/10 border border-green-500/20 rounded text-green-300 font-mono font-bold">{unicodeValidation.parsed.asciiEquivalent}</div>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="text-red-400 space-y-2">
                             <div className="flex items-center gap-2 font-bold">
                                <AlertOctagon size={14} /> PARSE ERROR
                            </div>
                            <div className="text-xs opacity-80 pl-6 border-l border-red-500/30">
                                {unicodeValidation?.error}
                            </div>
                        </div>
                    )}
                </div>

                {/* Translation Bridge */}
                {unicodeValidation?.valid && (
                    <div className="p-3 bg-hlx-accent/5 border border-hlx-accent/20 rounded text-xs">
                        <div className="text-hlx-accent font-bold mb-2 flex items-center gap-2">
                            <ArrowRight size={14} /> HLX-Lite Projection
                        </div>
                        <div className="font-mono text-hlx-muted">
                           &#123;<span className="text-purple-400">800</span>:&#123;
                           <span className="text-pink-400">@0</span>:"{unicodeValidation.parsed.normalizedId}", 
                           <span className="text-pink-400">@1</span>:"{unicodeValidation.parsed.microtag || ''}"
                           &#125;&#125;
                        </div>
                    </div>
                )}
            </div>
          </section>

          {/* HLXL-LS (ASCII) Playground */}
          <section className="bg-hlx-surface/50 border border-hlx-border rounded-xl p-6 flex flex-col h-full">
            <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <Code size={20} className="text-purple-400" />
                HLXL-LS (ASCII Lane)
            </h3>
            
            <div className="space-y-6 flex-1">
                <div className="space-y-2">
                    <label className="text-xs font-bold text-hlx-muted uppercase tracking-wider">ASCII Handle Input</label>
                    <input 
                        type="text" 
                        value={asciiHandleInput}
                        onChange={(e) => setAsciiHandleInput(e.target.value)}
                        className={`w-full bg-hlx-bg border rounded px-4 py-3 font-mono text-lg text-white focus:outline-none 
                            ${asciiValidation?.valid ? 'border-green-500/50 focus:border-green-500' : 'border-red-500/50 focus:border-red-500'}`}
                        placeholder="&h_class_tag_id"
                    />
                </div>
                
                <div className="bg-[#09090b] border border-hlx-border rounded p-4 font-mono text-sm min-h-[160px]">
                    {asciiValidation?.valid ? (
                        <div className="space-y-3">
                            <div className="flex justify-between border-b border-hlx-border/50 pb-2">
                                <span className="text-hlx-muted">Structure:</span>
                                <span className="text-green-400 font-bold flex items-center gap-1"><CheckCircle size={12}/> VALID CANONICAL</span>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <div className="text-xs text-hlx-muted mb-1">Class Tag</div>
                                    <div className="text-purple-400">{asciiValidation.parsed.tag || <span className="text-gray-600 italic">None</span>}</div>
                                </div>
                                <div>
                                    <div className="text-xs text-hlx-muted mb-1">Handle ID</div>
                                    <div className="text-white">{asciiValidation.parsed.id}</div>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="text-red-400 space-y-2">
                            <div className="flex items-center gap-2 font-bold">
                                <AlertOctagon size={14} /> NON-CANONICAL
                            </div>
                            <div className="text-xs opacity-80 pl-6 border-l border-red-500/30">
                                {asciiValidation?.error}
                            </div>
                        </div>
                    )}
                </div>

                 {/* Translation Bridge */}
                 {asciiValidation?.valid && (
                    <div className="p-3 bg-purple-500/5 border border-purple-500/20 rounded text-xs">
                        <div className="text-purple-400 font-bold mb-2 flex items-center gap-2">
                            <ArrowRight size={14} /> HLX-Lite Projection
                        </div>
                        <div className="font-mono text-hlx-muted">
                           &#123;<span className="text-purple-400">800</span>:&#123;
                           <span className="text-pink-400">@0</span>:"{asciiValidation.parsed.id}", 
                           <span className="text-pink-400">@1</span>:"{asciiValidation.parsed.tag || ''}"
                           &#125;&#125;
                        </div>
                    </div>
                )}
            </div>
        </section>
      </div>

      {/* NEW: Bootstrap Verification Simulator (Pass 2.5 & 3) */}
      <section className="mt-8 border-t border-hlx-border pt-8">
        <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-3">
             <Database size={20} className="text-yellow-400" />
             Latent Engine Simulator (Bootstrap Pass 3)
        </h3>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* 1. Latent Table State */}
            <div className="bg-hlx-surface border border-hlx-border rounded-xl p-4 flex flex-col">
                <div className="text-xs font-bold text-hlx-muted uppercase tracking-wider mb-3 flex justify-between items-center">
                    <span>Active Latent Table</span>
                    <span className="text-[10px] bg-green-900/30 text-green-400 px-2 py-0.5 rounded">{simTable.length} Entries</span>
                </div>
                <div className="flex-1 bg-[#09090b] rounded border border-hlx-border p-3 overflow-y-auto max-h-[300px]">
                    <div className="space-y-2">
                        {simTable.map((entry, idx) => (
                            <div key={idx} className="p-2 border border-hlx-border/30 rounded bg-white/5 text-xs font-mono">
                                <div className="flex justify-between text-yellow-400 font-bold mb-1">
                                    <span>{entry.handle}</span>
                                    <span className="opacity-50 text-[10px]">fp: {entry.fingerprint}</span>
                                </div>
                                <div className="text-hlx-muted break-all">{entry.value}</div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* 2. Interactive Console & Inspector */}
            <div className="bg-hlx-surface border border-hlx-border rounded-xl p-4 flex flex-col lg:col-span-2">
                <div className="text-xs font-bold text-hlx-muted uppercase tracking-wider mb-3 flex gap-4">
                    <button className="flex items-center gap-2 hover:text-white transition-colors" onClick={handleResolve}>
                        <Play size={12} /> Resolve
                    </button>
                    <button className="flex items-center gap-2 hover:text-white transition-colors" onClick={handleCollapse}>
                        <Layers size={12} /> Collapse
                    </button>
                    <button className="flex items-center gap-2 hover:text-white transition-colors" onClick={handleSnapshot}>
                        <Camera size={12} /> Snapshot
                    </button>
                    <div className="h-4 w-px bg-hlx-border mx-2" />
                    <button className="flex items-center gap-2 hover:text-white transition-colors" onClick={handleVerify}>
                        <RefreshCw size={12} /> Verify Identity
                    </button>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div className="space-y-1">
                        <label className="text-[10px] text-hlx-muted uppercase">Resolution Target</label>
                        <select 
                             className="w-full bg-[#09090b] border border-hlx-border rounded p-2 text-sm text-white font-mono"
                             value={resolveTarget}
                             onChange={(e) => setResolveTarget(e.target.value)}
                        >
                            {simTable.map(e => <option key={e.handle} value={e.handle}>{e.handle}</option>)}
                            <option value="&h_unknown_99">Invalid Handle</option>
                        </select>
                    </div>
                     <div className="space-y-1">
                        <label className="text-[10px] text-hlx-muted uppercase">Collapse Input (HLX-Lite)</label>
                        <div className="flex gap-2">
                            <input 
                                type="text"
                                className="w-2/3 bg-[#09090b] border border-hlx-border rounded p-2 text-sm text-white font-mono"
                                value={collapseInput}
                                onChange={(e) => setCollapseInput(e.target.value)}
                            />
                            <input 
                                type="text"
                                className="w-1/3 bg-[#09090b] border border-hlx-border rounded p-2 text-sm text-white font-mono"
                                value={collapseTag}
                                onChange={(e) => setCollapseTag(e.target.value)}
                                placeholder="tag"
                            />
                        </div>
                    </div>
                </div>

                {/* Cross-Lane Instruction Envelope Inspector (Pass 3) */}
                {envelopeInspector && (
                    <div className="mb-4 bg-[#09090b] rounded border border-hlx-border p-4 animate-fade-in">
                        <div className="flex justify-between items-center mb-3 pb-2 border-b border-hlx-border/30">
                            <span className="text-xs font-bold text-hlx-accent uppercase tracking-wider flex items-center gap-2">
                                <Network size={14} /> Instruction Envelope (Cross-Lane)
                            </span>
                            <span className="text-[10px] bg-hlx-accent/10 text-hlx-accent px-2 py-0.5 rounded border border-hlx-accent/20 font-bold">
                                {envelopeInspector.op}
                            </span>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs font-mono">
                            <div>
                                <div className="text-[10px] text-hlx-muted uppercase mb-1">Unicode Surface</div>
                                <div className="text-hlx-text break-words bg-hlx-surface/50 p-2 rounded border border-hlx-border/30">
                                    {envelopeInspector.unicodeEnv}
                                </div>
                            </div>
                            <div>
                                <div className="text-[10px] text-purple-400 uppercase mb-1">ASCII Surface (HLXL-LS)</div>
                                <div className="text-purple-300 break-words bg-purple-500/5 p-2 rounded border border-purple-500/20">
                                    {JSON.stringify(envelopeInspector.asciiEnv, null, 1).replace(/\n/g, '').replace(/\s+/g, ' ')}
                                </div>
                            </div>
                            <div>
                                <div className="text-[10px] text-green-400 uppercase mb-1">Canonical HLX-Lite (Contract 820)</div>
                                <div className="text-green-300 break-all bg-green-500/5 p-2 rounded border border-green-500/20">
                                    {envelopeInspector.hlxLiteEnv}
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {/* Log Output */}
                <div className="flex-1 bg-black rounded border border-hlx-border p-3 font-mono text-xs overflow-y-auto h-[150px]">
                    {simLog.map((log, i) => (
                        <div key={i} className="mb-1">
                            <span className="text-hlx-muted opacity-50 mr-2">[{simLog.length - i}]</span>
                            <span className="text-blue-400 font-bold mr-2">{log.action}:</span>
                            <span className={log.status === 'success' ? 'text-green-400' : 'text-hlx-text'}>{log.result}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
      </section>

      {/* Latent Contracts */}
      <section>
          <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <GitBranch size={20} className="text-hlx-secondary" />
            Latent Contracts (Layer 4)
          </h3>
          <div className="bg-hlx-surface border border-hlx-border rounded-xl overflow-hidden">
             <table className="w-full text-left text-sm">
                <thead className="bg-hlx-bg border-b border-hlx-border text-hlx-muted font-mono text-xs uppercase">
                    <tr>
                        <th className="p-4">ID</th>
                        <th className="p-4">Name</th>
                        <th className="p-4">Definition</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-hlx-border/50">
                    {Object.entries(contracts).map(([key, def]: [string, any]) => {
                        const [id, name] = key.split(':');
                        return (
                            <tr key={key} className="hover:bg-hlx-bg/50">
                                <td className="p-4 font-mono text-pink-400">{id}</td>
                                <td className="p-4 font-bold text-white">{name}</td>
                                <td className="p-4">
                                    <div className="space-y-1">
                                        {/* Use fields or default to empty if not present in new shim */}
                                        {def.fields && Object.entries(def.fields).map(([fKey, fType]: [string, any]) => (
                                            <div key={fKey} className="font-mono text-xs flex gap-2">
                                                <span className="text-hlx-muted w-24 text-right">{fKey.split(':')[1]}</span>
                                                <span className="text-hlx-accent">{fType}</span>
                                            </div>
                                        ))}
                                    </div>
                                </td>
                            </tr>
                        );
                    })}
                </tbody>
             </table>
          </div>
      </section>
    </div>
  );
};

const LaneCard: React.FC<{title: string, symbol: string, desc: string, color: string, isLatent?: boolean}> = ({title, symbol, desc, color, isLatent}) => (
    <div className={`p-4 rounded-xl border ${color} relative overflow-hidden group`}>
        {isLatent && (
            <div className="absolute top-0 right-0 p-1 bg-black/20 rounded-bl text-[10px] font-bold uppercase text-hlx-muted px-2">
                Compressed
            </div>
        )}
        <div className="flex justify-between items-start mb-2">
            <h4 className="font-bold text-white">{title}</h4>
        </div>
        <div className="text-3xl font-mono text-white/90 mb-3">{symbol}</div>
        <p className="text-xs text-hlx-muted">{desc}</p>
    </div>
);

export default LatentSpaceDesigner;
