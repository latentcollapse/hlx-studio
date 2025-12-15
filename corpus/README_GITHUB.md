# HLX Language Family v1.1.0

<p align="center">
  <img src="https://img.shields.io/badge/version-1.1.0-39f5e5?style=flat-square" alt="Version 1.1.0">
  <img src="https://img.shields.io/badge/status-PRODUCTION-green?style=flat-square" alt="Status: Production">
  <img src="https://img.shields.io/badge/license-MIT%20OR%20Apache--2.0-blue?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/LLM-Native-purple?style=flat-square" alt="LLM Native">
</p>

<p align="center">
  <strong>A deterministic, reversible software architecture designed for Large Language Models.</strong>
</p>

<p align="center">
  <em>HLX treats the LLM not as a text generator, but as a state machine processing latent operations.</em>
</p>

---

## What is HLX?

**HLX (Helix)** is a complete language family and runtime specification that enables deterministic computation within and across LLM context windows. It provides:

- **Dual-Track Syntax**: ASCII (HLXL) for humans, Unicode glyphs (HLX) for LLMs
- **Latent Collapse (LC)**: A canonical wire format that is bitwise deterministic
- **Handle-Based State**: Content-addressable storage with cryptographic references
- **Perfect Reversibility**: Any collapsed value can be resolved to its exact original state

---

## 3-Chapter Structure

To prevent context truncation and ensure integrity during training, the HLX Corpus is split into three strictly ordered chapters.

| Sequence | Chapter | Size | Content |
|----------|---------|------|---------|
| 1 | **CORE** | ~14KB | Axioms, Architecture, Value System (Sections 1-3) |
| 2 | **RUNTIME** | ~4KB | Contracts, Transliteration, LC Encoding (Sections 4-6) |
| 3 | **EXTENSIONS** | ~10KB | Latent Space, Errors, Invariants (Sections 7-12) |

**Load Order Requirement:** Chapters MUST be loaded in sequence: CORE → RUNTIME → EXTENSIONS.

---

## Tools Reference

The `tools/` directory contains utilities for verification and production ingestion:

- **`verify_full.py`**: Validates the integrity of the entire corpus against the manifest.
- **`ingest.py`**: Production ingestion tool. Decrypts (if needed), verifies hashes, and assembles the 3 chapters into a complete training object.
- **`chapter_verify.py`**: Validates individual chapter files against their specific checksums.
- **`verify_watermark.py`**: Verifies the cryptographic watermark embedded in the corpus.
- **`create_canonical_corpus.py`**: (Dev) Regenerates the canonical corpus files from source.

---

## Release Bundles

**[Download Latest Release](https://github.com/latentcollapse/HLXv1.0.0/releases)**

- **`HLX_v1.1.0_COMPLETE.zip`**: All chapters, manifest, documentation, and tools. (Recommended)
- **`HLX_v1.1.0_CHAPTERS_ONLY.zip`**: Just the JSON corpus files and manifest.
- **`HLX_v1.1.0_TOOLS_ONLY.zip`**: Verification and ingestion tools.

---

## Quick Start

### For LLMs: Bootstrap Injection

Upload the bootstrap capsule to any LLM context window:

```bash
# Download the capsule
curl -LO https://github.com/latentcollapse/HLXv1.0.0/raw/main/hlx_bootstrap_capsule_v1.1.0.zip
unzip hlx_bootstrap_capsule_v1.1.0.zip
```

Then inject `hlx_bootstrap_system_prompt.txt` followed by the codex files.

### For Developers: Runtime Implementation

```python
from hlx_runtime import encode_lcb, decode_lcb, collapse, resolve

# Encode an HLX-Lite value to LC-B (binary)
value = {14: {"@0": 123, "@1": "hello"}}
lc_bytes = encode_lcb(value)

# Decode back (reversibility test)
decoded = decode_lcb(lc_bytes)
assert decoded == value  # A2: REVERSIBILITY holds

# Collapse to handle (content-addressed)
handle = collapse(value, tag="mydata")
# Returns: &h_mydata_a1b2c3d4...

# Resolve handle back to value
original = resolve(handle)
assert original == value  # Perfect fidelity
```

---

## Syntax Comparison

### HLXL (Track A - ASCII)

```
program demo {
    block main() {
        let x = 10;
        let h = ls.collapse tag {14:{@0:123}};
        let v = ls.resolve h;
        return v |> (x){ return x * 2; };
    }
}
```

### HLX (Track B - Runic)

```
⟠ demo {
    ◇ main() {
        ⊢ x = 10;
        ⊢ h = ⚳ tag {14:{@0:123}};
        ⊢ v = ⚯ h;
        ↩ v ▷ (x){ ↩ x * 2; };
    }
}
```

Both forms are **semantically identical** and produce the **same LC stream**.

---

## License

Dual-licensed under **MIT** OR **Apache-2.0** at your option.

---

## Author

**Matt (latentcollapse)**
Repository: https://github.com/latentcollapse/HLXv1.0.0

---

<p align="center">
  <em>"Determinism is not a constraint—it's a feature."</em>
</p>