// ============================================================================
// HLX Playground - Full Glyph Transliteration Layer
// Supports HLX Passes 0-4 + HLX-LS Passes 1-15
// Drop this into views/HLXPlayground.tsx
// ============================================================================

import React, { useState, useMemo } from 'react';

// -----------------------------------------------------------------------------
// COMPLETE GLYPH TRANSLITERATION MAP
// -----------------------------------------------------------------------------
const HLX_GLYPH_MAP: Record<string, string> = {
  // === HLX Core (Passes 0-4) ===
  '⟠': 'program',
  '◇': 'block',
  '⊢': 'let',
  '⊡': 'local',
  '↩': 'return',
  '❓': 'if',
  '❗': 'else',
  '⟳': 'while',
  '⟲': 'for',
  
  // === HLX-LS Passes 1-5 ===
  'ꙮ': 'latent',
  '⌸': 'table',
  '▣': 'using',
  '⚳': 'ls.collapse',
  '⚯': 'ls.resolve',
  '⚶': 'ls.snapshot',
  '⚷': 'latent',        // collapse-and-bind (followed by IDENT =)
  '⚵': 'latent value',  // resolve-and-bind
  '⚻': 'latent snapshot', // snapshot-and-bind
  
  // === HLX-LS Passes 6-10 ===
  '▷': '|>',             // pipeline
  '⚑': 'latent match',   // pattern match
  '⚐': 'latent guard',   // guard/assert
  '⚳⃰': 'latent batch',   // batch collapse (with combining asterisk)
  '⚯⃰': 'latent resolve batch', // batch resolve
  
  // === HLX-LS Passes 11-15 ===
  '⚳?': 'ls.collapse_if',
  '⚯‖': 'ls.resolve_or',
  '⚿': 'ls.transaction',
  '⚉': 'ls.fingerprint',
  '⚇': 'ls.validate',
  '⌸⑂': 'ls.table_fork',
  '⌸Δ': 'ls.table_diff',
  '⌸⊕': 'ls.table_merge',
};

// Reverse map for HLXL → HLX conversion
const HLXL_TO_HLX_MAP: Record<string, string> = Object.entries(HLX_GLYPH_MAP)
  .reduce((acc, [glyph, hlxl]) => {
    acc[hlxl] = glyph;
    return acc;
  }, {} as Record<string, string>);

// -----------------------------------------------------------------------------
// TRANSLITERATION FUNCTIONS
// -----------------------------------------------------------------------------

/**
 * Transliterate HLX (glyph) source to HLXL (ASCII) source.
 * Order matters: longer sequences must be replaced first.
 */
export function transliterateHLXtoHLXL(source: string): string {
  let result = source;
  
  // Sort by length descending to handle multi-char glyphs first
  const sortedGlyphs = Object.keys(HLX_GLYPH_MAP)
    .sort((a, b) => b.length - a.length);
  
  for (const glyph of sortedGlyphs) {
    const hlxl = HLX_GLYPH_MAP[glyph];
    result = result.split(glyph).join(hlxl);
  }
  
  return result;
}

/**
 * Transliterate HLXL (ASCII) source to HLX (glyph) source.
 * For round-trip verification.
 */
export function transliterateHLXLtoHLX(source: string): string {
  let result = source;
  
  // Sort by length descending
  const sortedKeywords = Object.keys(HLXL_TO_HLX_MAP)
    .sort((a, b) => b.length - a.length);
  
  for (const keyword of sortedKeywords) {
    const glyph = HLXL_TO_HLX_MAP[keyword];
    // Use word boundaries to avoid partial replacements
    const regex = new RegExp(`\\b${escapeRegex(keyword)}\\b`, 'g');
    result = result.replace(regex, glyph);
  }
  
  return result;
}

function escapeRegex(str: string): string {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// -----------------------------------------------------------------------------
// TASK DEFINITIONS - All HLX/LS Passes
// -----------------------------------------------------------------------------
interface Task {
  id: string;
  pass: string;
  title: string;
  description: string;
  hlx_example: string;
  expected_hlxl: string;
}

const HLX_TASKS: Task[] = [
  // === HLX Core Tasks (Passes 1-4) ===
  {
    id: 'hlx-1',
    pass: 'HLX-Pass-1',
    title: 'Structural Glyphs',
    description: 'Use ⟠ (program), ◇ (block), ⊢ (let), ↩ (return)',
    hlx_example: `⟠ hello_world {
  ◇ main() {
    ⊢ x = 1;
    ↩ x;
  }
}`,
    expected_hlxl: `program hello_world {
  block main() {
    let x = 1;
    return x;
  }
}`
  },
  {
    id: 'hlx-2',
    pass: 'HLX-Pass-2',
    title: 'Expressions',
    description: 'HLX reuses HLXL expression syntax unchanged',
    hlx_example: `⟠ math {
  ◇ calc() {
    ⊢ sum = 1 + 2 * 3;
    ⊢ ok = (x > 0) && flag;
    ↩ sum;
  }
}`,
    expected_hlxl: `program math {
  block calc() {
    let sum = 1 + 2 * 3;
    let ok = (x > 0) && flag;
    return sum;
  }
}`
  },
  {
    id: 'hlx-3',
    pass: 'HLX-Pass-3',
    title: 'Control Flow Glyphs',
    description: 'Use ❓ (if), ❗ (else), ⟳ (while), ⟲ (for)',
    hlx_example: `⟠ control {
  ◇ flow() {
    ❓(x > 0) {
      ⊢ sign = "positive";
    } ❗ {
      ⊢ sign = "non-positive";
    }
    
    ⟳(i < 10) {
      ⊢ i = i + 1;
    }
    
    ⟲(item in values) {
      ⊢ total = total + item;
    }
  }
}`,
    expected_hlxl: `program control {
  block flow() {
    if(x > 0) {
      let sign = "positive";
    } else {
      let sign = "non-positive";
    }
    
    while(i < 10) {
      let i = i + 1;
    }
    
    for(item in values) {
      let total = total + item;
    }
  }
}`
  },
  {
    id: 'hlx-4',
    pass: 'HLX-Pass-4',
    title: 'Objects & Arrays',
    description: 'Object literals and arrays pass through unchanged',
    hlx_example: `⟠ data {
  ◇ init() {
    ⊢ values = [1, 2, 3];
    ⊢ node = object 14 {
      @0: 123,
    };
    // sanity check
    assert(node.@0 == 123);
  }
}`,
    expected_hlxl: `program data {
  block init() {
    let values = [1, 2, 3];
    let node = object 14 {
      @0: 123,
    };
    // sanity check
    assert(node.@0 == 123);
  }
}`
  },
  
  // === HLX-LS Tasks (Passes 1-5) ===
  {
    id: 'hlx-ls-1',
    pass: 'HLX-LS-Pass-1',
    title: 'Latent Table Declaration',
    description: 'Declare a latent table with ꙮ ⌸',
    hlx_example: `ꙮ ⌸ bootstrap_table;`,
    expected_hlxl: `latent table bootstrap_table;`
  },
  {
    id: 'hlx-ls-2',
    pass: 'HLX-LS-Pass-2',
    title: 'LS Operations',
    description: 'Use ▣ (using), ⚳ (collapse), ⚯ (resolve), ⚶ (snapshot)',
    hlx_example: `ꙮ ⌸ bootstrap_table;

⟠ demo {
  ◇ main() ▣ bootstrap_table {
    ⊢ ast = object 14 { @0: 123 };
    ⊢ h = ⚳ ast ast;
    ⊢ v = ⚯ h;
    ⊢ snap = ⚶;
  }
}`,
    expected_hlxl: `latent table bootstrap_table;

program demo {
  block main() using bootstrap_table {
    let ast = object 14 { @0: 123 };
    let h = ls.collapse ast ast;
    let v = ls.resolve h;
    let snap = ls.snapshot;
  }
}`
  },
  {
    id: 'hlx-ls-3',
    pass: 'HLX-LS-Pass-3',
    title: 'Collapse-and-Bind',
    description: 'Use ⚷ for collapse-and-bind sugar',
    hlx_example: `⚷ ast = object 14 { @0: 123 };`,
    expected_hlxl: `latent ast = object 14 { @0: 123 };`
  },
  {
    id: 'hlx-ls-4',
    pass: 'HLX-LS-Pass-4',
    title: 'Resolve-and-Bind',
    description: 'Use ⚵ for resolve-and-bind sugar',
    hlx_example: `⚵ value = handle;`,
    expected_hlxl: `latent value value = handle;`
  },
  {
    id: 'hlx-ls-5',
    pass: 'HLX-LS-Pass-5',
    title: 'Snapshot-and-Bind',
    description: 'Use ⚻ for snapshot-and-bind sugar',
    hlx_example: `⚻ table_snapshot;`,
    expected_hlxl: `latent snapshot table_snapshot;`
  },
  
  // === HLX-LS Tasks (Passes 6-10) ===
  {
    id: 'hlx-ls-6',
    pass: 'HLX-LS-Pass-6',
    title: 'Pipeline Operator',
    description: 'Use ▷ for chained transformations',
    hlx_example: `⊢ h = ast ▷ ⚳ node;
⊢ v = h ▷ ⚯;
⊢ result = data ▷ ⚳ raw ▷ ⚯ ▷ process;`,
    expected_hlxl: `let h = ast |> ls.collapse node;
let v = h |> ls.resolve;
let result = data |> ls.collapse raw |> ls.resolve |> process;`
  },
  {
    id: 'hlx-ls-7',
    pass: 'HLX-LS-Pass-7',
    title: 'Pattern Matching',
    description: 'Use ⚑ for latent match blocks',
    hlx_example: `⚑ resolved = some_handle {
  ⊢ x = resolved.@0;
  ↩ x + 1;
}`,
    expected_hlxl: `latent match resolved = some_handle {
  let x = resolved.@0;
  return x + 1;
}`
  },
  {
    id: 'hlx-ls-8',
    pass: 'HLX-LS-Pass-8',
    title: 'Guards',
    description: 'Use ⚐ for latent guard assertions',
    hlx_example: `⚐ handle != null;
⚐ count > 0;`,
    expected_hlxl: `latent guard handle != null;
latent guard count > 0;`
  },
  {
    id: 'hlx-ls-9',
    pass: 'HLX-LS-Pass-9',
    title: 'Batch Collapse',
    description: 'Use ⚳⃰ for batch collapse over arrays',
    hlx_example: `⊢ handles = ⚳⃰ node nodes;`,
    expected_hlxl: `let handles = latent batch node nodes;`
  },
  {
    id: 'hlx-ls-10',
    pass: 'HLX-LS-Pass-10',
    title: 'Batch Resolve',
    description: 'Use ⚯⃰ for batch resolve over handle arrays',
    hlx_example: `⊢ values = ⚯⃰ handles;`,
    expected_hlxl: `let values = latent resolve batch handles;`
  },
  
  // === HLX-LS Tasks (Passes 11-15) ===
  {
    id: 'hlx-ls-11',
    pass: 'HLX-LS-Pass-11',
    title: 'Conditional Collapse',
    description: 'Use ⚳? for conditional collapse',
    hlx_example: `⊢ h = ⚳?(should_cache) node ast;`,
    expected_hlxl: `let h = ls.collapse_if(should_cache) node ast;`
  },
  {
    id: 'hlx-ls-12',
    pass: 'HLX-LS-Pass-12',
    title: 'Resolve with Fallback',
    description: 'Use ⚯‖ for resolve-or-default',
    hlx_example: `⊢ v = ⚯‖ maybe_handle {14:{@0:0}};
⊢ safe = ⚯‖ cached_ast empty_node;`,
    expected_hlxl: `let v = ls.resolve_or maybe_handle {14:{@0:0}};
let safe = ls.resolve_or cached_ast empty_node;`
  },
  {
    id: 'hlx-ls-13',
    pass: 'HLX-LS-Pass-13',
    title: 'Transactions',
    description: 'Use ⚿ for atomic LS transaction blocks',
    hlx_example: `⚿ {
  ⊢ h1 = ⚳ node ast1;
  ⊢ h2 = ⚳ node ast2;
  ⚐ h1 != h2;
  ↩ [h1, h2];
}`,
    expected_hlxl: `ls.transaction {
  let h1 = ls.collapse node ast1;
  let h2 = ls.collapse node ast2;
  latent guard h1 != h2;
  return [h1, h2];
}`
  },
  {
    id: 'hlx-ls-14',
    pass: 'HLX-LS-Pass-14',
    title: 'Fingerprint & Validate',
    description: 'Use ⚉ (fingerprint) and ⚇ (validate)',
    hlx_example: `⊢ fp = ⚉ cached_handle;
⊢ ok = ⚇ maybe_stale;
❓(!⚇ h) {
  ⊢ h = ⚳ node fresh_data;
}`,
    expected_hlxl: `let fp = ls.fingerprint cached_handle;
let ok = ls.validate maybe_stale;
if(!ls.validate h) {
  let h = ls.collapse node fresh_data;
}`
  },
  {
    id: 'hlx-ls-15',
    pass: 'HLX-LS-Pass-15',
    title: 'Table Operations',
    description: 'Use ⌸⑂ (fork), ⌸Δ (diff), ⌸⊕ (merge)',
    hlx_example: `ꙮ ⌸ main_table;
⌸⑂ scratch from main_table;
⊢ changes = ⌸Δ scratch main_table;
⌸⊕ scratch into main_table;`,
    expected_hlxl: `latent table main_table;
ls.table_fork scratch from main_table;
let changes = ls.table_diff scratch main_table;
ls.table_merge scratch into main_table;`
  },
];

// -----------------------------------------------------------------------------
// GLYPH REFERENCE PANEL
// -----------------------------------------------------------------------------
interface GlyphCategory {
  name: string;
  glyphs: { glyph: string; hlxl: string; desc: string }[];
}

const GLYPH_REFERENCE: GlyphCategory[] = [
  {
    name: 'Structure',
    glyphs: [
      { glyph: '⟠', hlxl: 'program', desc: 'Program declaration' },
      { glyph: '◇', hlxl: 'block', desc: 'Block declaration' },
      { glyph: '⊢', hlxl: 'let', desc: 'State variable' },
      { glyph: '⊡', hlxl: 'local', desc: 'Frame-local variable' },
      { glyph: '↩', hlxl: 'return', desc: 'Return statement' },
    ]
  },
  {
    name: 'Control Flow',
    glyphs: [
      { glyph: '❓', hlxl: 'if', desc: 'Conditional' },
      { glyph: '❗', hlxl: 'else', desc: 'Else branch' },
      { glyph: '⟳', hlxl: 'while', desc: 'While loop' },
      { glyph: '⟲', hlxl: 'for', desc: 'For-each loop' },
    ]
  },
  {
    name: 'Latent Space',
    glyphs: [
      { glyph: 'ꙮ', hlxl: 'latent', desc: 'Latent keyword' },
      { glyph: '⌸', hlxl: 'table', desc: 'Table declaration' },
      { glyph: '▣', hlxl: 'using', desc: 'Default table binding' },
      { glyph: '⚳', hlxl: 'ls.collapse', desc: 'Collapse to handle' },
      { glyph: '⚯', hlxl: 'ls.resolve', desc: 'Resolve handle' },
      { glyph: '⚶', hlxl: 'ls.snapshot', desc: 'Snapshot table' },
    ]
  },
  {
    name: 'LS Sugar',
    glyphs: [
      { glyph: '⚷', hlxl: 'latent X =', desc: 'Collapse-and-bind' },
      { glyph: '⚵', hlxl: 'latent value X =', desc: 'Resolve-and-bind' },
      { glyph: '⚻', hlxl: 'latent snapshot', desc: 'Snapshot-and-bind' },
      { glyph: '▷', hlxl: '|>', desc: 'Pipeline operator' },
      { glyph: '⚑', hlxl: 'latent match', desc: 'Pattern match' },
      { glyph: '⚐', hlxl: 'latent guard', desc: 'Guard assertion' },
    ]
  },
  {
    name: 'Batch Ops',
    glyphs: [
      { glyph: '⚳⃰', hlxl: 'latent batch', desc: 'Batch collapse' },
      { glyph: '⚯⃰', hlxl: 'latent resolve batch', desc: 'Batch resolve' },
    ]
  },
  {
    name: 'Advanced LS',
    glyphs: [
      { glyph: '⚳?', hlxl: 'ls.collapse_if', desc: 'Conditional collapse' },
      { glyph: '⚯‖', hlxl: 'ls.resolve_or', desc: 'Resolve with fallback' },
      { glyph: '⚿', hlxl: 'ls.transaction', desc: 'Atomic transaction' },
      { glyph: '⚉', hlxl: 'ls.fingerprint', desc: 'Get fingerprint' },
      { glyph: '⚇', hlxl: 'ls.validate', desc: 'Validate handle' },
    ]
  },
  {
    name: 'Table Ops',
    glyphs: [
      { glyph: '⌸⑂', hlxl: 'ls.table_fork', desc: 'Fork table' },
      { glyph: '⌸Δ', hlxl: 'ls.table_diff', desc: 'Diff tables' },
      { glyph: '⌸⊕', hlxl: 'ls.table_merge', desc: 'Merge tables' },
    ]
  },
];

// -----------------------------------------------------------------------------
// MAIN COMPONENT
// -----------------------------------------------------------------------------
export default function HLXPlayground() {
  const [hlxSource, setHlxSource] = useState<string>(HLX_TASKS[0].hlx_example);
  const [activeTask, setActiveTask] = useState<string>(HLX_TASKS[0].id);
  const [showReference, setShowReference] = useState<boolean>(true);
  
  // Transliterate HLX → HLXL
  const hlxlSource = useMemo(() => transliterateHLXtoHLXL(hlxSource), [hlxSource]);
  
  // Round-trip verification
  const roundTrip = useMemo(() => transliterateHLXLtoHLX(hlxlSource), [hlxlSource]);
  const isRoundTripValid = roundTrip.trim() === hlxSource.trim();
  
  // Find current task
  const currentTask = HLX_TASKS.find(t => t.id === activeTask);
  const isCorrect = currentTask && hlxlSource.trim() === currentTask.expected_hlxl.trim();

  return (
    <div className="hlx-playground" style={{ display: 'flex', gap: '1rem', padding: '1rem' }}>
      {/* Left Panel: Editor */}
      <div style={{ flex: 2, display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <h2>HLX Playground - Runic Surface Language</h2>
        
        {/* Task Selector */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
          {HLX_TASKS.map(task => (
            <button
              key={task.id}
              onClick={() => {
                setActiveTask(task.id);
                setHlxSource(task.hlx_example);
              }}
              style={{
                padding: '0.25rem 0.5rem',
                fontSize: '0.75rem',
                background: activeTask === task.id ? '#4a9eff' : '#2a2a2a',
                color: '#fff',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
              }}
            >
              {task.pass}
            </button>
          ))}
        </div>
        
        {/* Task Description */}
        {currentTask && (
          <div style={{ background: '#1a1a2e', padding: '0.75rem', borderRadius: '4px' }}>
            <strong>{currentTask.title}</strong>
            <p style={{ margin: '0.5rem 0 0', opacity: 0.8 }}>{currentTask.description}</p>
          </div>
        )}
        
        {/* HLX Source Editor */}
        <div>
          <label style={{ display: 'block', marginBottom: '0.25rem' }}>
            HLX Source (Glyph)
          </label>
          <textarea
            value={hlxSource}
            onChange={e => setHlxSource(e.target.value)}
            style={{
              width: '100%',
              minHeight: '200px',
              fontFamily: 'monospace',
              fontSize: '14px',
              background: '#0a0a0a',
              color: '#e0e0e0',
              border: '1px solid #333',
              borderRadius: '4px',
              padding: '0.5rem',
              whiteSpace: 'pre-wrap',
              wordBreak: 'break-word',
            }}
            spellCheck={false}
          />
        </div>
        
        {/* Pipeline Visualization */}
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '0.5rem',
          padding: '0.5rem',
          background: '#1a1a1a',
          borderRadius: '4px'
        }}>
          <span style={{ 
            background: '#4a9eff', 
            padding: '0.25rem 0.5rem', 
            borderRadius: '4px' 
          }}>HLX</span>
          <span>→</span>
          <span style={{ opacity: 0.7 }}>transliterate</span>
          <span>→</span>
          <span style={{ 
            background: '#9e4aff', 
            padding: '0.25rem 0.5rem', 
            borderRadius: '4px' 
          }}>HLXL</span>
          <span>→</span>
          <span style={{ opacity: 0.7 }}>compile</span>
          <span>→</span>
          <span style={{ 
            background: '#ff4a9e', 
            padding: '0.25rem 0.5rem', 
            borderRadius: '4px' 
          }}>Core</span>
        </div>
        
        {/* HLXL Output */}
        <div>
          <label style={{ display: 'block', marginBottom: '0.25rem' }}>
            HLXL Output (ASCII)
            {isCorrect && <span style={{ color: '#4aff4a', marginLeft: '0.5rem' }}>✓ Correct</span>}
          </label>
          <pre style={{
            background: '#0a0a0a',
            border: '1px solid #333',
            borderRadius: '4px',
            padding: '0.5rem',
            margin: 0,
            overflow: 'auto',
            maxHeight: '200px',
            whiteSpace: 'pre-wrap',
            wordBreak: 'break-word',
          }}>
            {hlxlSource}
          </pre>
        </div>
        
        {/* Round-trip Status */}
        <div style={{
          padding: '0.5rem',
          background: isRoundTripValid ? '#1a2e1a' : '#2e1a1a',
          borderRadius: '4px',
          fontSize: '0.85rem',
        }}>
          Round-trip: {isRoundTripValid ? '✓ Bijective' : '⚠ Mismatch'}
        </div>
      </div>
      
      {/* Right Panel: Glyph Reference */}
      {showReference && (
        <div style={{ 
          flex: 1, 
          background: '#0a0a0a', 
          borderRadius: '4px', 
          padding: '1rem',
          maxHeight: '80vh',
          overflow: 'auto'
        }}>
          <h3 style={{ marginTop: 0 }}>Glyph Reference</h3>
          {GLYPH_REFERENCE.map(category => (
            <div key={category.name} style={{ marginBottom: '1rem' }}>
              <h4 style={{ 
                margin: '0 0 0.5rem', 
                color: '#4a9eff',
                fontSize: '0.9rem'
              }}>
                {category.name}
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                {category.glyphs.map(g => (
                  <div 
                    key={g.glyph}
                    onClick={() => setHlxSource(prev => prev + g.glyph)}
                    style={{
                      display: 'grid',
                      gridTemplateColumns: '2rem 1fr 1fr',
                      gap: '0.5rem',
                      padding: '0.25rem',
                      fontSize: '0.8rem',
                      cursor: 'pointer',
                      borderRadius: '2px',
                    }}
                    className="glyph-row"
                  >
                    <span style={{ fontWeight: 'bold', fontSize: '1.1rem' }}>{g.glyph}</span>
                    <code style={{ opacity: 0.7 }}>{g.hlxl}</code>
                    <span style={{ opacity: 0.5 }}>{g.desc}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
      
      {/* Toggle Reference Button */}
      <button
        onClick={() => setShowReference(!showReference)}
        style={{
          position: 'fixed',
          bottom: '1rem',
          right: '1rem',
          padding: '0.5rem 1rem',
          background: '#333',
          color: '#fff',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
        }}
      >
        {showReference ? 'Hide' : 'Show'} Glyphs
      </button>
      
      <style>{`
        .glyph-row:hover {
          background: #1a1a2e;
        }
      `}</style>
    </div>
  );
}
