# HLX Canonical Teaching Corpus v1.1.0

**Open-source, cryptographically watermarked teaching materials for the HLX Language Family.**

---

## 📚 Corpus Contents

This repository contains **complete, immutable teaching materials** for learning and training LLMs on the HLX architecture:

| File | Size | Purpose |
|------|------|---------|
| `HLX_CANONICAL_CORPUS_v1.0.0.json` | 21KB | Complete corpus with BLAKE2b-256 watermark |
| `HLX_LLM_TRAINING_CORPUS_v1.0.0.md` | 720 lines | Exaflopic precision training guide (11 sections) |
| `HLX_RAW_CORPUS_v1.0.0.json` | 18KB | Raw corpus for direct LLM injection |
| `HLX_WATERMARK_v1.0.0.json` | 541B | Cryptographic proof of authorship & immutability |
| `README_GITHUB.md` | 10KB | Comprehensive documentation & quick-start guide |

---

## 🔐 Ownership & Integrity

**Watermark Signature**: `a7d6b60d4008efd9a897ca930f1e1841b25bbf1debe50bfb85c8be05b129b394`

**Content Hash**: `32f91dbdfe95d3b98429204c521522a6664042e321bcb8fb6c7912ce40becf4c`

**Author**: Matt (latentcollapse)

**License**: Apache-2.0

---

## 🚀 Quick Start

### For LLM Training
```bash
# Direct injection (no parsing needed)
cat corpus/HLX_RAW_CORPUS_v1.0.0.json | llm-prompt-engine
```

### For Developers
```bash
# Complete reference with verification
cat corpus/HLX_CANONICAL_CORPUS_v1.0.0.json | jq '..__watermark__'
```

### For Learning
Start with `corpus/README_GITHUB.md` for:
- Architecture overview
- Syntax comparison (ASCII vs Runic)
- Glyph reference tables
- Value system guide
- Contract registry
- LC encoding rules

---

## 📖 What is HLX?

**HLX (Helix)** is a deterministic, reversible software architecture designed for Large Language Models.

**Four Core Axioms**:
1. **DETERMINISM** - Same input always produces identical output
2. **REVERSIBILITY** - Values can be collapsed and resolved without loss
3. **BIJECTION** - ASCII (HLXL) ↔ Runic (HLX) map 1:1
4. **UNIVERSAL_VALUE** - All tracks lower to HLX-Lite

**Two Surface Languages**:
- **HLXL** (Track A): ASCII for humans and IDEs
- **HLX** (Track B): Unicode glyphs for LLM efficiency

**Universal Wire Format**:
- **LC-B**: Canonical binary (BLAKE3 hashable)
- **LC-T**: Pedagogical text/glyph format

---

## 🔗 Related Repositories

- **helix-studio**: Full IDE and development environment (TypeScript/React/Tauri)
  - https://github.com/latentcollapse/helix-studio

- **HLXv1.0.0**: Original bootstrap capsule (historical archive)
  - https://github.com/latentcollapse/HLXv1.0.0

---

## 📜 License

Dual-licensed under **MIT** OR **Apache-2.0** at your option.

See `LICENSE` for full text.

---

<p align="center">
  <em>"Determinism is not a constraint—it's a feature."</em>
</p>
