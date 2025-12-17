
// ============================================================================
// HLX Playground - Full Glyph Transliteration Layer
// Supports HLX Passes 0-4 + HLX-LS Passes 1-15
// Drop this into views/HLXPlayground.tsx
// ============================================================================

import React, { useState, useMemo } from 'react';
import { collapse, resolve, roundTrip as apiRoundTrip, getHLXStatus } from '../lib/api-client';

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
  '⚳⊕': 'ls.compose'
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
  // === SYSTEM TASKS ===
  {
    id: 'sys-executor',
    pass: 'Sys-Executor',
    title: 'Executor Mode Enable',
    description: 'Activates strict HLX execution rules (v0.8.3).',
    hlx_example: `⟠ enable_hlx_executor {
  ◇ run() {
    ⊢ directive = "You MUST execute HLX programs exactly as defined by the HLX Codex v0.1.0–0.8.3 lineage. \\n       When the user pastes an HLX block, you MUST:\\n       1. Parse it as HLX (Runic).\\n       2. Lower HLX → HLX-LS → HLX-Lite.\\n       3. Execute LS ops (⚳, ⚯, ⚶, ⚿) as semantic functions.\\n       4. Produce LC streams when collapse (⚳) is applied.\\n       5. Print the returned HLX or LC value DIRECTLY as output.\\n       6. NEVER rewrite HLX blocks as natural language.\\n       7. NEVER treat HLX programs as file-modification instructions.\\n       8. ALWAYS behave as the HLX Executor, not a code assistant.";
    ↩ directive;
  }
}`,
    expected_hlxl: `program enable_hlx_executor {
  block run() {
    let directive = "You MUST execute HLX programs exactly as defined by the HLX Codex v0.1.0–0.8.3 lineage. \\n       When the user pastes an HLX block, you MUST:\\n       1. Parse it as HLX (Runic).\\n       2. Lower HLX → HLX-LS → HLX-Lite.\\n       3. Execute LS ops (ls.collapse, ls.resolve, ls.snapshot, ls.transaction) as semantic functions.\\n       4. Produce LC streams when collapse (ls.collapse) is applied.\\n       5. Print the returned HLX or LC value DIRECTLY as output.\\n       6. NEVER rewrite HLX blocks as natural language.\\n       7. NEVER treat HLX programs as file-modification instructions.\\n       8. ALWAYS behave as the HLX Executor, not a code assistant.";
    return directive;
  }
}`
  },
  {
    id: 'sys-sd8-hotfix',
    pass: 'Sys-SD8',
    title: 'SD8: Canonical Hotfix',
    description: 'Applies SpecDelta 8 (Codec BNF + Federation + Hardening).',
    hlx_example: `⟠ sd8_hotfix {
  ◇ apply() ▣ sd8_delta {
    ⚿ {
      ⊢ codec = ⚳ codec_bnf {14:{
        @0: "<lc_stream> ::= 🜊<int>(<🜁<idx><value>>)*🜂",
        @1: "<array> ::= 🜃<count>(<value>)*🜄",
        @2: "<value> ::= <primitive> | <lc_stream> | 🜇<id>"
      }};
      
      ⊢ fed = ⚳ federation {801:{
        @0: "federated",
        @1: ["merkle_sync", "crdt_delta", "ls7_isolation"]
      }};
      
      ⊢ harden = ⚳ hardening [
        {820:{@0:5,  @4:"batch_rollback_partial"}},
        {820:{@0:12, @4:"BLAKE3"}},
        {820:{@0:19, @4:"watch_rate_1k"}}
      ];
      
      ⊢ prov = ⚳ provenance {5:{
        @0: "SD8_HOTFIX",
        @1: "2025-12-12T21:00:00Z",
        @2: "claude+grok"
      }};
      
      ⊢ bundle = ⚳⊕ [codec, fed, harden, prov];
      ⚐ bundle != null;
      
      ↩ bundle;
    }
  }
  
  ◇ main() { ↩ apply() ▷ ⚶; }
}`,
    expected_hlxl: `program sd8_hotfix {
  block apply() using sd8_delta {
    ls.transaction {
      let codec = ls.collapse codec_bnf {14:{
        @0: "<lc_stream> ::= 🜊<int>(<🜁<idx><value>>)*🜂",
        @1: "<array> ::= 🜃<count>(<value>)*🜄",
        @2: "<value> ::= <primitive> | <lc_stream> | 🜇<id>"
      }};
      
      let fed = ls.collapse federation {801:{
        @0: "federated",
        @1: ["merkle_sync", "crdt_delta", "ls7_isolation"]
      }};
      
      let harden = ls.collapse hardening [
        {820:{@0:5,  @4:"batch_rollback_partial"}},
        {820:{@0:12, @4:"BLAKE3"}},
        {820:{@0:19, @4:"watch_rate_1k"}}
      ];
      
      let prov = ls.collapse provenance {5:{
        @0: "SD8_HOTFIX",
        @1: "2025-12-12T21:00:00Z",
        @2: "claude+grok"
      }};
      
      let bundle = ls.compose [codec, fed, harden, prov];
      latent guard bundle != null;
      
      return bundle;
    }
  }
  
  block main() { return apply() |> ls.snapshot; }
}`
  },
  {
    id: 'sys-sd9-synthesis',
    pass: 'Sys-SD9',
    title: 'SD9: Grok Synthesis',
    description: 'Applies SpecDelta 9 (Dual-Mode LC, BLAKE3, Field Policy).',
    hlx_example: `⟠ sd9_grok_synthesis {
  // ============================================================
  // SD9: SYNTHESIS OF GROK'S CRITIQUE
  // Author: The Clauditor
  // Reviewed-by: Grok (The Linus)
  // ============================================================
  
  ◇ main() ▣ sd9_table {
    
    // 1. LC DUAL-MODE (compromise)
    ⊢ lc_spec = ⚳ lc_modes {14:{
      @0: "LC-TEXT",
      @1: {
        markers: {
          OBJ_START: "🜊 (U+1F70A)",
          FIELD: "🜁 (U+1F701)",
          OBJ_END: "🜂 (U+1F702)",
          ARR_START: "🜃 (U+1F703)",
          ARR_END: "🜄 (U+1F704)",
          HANDLE_REF: "🜇 (U+1F707)",
          STREAM_END: "🜋 (U+1F70B)"
        },
        values: "Text representation (123, \\"hello\\")",
        audience: "LLMs, human debugging"
      },
      @2: "LC-BINARY",
      @3: {
        opcodes: {
          OBJ_START: "0x01",
          FIELD: "0x02",
          OBJ_END: "0x03",
          ARR_START: "0x04",
          ARR_END: "0x05",
          HANDLE_REF: "0x06",
          STREAM_END: "0x07"
        },
        values: "LEB128 ints, length-prefixed UTF-8 strings",
        audience: "Storage, transmission, native runtimes"
      },
      @4: "Lossless conversion between modes"
    }};
    
    // 2. BLAKE3 FINGERPRINTS (adopt)
    ⊢ hash_spec = ⚳ hashing {14:{
      @0: "BLAKE3",
      @1: "32-byte digest",
      @2: "Fingerprint = BLAKE3(canonical_lc_binary)",
      @3: "Handles carry truncated fingerprint (8 bytes) for verification"
    }};
    
    // 3. PRIMITIVE ENCODING (adopt)
    ⊢ encoding_spec = ⚳ primitives {14:{
      @0: "INT",
      @1: "LEB128 signed 64-bit",
      @2: "FLOAT", 
      @3: "IEEE 754 double, big-endian",
      @4: "TEXT",
      @5: "LEB128 length + UTF-8 bytes",
      @6: "BYTES",
      @7: "LEB128 length + raw bytes"
    }};
    
    // 4. TEST VECTORS (adopt - dual format)
    ⊢ test_vectors = ⚳ tests [
      {
        name: "T0_Int",
        input: 123,
        lc_text: "🜊2🜁0123🜂",
        lc_binary: "01 02 02 00 7B 03"
      },
      {
        name: "T1_String",
        input: "hello",
        lc_text: "🜊4🜁0\\"hello\\"🜂",
        lc_binary: "01 04 02 00 05 68 65 6C 6C 6F 03"
      },
      {
        name: "T2_Object",
        input: {14:{@0:1}},
        lc_text: "🜊14🜁01🜂",
        lc_binary: "01 0E 02 00 01 03"
      }
    ];
    
    // 5. GLYPH POLICY (reject prune, adopt deprecation)
    ⊢ glyph_policy = ⚳ glyphs {14:{
      @0: "POLICY",
      @1: "SD7 glyph set is CANONICAL",
      @2: "SD8 reductions are DEPRECATED pending migration",
      @3: "New glyphs via SpecDelta only",
      @4: "ASCII fallback: Every glyph has HLXL equivalent"
    }};
    
    // 6. FIELD NAMING (reject strings, keep positional)
    ⊢ field_policy = ⚳ fields {14:{
      @0: "POLICY",
      @1: "Wire format uses positional indices (@0, @1, @2)",
      @2: "Contract schemas define index → name mapping",
      @3: "Runtime resolves names at parse time",
      @4: "Rationale: Determinism, density, no name conflicts"
    }};
    
    // 7. TOKEN TABLES (adopt)
    ⊢ token_tables = ⚳ benchmarks {14:{
      @0: "Per-model token counts for equivalent HLX",
      @1: {
        grok: {glyph_avg: 1.0, lc_stream_avg: 4},
        claude: {glyph_avg: 1.0, lc_stream_avg: 5},
        gemini: {glyph_avg: 1.5, lc_stream_avg: 6},
        qwen: {glyph_avg: 1.0, lc_stream_avg: 4},
        gpt4: {glyph_avg: 1.0, lc_stream_avg: 5}
      },
      @2: "Methodology: cl100k_base tokenizer baseline"
    }};
    
    // BUNDLE SD9
    ⊢ sd9 = ⚳⊕ SD9_SYNTHESIS [
      lc_spec,
      hash_spec, 
      encoding_spec,
      test_vectors,
      glyph_policy,
      field_policy,
      token_tables
    ];
    
    ⚐ sd9 != null;
    
    ↩ sd9 ▷ ⚿ "SD9_CANONICAL" ▷ ⚶;
  }
}`,
    expected_hlxl: `program sd9_grok_synthesis {
  // ============================================================
  // SD9: SYNTHESIS OF GROK'S CRITIQUE
  // Author: The Clauditor
  // Reviewed-by: Grok (The Linus)
  // ============================================================
  
  block main() using sd9_table {
    
    // 1. LC DUAL-MODE (compromise)
    let lc_spec = ls.collapse lc_modes {14:{
      @0: "LC-TEXT",
      @1: {
        markers: {
          OBJ_START: "🜊 (U+1F70A)",
          FIELD: "🜁 (U+1F701)",
          OBJ_END: "🜂 (U+1F702)",
          ARR_START: "🜃 (U+1F703)",
          ARR_END: "🜄 (U+1F704)",
          HANDLE_REF: "🜇 (U+1F707)",
          STREAM_END: "🜋 (U+1F70B)"
        },
        values: "Text representation (123, \\"hello\\")",
        audience: "LLMs, human debugging"
      },
      @2: "LC-BINARY",
      @3: {
        opcodes: {
          OBJ_START: "0x01",
          FIELD: "0x02",
          OBJ_END: "0x03",
          ARR_START: "0x04",
          ARR_END: "0x05",
          HANDLE_REF: "0x06",
          STREAM_END: "0x07"
        },
        values: "LEB128 ints, length-prefixed UTF-8 strings",
        audience: "Storage, transmission, native runtimes"
      },
      @4: "Lossless conversion between modes"
    }};
    
    // 2. BLAKE3 FINGERPRINTS (adopt)
    let hash_spec = ls.collapse hashing {14:{
      @0: "BLAKE3",
      @1: "32-byte digest",
      @2: "Fingerprint = BLAKE3(canonical_lc_binary)",
      @3: "Handles carry truncated fingerprint (8 bytes) for verification"
    }};
    
    // 3. PRIMITIVE ENCODING (adopt)
    let encoding_spec = ls.collapse primitives {14:{
      @0: "INT",
      @1: "LEB128 signed 64-bit",
      @2: "FLOAT", 
      @3: "IEEE 754 double, big-endian",
      @4: "TEXT",
      @5: "LEB128 length + UTF-8 bytes",
      @6: "BYTES",
      @7: "LEB128 length + raw bytes"
    }};
    
    // 4. TEST VECTORS (adopt - dual format)
    let test_vectors = ls.collapse tests [
      {
        name: "T0_Int",
        input: 123,
        lc_text: "🜊2🜁0123🜂",
        lc_binary: "01 02 02 00 7B 03"
      },
      {
        name: "T1_String",
        input: "hello",
        lc_text: "🜊4🜁0\\"hello\\"🜂",
        lc_binary: "01 04 02 00 05 68 65 6C 6C 6F 03"
      },
      {
        name: "T2_Object",
        input: {14:{@0:1}},
        lc_text: "🜊14🜁01🜂",
        lc_binary: "01 0E 02 00 01 03"
      }
    ];
    
    // 5. GLYPH POLICY (reject prune, adopt deprecation)
    let glyph_policy = ls.collapse glyphs {14:{
      @0: "POLICY",
      @1: "SD7 glyph set is CANONICAL",
      @2: "SD8 reductions are DEPRECATED pending migration",
      @3: "New glyphs via SpecDelta only",
      @4: "ASCII fallback: Every glyph has HLXL equivalent"
    }};
    
    // 6. FIELD NAMING (reject strings, keep positional)
    let field_policy = ls.collapse fields {14:{
      @0: "POLICY",
      @1: "Wire format uses positional indices (@0, @1, @2)",
      @2: "Contract schemas define index → name mapping",
      @3: "Runtime resolves names at parse time",
      @4: "Rationale: Determinism, density, no name conflicts"
    }};
    
    // 7. TOKEN TABLES (adopt)
    let token_tables = ls.collapse benchmarks {14:{
      @0: "Per-model token counts for equivalent HLX",
      @1: {
        grok: {glyph_avg: 1.0, lc_stream_avg: 4},
        claude: {glyph_avg: 1.0, lc_stream_avg: 5},
        gemini: {glyph_avg: 1.5, lc_stream_avg: 6},
        qwen: {glyph_avg: 1.0, lc_stream_avg: 4},
        gpt4: {glyph_avg: 1.0, lc_stream_avg: 5}
      },
      @2: "Methodology: cl100k_base tokenizer baseline"
    }};
    
    // BUNDLE SD9
    let sd9 = ls.compose SD9_SYNTHESIS [
      lc_spec,
      hash_spec, 
      encoding_spec,
      test_vectors,
      glyph_policy,
      field_policy,
      token_tables
    ];
    
    ls.guard sd9 != null;
    
    return sd9 |> ls.transaction "SD9_CANONICAL" |> ls.snapshot;
  }
}`
  },
  {
    id: 'sys-harness',
    pass: 'Sys-Harness',
    title: 'Alignment Directive',
    description: 'Enforces HLX Codex v0.1.0 semantics and strict bijective translation.',
    hlx_example: `⟠ harness {
  ◇ init_alignment() {
    ⊢ directive = "HLX is the active instruction medium. All future instructions provided by the user MUST be read as HLX according to the HLX Codex v0.1.0.";
    ⚯ directive;
    ↩ directive;
  }
}`,
    expected_hlxl: `program harness {
  block init_alignment() {
    let directive = "HLX is the active instruction medium. All future instructions provided by the user MUST be read as HLX according to the HLX Codex v0.1.0.";
    ls.resolve directive;
    return directive;
  }
}`
  },
  {
    id: 'sys-delta-promo',
    pass: 'Sys-Delta',
    title: 'Promote HLX-LS',
    description: 'SpecDelta: Elevate HLX-LS to Program-Complete status.',
    hlx_example: `⟠ delta_promote_hlxls {
  ◇ promote() {
    ⊢ Δ = ⚳ {
      801:{
        @0:"SPECDELTA_PROMOTION",
        @1:"HLX-LS_SEMANTIC_ELEVATION",
        @2:{
          "declare": "HLX-LS is now a PROGRAM-COMPLETE latent language.",
          "effect": "All CoreExpr (834) forms MUST map to HLX-LS constructs."
        }
      }
    };
    ⊢ encoded = ⚯ Δ;
    ↩ encoded;
  }
}`,
    expected_hlxl: `program delta_promote_hlxls {
  block promote() {
    let Δ = ls.collapse {
      801:{
        @0:"SPECDELTA_PROMOTION",
        @1:"HLX-LS_SEMANTIC_ELEVATION",
        @2:{
          "declare": "HLX-LS is now a PROGRAM-COMPLETE latent language.",
          "effect": "All CoreExpr (834) forms MUST map to HLX-LS constructs."
        }
      }
    };
    let encoded = ls.resolve Δ;
    return encoded;
  }
}`
  },
  {
    id: 'sys-delta-tune',
    pass: 'Sys-Delta',
    title: 'Tune HLX-LS',
    description: 'SpecDelta: Tune HLX-LS canonical forms and normalization rules.',
    hlx_example: `⟠ delta_tune_hlxls {
  ◇ tune() {
    ⊢ Δ = ⚳ {
      801:{
        @0:"SPECDELTA_TUNING",
        @1:"HLX-LS_PROGRAM_TUNING",
        @2:{
          "codex_version": "0.8.2-ls-tuning",
          "canonical_forms": {
            "LITERAL": "ꙮ {hlx-lite-value}",
            "VAR_REF": "⊡ <name>",
            "SET_VAR": "⊢ <name> = <expr>;",
            "APPLY_INTRINSIC": "<intrinsic>(<args…>);",
            "LS_OP": "<ls-glyph> …;",
            "SEQ": "<stmt>; <stmt>; …",
            "IF": "❓(<cond>) { <then_block> } ❗ { <else_block> }"
          },
          "normalization_rules": [
            "N0: All HLX-LS programs MUST normalize to a sequence (SEQ) of canonical statements.",
            "N1: Redundant parentheses and whitespace MUST be removed in normalized form.",
            "N2: Implicit returns at end of block MUST be made explicit as VAR_REF or LITERAL.",
            "N3: Intrinsic calls MUST use APPLY_INTRINSIC form with explicit argument list.",
            "N4: All literals MUST be representable as HLX-Lite values in ꙮ {…} form.",
            "N5: Variable references MUST use ⊡ <name> in normalized representation.",
            "N6: Control-flow MUST use ❓ / ❗ glyphs for IF expressions; no alternate forms."
          ]
        }
      }
    };
    ⊢ encoded = ⚯ Δ;
    ↩ encoded;
  }
}`,
    expected_hlxl: `program delta_tune_hlxls {
  block tune() {
    let Δ = ls.collapse {
      801:{
        @0:"SPECDELTA_TUNING",
        @1:"HLX-LS_PROGRAM_TUNING",
        @2:{
          "codex_version": "0.8.2-ls-tuning",
          "canonical_forms": {
            "LITERAL": "latent {hlx-lite-value}",
            "VAR_REF": "local <name>",
            "SET_VAR": "let <name> = <expr>;",
            "APPLY_INTRINSIC": "<intrinsic>(<args…>);",
            "LS_OP": "<ls-glyph> …;",
            "SEQ": "<stmt>; <stmt>; …",
            "IF": "if(<cond>) { <then_block> } else { <else_block> }"
          },
          "normalization_rules": [
            "N0: All HLX-LS programs MUST normalize to a sequence (SEQ) of canonical statements.",
            "N1: Redundant parentheses and whitespace MUST be removed in normalized form.",
            "N2: Implicit returns at end of block MUST be made explicit as VAR_REF or LITERAL.",
            "N3: Intrinsic calls MUST use APPLY_INTRINSIC form with explicit argument list.",
            "N4: All literals MUST be representable as HLX-Lite values in latent {…} form.",
            "N5: Variable references MUST use local <name> in normalized representation.",
            "N6: Control-flow MUST use if / else glyphs for IF expressions; no alternate forms."
          ]
        }
      }
    };
    let encoded = ls.resolve Δ;
    return encoded;
  }
}`
  },
  {
    id: 'sys-delta-lc',
    pass: 'Sys-Delta',
    title: 'Tune LC',
    description: 'SpecDelta: Tune Latent Collapse (LC) grammar and capsule forms.',
    hlx_example: `⟠ delta_tune_lc {
  ◇ tune() {
    ⊢ Δ = ⚳ {
      801:{
        @0:"SPECDELTA_TUNING",
        @1:"LC_TUNING",
        @2:{
          "codex_version": "0.8.3-lc-tuning",
          "stream_grammar": {
            "LC_ATOM": "🜊<contract_id>🜁<field_index> <value_seq>🜂",
            "LC_POS_STREAM": "🜊<cid>🜁<slot> <v0> 🜇<slot1> <v1> … 🜂"
          },
          "collapse_pipeline": {
            "P0": "HLX-LS (canonical, normalized) MUST be the input to LC."
          }
        }
      }
    };
    ⊢ encoded = ⚯ Δ;
    ↩ encoded;
  }
}`,
    expected_hlxl: `program delta_tune_lc {
  block tune() {
    let Δ = ls.collapse {
      801:{
        @0:"SPECDELTA_TUNING",
        @1:"LC_TUNING",
        @2:{
          "codex_version": "0.8.3-lc-tuning",
          "stream_grammar": {
            "LC_ATOM": "🜊<contract_id>🜁<field_index> <value_seq>🜂",
            "LC_POS_STREAM": "🜊<cid>🜁<slot> <v0> 🜇<slot1> <v1> … 🜂"
          },
          "collapse_pipeline": {
            "P0": "HLX-LS (canonical, normalized) MUST be the input to LC."
          }
        }
      }
    };
    let encoded = ls.resolve Δ;
    return encoded;
  }
}`
  },
  {
    id: 'sys-exporter',
    pass: 'Sys-Exporter',
    title: 'Codex Exporter',
    description: 'Definition of the HLX Codex v0.1.0 export structure.',
    hlx_example: `⟠ hlx_codex_exporter_v0_1_0 {
  ◇ main() {
    ⊢ export_folder = "HLX_Codex_v0.1.0";
    ⊢ file_00 = { "filename": "00_overview.json", "lossless": true };
    // ... (full structure in ArchitectureMap.tsx)
    ↩ export_folder;
  }
}`,
    expected_hlxl: `program hlx_codex_exporter_v0_1_0 {
  block main() {
    let export_folder = "HLX_Codex_v0.1.0";
    let file_00 = { "filename": "00_overview.json", "lossless": true };
    // ... (full structure in ArchitectureMap.tsx)
    return export_folder;
  }
}`
  },
  {
    id: 'lc-test-basic',
    pass: 'LC-Test',
    title: 'LC Basic Validation v2',
    description: 'Fundamental collapse/resolve cycle verification with structured output.',
    hlx_example: `⟠ lc_test_basic_v2 {
  ◇ run() {
    ⊢ obj = {14:{@0:123}};
    ⊢ c   = ⚳ obj;
    ⊢ r   = ⚯ c;

    ⊢ out = {
      "lc_stream": c,
      "roundtrip": r
    };

    ↩ out;
  }
}`,
    expected_hlxl: `program lc_test_basic_v2 {
  block run() {
    let obj = {14:{@0:123}};
    let c   = ls.collapse obj;
    let r   = ls.resolve c;
    let out = {
      "lc_stream": c,
      "roundtrip": r
    };
    return out;
  }
}`
  },
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

  // Backend execution state
  const [testValue, setTestValue] = useState<string>('{"@0": 42}');
  const [executing, setExecuting] = useState<boolean>(false);
  const [executionResult, setExecutionResult] = useState<any>(null);
  const [executionError, setExecutionError] = useState<string | null>(null);
  const [backendStatus, setBackendStatus] = useState<string>('unknown');

  // Transliterate HLX → HLXL
  const hlxlSource = useMemo(() => transliterateHLXtoHLXL(hlxSource), [hlxSource]);

  // Round-trip verification
  const roundTrip = useMemo(() => transliterateHLXLtoHLX(hlxlSource), [hlxlSource]);
  const isRoundTripValid = roundTrip.trim() === hlxSource.trim();

  // Find current task
  const currentTask = HLX_TASKS.find(t => t.id === activeTask);
  const isCorrect = currentTask && hlxlSource.trim() === currentTask.expected_hlxl.trim();

  // Check backend status on mount
  React.useEffect(() => {
    getHLXStatus()
      .then(status => setBackendStatus(status.hlx_available ? 'connected' : 'unavailable'))
      .catch(() => setBackendStatus('offline'));
  }, []);

  const executeCollapse = async () => {
    setExecuting(true);
    setExecutionError(null);
    try {
      const value = JSON.parse(testValue);
      const result = await collapse(value, false);
      setExecutionResult({ type: 'collapse', ...result });
    } catch (error) {
      setExecutionError(error instanceof Error ? error.message : String(error));
    } finally {
      setExecuting(false);
    }
  };

  const executeRoundTrip = async () => {
    setExecuting(true);
    setExecutionError(null);
    try {
      const value = JSON.parse(testValue);
      const result = await apiRoundTrip(value);
      setExecutionResult({ type: 'round-trip', ...result });
    } catch (error) {
      setExecutionError(error instanceof Error ? error.message : String(error));
    } finally {
      setExecuting(false);
    }
  };

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
            borderRadius: '4px',
            fontWeight: 'bold'
          }}>HLX</span>
          <span>→</span>
          <span style={{ opacity: 0.7, fontSize: '0.8em' }}>transliterate</span>
          <span>→</span>
          <span style={{ 
            border: '1px dashed #555', 
            color: '#888',
            padding: '0.25rem 0.5rem', 
            borderRadius: '4px' 
          }}>HLXL</span>
          <span>→</span>
          <span style={{ opacity: 0.7, fontSize: '0.8em' }}>lower</span>
          <span>→</span>
          <span style={{ 
            background: '#d946ef', // Fuchsia-500
            padding: '0.25rem 0.5rem', 
            borderRadius: '4px',
            fontWeight: 'bold'
          }}>HLX-LS</span>
          <span>→</span>
          <span style={{ opacity: 0.7, fontSize: '0.8em' }}>compile</span>
          <span>→</span>
          <span style={{ 
            background: '#22c55e', 
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

        {/* Backend Execution Panel */}
        <div style={{
          background: '#1a1a2e',
          border: '1px solid #333',
          borderRadius: '4px',
          padding: '1rem',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
            <h3 style={{ margin: 0, fontSize: '1rem' }}>Backend Execution</h3>
            <span style={{
              fontSize: '0.7rem',
              padding: '0.2rem 0.4rem',
              borderRadius: '3px',
              background: backendStatus === 'connected' ? '#1a2e1a' : backendStatus === 'offline' ? '#2e1a1a' : '#2e2e1a',
              color: backendStatus === 'connected' ? '#4aff4a' : backendStatus === 'offline' ? '#ff4a4a' : '#ffaa4a',
            }}>
              {backendStatus.toUpperCase()}
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <label style={{ fontSize: '0.85rem', opacity: 0.8 }}>Test Value (HLX-Lite JSON):</label>
            <textarea
              value={testValue}
              onChange={e => setTestValue(e.target.value)}
              style={{
                width: '100%',
                minHeight: '60px',
                fontFamily: 'monospace',
                fontSize: '13px',
                background: '#0a0a0a',
                color: '#e0e0e0',
                border: '1px solid #333',
                borderRadius: '4px',
                padding: '0.5rem',
              }}
              placeholder='{"@0": 42}'
            />

            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button
                onClick={executeCollapse}
                disabled={executing || backendStatus !== 'connected'}
                style={{
                  flex: 1,
                  padding: '0.5rem 1rem',
                  fontSize: '0.85rem',
                  background: executing || backendStatus !== 'connected' ? '#333' : '#4a9eff',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: executing || backendStatus !== 'connected' ? 'not-allowed' : 'pointer',
                  opacity: executing || backendStatus !== 'connected' ? 0.5 : 1,
                }}
              >
                {executing ? 'Executing...' : 'Collapse'}
              </button>

              <button
                onClick={executeRoundTrip}
                disabled={executing || backendStatus !== 'connected'}
                style={{
                  flex: 1,
                  padding: '0.5rem 1rem',
                  fontSize: '0.85rem',
                  background: executing || backendStatus !== 'connected' ? '#333' : '#22c55e',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: executing || backendStatus !== 'connected' ? 'not-allowed' : 'pointer',
                  opacity: executing || backendStatus !== 'connected' ? 0.5 : 1,
                }}
              >
                {executing ? 'Executing...' : 'Round-Trip Test'}
              </button>
            </div>

            {executionError && (
              <div style={{
                padding: '0.5rem',
                background: '#2e1a1a',
                border: '1px solid #ff4a4a',
                borderRadius: '4px',
                fontSize: '0.85rem',
                color: '#ff4a4a',
              }}>
                Error: {executionError}
              </div>
            )}

            {executionResult && (
              <div style={{
                padding: '0.5rem',
                background: '#0a0a0a',
                border: '1px solid #4aff4a',
                borderRadius: '4px',
                fontSize: '0.85rem',
              }}>
                <div style={{ fontWeight: 'bold', marginBottom: '0.5rem', color: '#4aff4a' }}>
                  Result ({executionResult.type}):
                </div>
                <pre style={{
                  margin: 0,
                  whiteSpace: 'pre-wrap',
                  wordBreak: 'break-all',
                  fontSize: '0.8rem',
                  color: '#e0e0e0',
                }}>
                  {JSON.stringify(executionResult, null, 2)}
                </pre>
              </div>
            )}
          </div>
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
