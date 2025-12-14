
# Helix Studio

> **The first LLM-native development environment.**

![Helix Studio Interface](/api/placeholder/800/450)

Helix Studio is a research-grade IDE and runtime designed to bridge the gap between Large Language Models and deterministic software execution. It implements the **HLX Language Family**, a unified pipeline that allows LLMs to write, execute, and debug code with zero ambiguity and perfect reversibility.

---

## ⚡ Features

*   **LLM-Native Runtime:** Built on the **HLX Engine**, which executes Runic (HLX) and Latent (HLX-LS) code directly.
*   **Reversible Computation:** Collapse complex data into Latent Handles (`⚳`) and resolve them back (`⚯`) without information loss.
*   **Modular Architecture:** Five specialized nodes:
    *   **HELIX:** Conversational Orchestrator.
    *   **HLX ENGINE:** The Core Runtime & Language Lab.
    *   **CRUCIBLE:** Multi-file Code Forge.
    *   **TTY1:** OS/Kernel Build Environment.
    *   **ARCHIVE:** Historical State & Artifact Storage.
*   **Unified Codex:** Driven by a rigorous, downloadable JSON specification (Codex v1.0.1).
*   **Dual License:** Fully open source under MIT or Apache-2.0.

## 🚀 Getting Started

### Prerequisites
*   Node.js 18+
*   npm or yarn

### Installation

```bash
git clone https://github.com/helix-project/helix-studio.git
cd helix-studio
npm install
```

### Running the Studio

```bash
npm start
```
Access the Studio at `http://localhost:3000`.

## 🖥️ The Interface

Helix Studio is divided into five core "Nodes" (Tabs):

### 1. HELIX (Orchestrator)
Talk to the system. The entry point for high-level intent.
![Helix CLI](/api/placeholder/600/200)

### 2. HLX ENGINE (Runtime)
The "metal". Watch code execution, inspect the LC stream, and verify invariants.
![HLX Engine](/api/placeholder/600/300)

### 3. CRUCIBLE (Code Forge)
Write and compile standard code (TypeScript, Python) alongside HLX.

### 4. TTY1 (OS Forge)
Build and simulate Linux-based operating systems (Helinux).

### 5. ARCHIVE (Memory)
Browse previous sessions and inspect latent snapshots.

## 🔮 The HLX Language

Helix utilizes a tiered language family described in detail in the [Whitepaper](docs/helix_whitepaper_v1.md).

*   **HLXL (ASCII):** Human-readable, strict surface syntax.
*   **HLX (Runic):** LLM-optimized glyph syntax (e.g., `⟠`, `◇`, `⚳`).
*   **LC (Latent Collapse):** Binary wire format for execution streams.

### HLX Terminology (Canonical)

**IMPORTANT:** LS = **Latent Space** ONLY. Never "Lowered Surface".
- **HLXL**: ASCII surface syntax (human/tooling readable)
- **HLX**: Runic surface syntax (LLM-optimized glyphs)
- **HLX-LS**: Latent Space operations in runic form
- **HLXL-LS**: Latent Space operations in ASCII form
- **LC-T**: LC Text form (pedagogical, uses markers like `🜊🜁🜂`)
- **LC-B**: LC Binary form (canonical for hashing/transport)

### HLX Patch Delivery

HLX v1.0.1 introduces a standardized patch delivery mechanism. See `patches/v1.0.1/` for details on the transport-only patch architecture.

## Bootstrap Invariants (Canonical)

- **empty_table_handle**: `&h_empty_0`
- Empty LC-B payload is allowed.
  - Rule: If `chunk_count == 0`, `payload_root` MUST be `BLAKE3('')` and `chunks` MUST be `[]`.
- Runtimes MUST treat `&h_empty_0` as the genesis table handle.

## Merkle Spec (Canonical)

```
leaf_hash(i) = BLAKE3(chunk_bytes_i)
internal_node_hash = BLAKE3(child_count_u8 || child_hash_0 || ... || child_hash_(fanout-1))
```

- `child_count_u8` is the number of REAL children (1..fanout)
- If node has fewer than fanout children, pad remaining child_hash slots with EXACTLY 32 bytes of `0x00`
- For single-leaf: `payload_root = BLAKE3(0x01 || leaf_hash || 15*(32-byte-zeros))`

**Note:** LLMs MUST NOT compute hashes. Use `COMPUTE_WITH_EXPORTER` placeholder. Exporter/tooling is authoritative for BLAKE3/SHA256.

## Density Profile (Optional, Display-Only)

- `hlx_density_profile.json` is OPTIONAL.
- Density transformations are reversible and MUST expand to canonical HLX/HLXL BEFORE:
  - (a) lowering
  - (b) LC-B encoding
  - (c) hashing / LC_12 envelope construction
- Density is NEVER authoritative for transport integrity.

## 📜 License

This project is dual-licensed under **MIT** OR **Apache-2.0**, at your option.
See the `legal/` directory for full license texts.

## 📚 Documentation

*   **[Whitepaper (v1.0)](docs/helix_whitepaper_v1.md)**
*   **Export Codex:** You can download the full JSON specification directly from the **HLX ENGINE** tab in the Studio.

---
*Built with the Void Theme.*