
import { HLXContract, HLXToken } from './types';
import { GLYPH_MAP } from './glyphs_clean';

// =============================================================================
// HLX UNIFIED CODEX v2.0.0 (ACTIVE)
// Pure Language Specification.
// =============================================================================

export const HLX_UNIFIED_CODEX = {
  "meta": {
    "codex_version": "2.0.0",
    "status": "ACTIVE",
    "generated_at": new Date().toISOString(),
    "hash": "0x2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d", 
    "legal": "Dual Licensed: MIT OR Apache-2.0"
  },
  "files": [
    {
      "filename": "00_overview.json",
      "content": {
        "title": "HLX Codex v2.0",
        "scope": "Complete Language Family & Runtime Semantics",
        "status": "ACTIVE_CORE",
        "components": [
          "HLXL (ASCII Surface)",
          "HLXL-LS (ASCII Latent)",
          "HLX (Runic Surface)",
          "HLX-LS (Runic Latent)",
          "LC (Latent Collapse)",
          "SpecDelta",
          "Runtime Semantics"
        ]
      }
    },
    {
      "filename": "01_glyph_map_full.json",
      "content": {
        "glyphs": GLYPH_MAP
      }
    },
    {
      "filename": "02_transliteration.json",
      "content": { "rule": "Bijective mapping between HLX (Runic) and HLXL (ASCII)." }
    },
    {
      "filename": "03_hlxl_grammar.json",
      "content": { 
        "description": "ASCII deterministic surface language.",
        "grammar_ref": "BG1-BG4, EG1-EG4" 
      }
    },
    {
      "filename": "04_hlx_grammar.json",
      "content": { "description": "Runic surface form." }
    },
    {
      "filename": "05_latent_space_full.json",
      "content": {
        "description": "Layer 4: Latent Space Architecture",
        "passes": [
          "LS0: Basic ops", "LS1: Table binding", "LS2: Subscript normalization", "LS3: Round-trip",
          "LS4: Pipeline", "LS5: Batch collapse", "LS6: Batch resolve", "LS7: Multi-table isolation",
          "LS8: Guard", "LS9: Match", "LS10: Transaction", "LS11: Validate", "LS12: Fingerprint",
          "LS13: Table fork", "LS14: Table merge", "LS15: Table diff", "LS16: Lazy handles",
          "LS17: Handle aliasing", "LS18: Scoped tables", "LS19: Reactive watchers", "LS20: Handle composition"
        ],
        "contracts": { "LatentHandle": 800, "LatentTable": 801, "LSOp": 820 },
        "status": "PROGRAM_COMPLETE"
      }
    },
    {
      "filename": "06_latent_collapse_full.json",
      "content": { 
        "passes": ["LC0", "LC1", "LC2", "LC3", "LC4", "LC5", "LC6", "LC7", "LC8", "LC9", "LC10", "LC11", "LC12"],
        "stream_format": {
          "description": "Positional field encoding - no colons, no @, just marker + index + value",
          "markers": {
            "\uD83D\uDF0A": "Begin object, followed by contract ID",
            "\uD83D\uDF02": "End object",
            "\uD83D\uDF01": "Field marker, followed by field index",
            "\uD83D\uDF03": "Begin array",
            "\uD83D\uDF04": "End array",
            "\uD83D\uDF07": "Inline handle reference, followed by handle ID",
            "\u27C1": "Handle literal",
            "\uD83D\uDF0B": "Document end"
          }
        }
      }
    },
    {
      "filename": "07_specdelta_full.json",
      "content": { 
        "history": [
          "DELTA_001_PROMOTION", 
          "DELTA_002_TUNING", 
          "DELTA_003_RUNTIME_SEMANTICS",
          "DELTA_004_V1_FREEZE",
          "DELTA_005_V2_ACTIVE"
        ],
        "passes": ["SD0", "SD1", "SD2", "SD3", "SD4", "SD5", "SD6", "SD7"]
      }
    },
    {
      "filename": "08_end_to_end_examples.json",
      "content": { 
        "examples": [
          {
            "name": "T0_Minimal",
            "hlx": "\u27E0 t { \u25C7 main() { \u22A2 x = 7; \u21A9 x; } }",
            "hlxl": "program t { block main() { let x = 7; return x; } }",
            "expected": 7
          },
          {
            "name": "T1_Pipeline",
            "hlx": "\u22A2 y = 3 \u25B7 (v){ \u21A9 v * 2; };",
            "hlxl": "let y = 3 |> (v){ return v * 2; };",
            "expected": 6
          },
          {
            "name": "T2_LS_Roundtrip",
            "hlx": "\u2338 tbl { } \u22A2 h = \u26B3 tag {14:{@0:123}}; \u22A2 v = \u26AF h;",
            "hlxl": "latent table tbl { } let h = ls.collapse tag {14:{@0:123}}; let v = ls.resolve h;",
            "invariant": "v == {14:{@0:123}}"
          },
          {
            "name": "T3_LC_Stream",
            "lc_input": "\uD83D\uDF0A14\uD83D\uDF010 123\uD83D\uDF02",
            "expanded": "{14:{@0:123}}",
            "invariant": "decode(encode(v)) == v"
          },
          {
            "name": "T4_Transaction",
            "hlx": "\u26BF { \u22A2 x = \u26B3 data; \u2690 x != null; \u21A9 x; }",
            "hlxl": "ls.transaction { let x = ls.collapse data; ls.guard x != null; return x; }",
            "behavior": "Atomic commit or full rollback"
          },
          {
            "name": "T5_Composition",
            "hlx": "\u22A2 doc = \u26B3\u2295 bundle [h1, h2, h3]; \u22A2 parts = \u26AF\u2296 doc;",
            "hlxl": "let doc = ls.compose bundle [h1, h2, h3]; let parts = ls.decompose doc;",
            "invariant": "parts == [h1, h2, h3]"
          }
        ]
      }
    },
    {
      "filename": "09_contracts_appendix.json",
      "content": { 
        "contracts": {
          "1:HLXLiteValue": { "fields": ["kind", "bool", "int", "float", "text", "bytes", "array", "object"] },
          "2:HLXLiteField": { "fields": ["index", "name", "value"] },
          "3:HLXLiteObject": { "fields": ["contract_id", "fields"] },
          "4:HLXLiteDocument": { "fields": ["root", "provenance"] },
          "5:ProvenanceLite": { "fields": ["profile", "created_at", "engine_id", "content_hash", "origin"] },
          "800:LatentHandle": { "fields": ["id", "tag", "fingerprint"] },
          "801:LatentTable": { "fields": ["table_id", "entries", "metadata"] },
          "820:LSOp": { "fields": ["op_code", "table", "handle", "value", "tag", "flags"] },
          "830:CoreProgram": { "fields": ["prog_id", "blocks"] },
          "831:CoreBlock": { "fields": ["block_id", "params", "body"] },
          "832:CoreState": { "fields": ["vars", "ls_refs", "stack"] },
          "834:CoreExpr": { "fields": ["kind", "payload", "meta"] },
          "836:EngineSnapshot": { "fields": ["prog_id", "state", "heap", "profile"] }
        }
      }
    },
    {
      "filename": "10_runtime_semantics.json",
      "content": {
        "title": "HLX Runtime Semantics v1.0",
        "description": "Formal definition of the execution model and CAS interactions.",
        "operations": {
          "collapse": "Serialize HLXLite -> Canonical JSON -> Hash -> Store. Returns Handle.",
          "resolve": "Lookup Handle -> Hash -> Retrieve HLXLite. Throw if missing.",
          "encode_lc": "Transform HLXLite -> LC Stream (\uD83D\uDF0AID\uD83D\uDF01Field...\uD83D\uDF02).",
          "decode_lc": "Parse LC Stream -> HLXLite.",
          "snapshot": "Capture all active handles and memory stats."
        },
        "invariants": [
          "TOTAL_FIDELITY: decode(encode(v)) == v",
          "IDEMPOTENCE: collapse(v) always returns same handle",
          "BIJECTION: 1:1 mapping between canonical value and hash"
        ],
        "error_model": {
          "E_UNKNOWN_HANDLE": "Handle not found in CAS.",
          "E_INVALID_LC": "Stream malformed or syntax error.",
          "E_CONTRACT_MISMATCH": "Decoded object does not match schema."
        }
      }
    },
    {
      "filename": "11_freeze_v1_declaration.json",
      "content": {
        "declaration": "HLX v1.0.0 FREEZE",
        "timestamp": new Date().toISOString(),
        "frozen_components": ["HLXL", "HLX", "HLXL-LS", "HLX-LS", "LC", "Runtime Semantics"],
        "rules": {
          "evolution": "SpecDelta Only",
          "invariants": "Must be preserved across v1.x"
        },
        "justification": "Ecosystem stability for tooling development. No semantic drift allowed."
      }
    },
    {
      "filename": "12_state_snapshot_v2.json",
      "content": {
        "snapshot_id": "v2-active",
        "integrity_hash": "sha256:f4a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1",
        "component_checksums": {
          "hlxl_grammar": "0xABC...",
          "runtime_core": "0xDEF...",
          "lc_opcodes": "0x123..."
        },
        "description": "Canonical snapshot of the active v2.0 state."
      }
    }
  ]
};

// Legacy Spec Structure for UI Components
export const HLX_SPEC_JSON = {
  components: {
    A_formal_canonical_specification: {
      description: "Formal definition of the HLX-Lite Foundation Layer.",
      canonical_test_vectors: {
        text_lite: `{4:{@0:null,@1:{5:{@0:"hlx-lite-2.0",@1:"2025-01-01T00:00:00Z",@2:"HLX-NEXUS",@4:"Native Generation"}}}}`
      },
      glyph_mapping: {
        mapping: GLYPH_MAP.structure
      },
      lite_contracts: {
        "HLXLiteValue": { id: 1 },
        "HLXLiteField": { id: 2 },
        "HLXLiteObject": { id: 3 },
        "HLXLiteDocument": { id: 4 },
        "ProvenanceLite": { id: 5 },
        "LatentHandle": { id: 800 },
        "LatentTable": { id: 801 },
        "LSOp": { id: 820 },
        "CoreProgram": { id: 830 },
        "CoreState": { id: 832 },
        "EngineSnapshot": { id: 836 }
      },
      binary_lite_spec: {
        opcodes: {
          "0x00": { name: "NULL", payload: "None" },
          "0x01": { name: "BOOL_TRUE", payload: "None" },
          "0x02": { name: "BOOL_FALSE", payload: "None" },
          "0x03": { name: "INT_8", payload: "1 byte" },
          "0x04": { name: "INT_32", payload: "4 bytes (LE)" },
          "0x07": { name: "TEXT_UTF8", payload: "VarInt Len + Bytes" }
        },
        canonical_binary_rules: [
          "All integers must be encoded in Little Endian.",
          "Strings must be UTF-8.",
          "Field sets must be sorted by index."
        ]
      },
      resource_limits: {
        "MAX_DEPTH": { value: "64", error: "E_DEPTH_EXCEEDED" },
        "MAX_OBJ_SIZE": { value: "1MB", error: "E_SIZE_EXCEEDED" }
      },
      canonical_principles: {
        "DETERMINISM": "Same input must produce bitwise identical output.",
        "BIJECTION": "Text and Binary forms must map 1:1."
      },
      canonical_format_rules: {
        whitespace: { rule: "No significant whitespace allowed outside strings." },
        integers: { rule: "No leading zeros allowed." },
        floats: { rule: "Must use scientific notation if abs(x) > 1e21." },
        bytes: { rule: "Lowercase hex only." },
        arrays: { rule: "No trailing commas." },
        objects: { rule: "Keys must be sorted." },
        error_model_ranges: {
           "1000-1099": "Lexical Errors",
           "1100-1199": "Syntactic Errors",
           "1300-1399": "Constraint Errors",
           "1400-1499": "Semantic Errors"
        }
      },
      invariants: {
        invariants: [
            { id: "INV-001", name: "Sort Order", rule: "Object keys sorted", description: "All keys must be sorted." }
        ]
      },
      error_taxonomy: {
        lexical_errors: [ { code: 1001, name: "E_INVALID_CHAR", desc: "Invalid character" } ],
        syntactic_errors: [ { code: 1101, name: "E_UNEXPECTED_TOKEN", desc: "Unexpected token" } ],
        constraint_errors: [ { code: 1301, name: "E_DEPTH", desc: "Max depth exceeded" } ],
        semantic_errors: [ { code: 1401, name: "E_TYPE", desc: "Type mismatch" } ]
      }
    },
    B_engineering_companion_manual: {}
  }
};

export const STUDIO_LAYER_MAP = {
  _hlx_unified_codex: {
    _meta: HLX_UNIFIED_CODEX.meta,
    layers: {
      "1_track_a_lite": {
        status: "ACTIVE", 
        version: "2.5",
        description: "TRACK A: HELIX LITE (Engineering)",
        contracts: {}
      },
      "2_track_b_runic": {
        status: "ACTIVE", 
        version: "2.0",
        description: "TRACK B: HELIX RUNIC (LLM Native)",
        contracts: {}
      },
      "3_lc_wire": {
        status: "FROZEN", 
        version: "1.0",
        description: "SHARED WIRE: LC (Latent Collapse)",
        contracts: { "820:LSOp": {} }
      },
      "4_hlx_core": {
        status: "ACTIVE", 
        version: "2.0",
        description: "KERNEL: Core Execution (AST)",
        contracts: { "830:CoreProgram": {}, "832:CoreState": {}, "836:EngineSnapshot": {} }
      },
      "5_runtime": {
        status: "PROGRAM_COMPLETE", 
        version: "2.0",
        description: "RUNTIME: HLX Engine & State",
        contracts: { "800:LatentHandle": { fields: {} }, "801:LatentTable": { fields: {} } }
      }
    }
  }
};

export const CONTRACT_DB: HLXContract[] = [
  { id: 1, name: 'HLXLiteValue', layer: '1_hlx_lite', fields: [] },
  { id: 4, name: 'HLXLiteDocument', layer: '1_hlx_lite', fields: [] },
  { id: 800, name: 'LatentHandle', layer: '4_hlx_ls', fields: [] },
  { id: 820, name: 'LSOp', layer: '4_hlx_ls', fields: [] },
  { id: 836, name: 'EngineSnapshot', layer: '2_hlx_core', fields: [] }
];
