
export const HLX_TERMINOLOGY_CANON = {
  "document": "HLX Terminology Canon",
  "version": "1.0.0",
  "authority": "NORMATIVE",
  "scope": "Terminology only. No semantics. No execution behavior.",
  "purpose": "Prevent terminology drift and misinterpretation across models, tools, and runtimes.",

  "global_rule": {
    "statement": "If a term is defined in this file, that definition is binding across all HLX artifacts.",
    "conflict_resolution": "This file overrides informal or implied usage elsewhere."
  },

  "layers": [
    {
      "name": "HLX",
      "type": "Surface Language (Runic)",
      "description": "Primary human-authored runic surface language.",
      "authority": "Human authoring only",
      "notes": "Bijective with HLXL. Not a transport encoding."
    },
    {
      "name": "HLXL",
      "type": "Surface Language (ASCII)",
      "description": "ASCII mirror of HLX for tool compatibility.",
      "authority": "Human and tooling",
      "notes": "Bijective with HLX. No semantic loss."
    },
    {
      "name": "LS",
      "type": "Latent Space",
      "description": "Runtime-resident latent tables, handles, and content-addressable state.",
      "authority": "Runtime only",
      "hard_lock": [
        "LS ALWAYS means Latent Space.",
        "LS is NOT a surface syntax.",
        "LS is NOT a lowered surface.",
        "LS is NOT a serialization format."
      ],
      "examples": [
        "ls.collapse",
        "ls.resolve",
        "ls.snapshot",
        "ls.transaction"
      ]
    },
    {
      "name": "LC-R",
      "type": "Latent Collapse — Runic",
      "description": "Human-visible runic representation of latent collapse streams.",
      "authority": "Display, pedagogy, debugging",
      "notes": [
        "Lossless mirror of LC-B.",
        "Not hashing-authoritative.",
        "Preserved for aesthetic and human inspection purposes."
      ]
    },
    {
      "name": "LC-B",
      "type": "Latent Collapse — Binary",
      "description": "Canonical binary encoding of latent collapse.",
      "authority": "Hashing and transport",
      "notes": [
        "Authoritative for integrity.",
        "Used by LC_12 envelopes.",
        "LC-R must lower to LC-B without loss."
      ]
    },
    {
      "name": "LC_12",
      "type": "Transfer Envelope",
      "description": "Chunking, Merkle hashing, and content-addressable transport layer.",
      "authority": "Provable 1:1 transfer",
      "notes": [
        "Wraps LC-B payloads.",
        "Provides exaflopic-scale integrity guarantees."
      ]
    }
  ],

  "explicit_non_meanings": [
    {
      "term": "LS",
      "invalid_meanings": [
        "Lowered Surface",
        "Low-level Syntax",
        "Linear Stream",
        "Language Stage"
      ]
    }
  ],

  "invariant": {
    "statement": "HLX may be beautiful. LC-R may be beautiful. LC-B must be correct.",
    "implication": "Aesthetic layers never override canonical transport authority."
  }
};
