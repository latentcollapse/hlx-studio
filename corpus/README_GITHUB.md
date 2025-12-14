# HLX Language Family v1.0.0

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-39f5e5?style=flat-square" alt="Version 1.0.0">
  <img src="https://img.shields.io/badge/status-FROZEN-green?style=flat-square" alt="Status: Frozen">
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

### The Four Axioms

| Axiom | Name | Rule |
|-------|------|------|
| **A1** | DETERMINISM | Same input MUST produce same LC stream |
| **A2** | REVERSIBILITY | `collapse(v)` → `resolve(h)` = `v` exactly |
| **A3** | BIJECTION | Track A (ASCII) ↔ Track B (Runic) maps 1:1 |
| **A4** | UNIVERSAL_VALUE | All tracks lower to HLX-Lite before encoding |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    HLX LANGUAGE FAMILY                       │
├─────────────────────────────┬───────────────────────────────┤
│      TRACK A: HLXL          │       TRACK B: HLX            │
│      (Engineering)          │       (LLM Native)            │
│      ASCII Text             │       Unicode Glyphs          │
├─────────────────────────────┴───────────────────────────────┤
│                   ↓ Lower to CoreExpr ↓                     │
├─────────────────────────────────────────────────────────────┤
│                    HLX-LITE VALUE SYSTEM                    │
│                    (Contracts 1-5)                          │
├─────────────────────────────────────────────────────────────┤
│                   ↓ Encode to Wire ↓                        │
├─────────────────────────────────────────────────────────────┤
│                    LC (LATENT COLLAPSE)                     │
│           LC-B (Binary) ←→ LC-T (Text/Glyph)               │
│                    CANONICAL WIRE FORMAT                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### For LLMs: Bootstrap Injection

Upload the bootstrap capsule to any LLM context window:

```bash
# Download the capsule
curl -LO https://github.com/latentcollapse/HLXv1.0.0/raw/main/hlx_bootstrap_capsule_v1.0.0.zip
unzip hlx_bootstrap_capsule_v1.0.0.zip
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

## Glyph Reference

### Structure
| Glyph | ASCII | Meaning |
|-------|-------|---------|
| `⟠` | `program` | Program declaration |
| `◇` | `block` | Block/function declaration |
| `⊢` | `let` | Variable binding |
| `⊡` | `local` | Frame-local binding |
| `↩` | `return` | Return statement |

### Control Flow
| Glyph | ASCII | Meaning |
|-------|-------|---------|
| `❓` | `if` | Conditional |
| `❗` | `else` | Else branch |
| `⟳` | `while` | While loop |
| `⟲` | `for` | For loop |

### Latent Operations
| Glyph | ASCII | Meaning |
|-------|-------|---------|
| `⚳` | `ls.collapse` | Collapse value to handle |
| `⚯` | `ls.resolve` | Resolve handle to value |
| `⚶` | `ls.snapshot` | Capture runtime state |
| `⚿` | `ls.transaction` | Atomic transaction block |
| `⟁` | `&h_` | Handle reference prefix |

### LC Markers (Wire Format)
| Glyph | Meaning | LC-B Tag |
|-------|---------|----------|
| `🜊` | Object start | `0x07` |
| `🜁` | Field marker | (inline) |
| `🜂` | Object end | `0x08` |
| `🜃` | Array start | `0x05` |
| `🜄` | Array end | `0x06` |
| `🜇` | Handle reference | `0x09` |
| `🜋` | Stream end | (terminal) |

---

## Value System (HLX-Lite)

HLX uses a typed value system with 8 primitive types:

| Type | ID | LC-B Tag | Encoding |
|------|-----|----------|----------|
| NULL | 0 | `0x00` | No payload |
| BOOL | 1 | `0x0A`/`0x0B` | TRUE/FALSE |
| INT | 2 | `0x01` | Signed LEB128 |
| FLOAT | 3 | `0x02` | IEEE 754 BE |
| TEXT | 4 | `0x03` | LEB128 len + UTF-8 |
| BYTES | 5 | `0x04` | LEB128 len + raw |
| ARRAY | 6 | `0x05`/`0x06` | START/END markers |
| OBJECT | 7 | `0x07`/`0x08` | Contract ID + sorted fields |

### Field Notation

Objects use `@N` notation for zero-based field indices:

```json
{14: {"@0": 123, "@1": "hello", "@2": true}}
```

**Rule**: Fields MUST be encoded in ascending index order (`@0` < `@1` < `@2`).

---

## Contract Registry

Contracts define typed object schemas:

### Core Contracts (1-5)
| ID | Name | Purpose |
|----|------|---------|
| 1 | HLXLiteValue | Root value wrapper |
| 2 | HLXLiteField | Field descriptor |
| 3 | HLXLiteObject | Typed object |
| 4 | HLXLiteDocument | Top-level document |
| 5 | ProvenanceLite | Document metadata |

### Latent Contracts (800+)
| ID | Name | Purpose |
|----|------|---------|
| 800 | LatentHandle | Handle reference |
| 801 | LatentTable | Handle storage |
| 820 | LSOp | LS operation instruction |

### Core Execution (830+)
| ID | Name | Purpose |
|----|------|---------|
| 830 | CoreProgram | Compiled program |
| 832 | CoreState | Execution state |
| 834 | CoreExpr | AST expression |
| 836 | EngineSnapshot | Full runtime snapshot |

---

## LC Encoding Rules

### LC-B (Binary - Canonical)

1. **Integers**: Signed LEB128
2. **Floats**: IEEE 754 Double, Big-Endian
3. **Text**: LEB128 length prefix + UTF-8 bytes
4. **Objects**: Contract ID (LEB128) + fields sorted by index
5. **Arrays**: `0x05` + elements + `0x06`
6. **Handles**: `0x09` + LEB128 length + ASCII string

### Canonical Constraints

- No trailing data after stream end
- No duplicate field indices
- Fields MUST be in ascending order
- No NaN/Infinity floats (E_FLOAT_SPECIAL)
- MAX_DEPTH = 64, MAX_SIZE = 1MB

---

## Error Taxonomy

| Range | Category |
|-------|----------|
| 1000-1099 | Lexical Errors |
| 1100-1199 | Syntactic Errors |
| 1200-1299 | Type Errors |
| 1300-1399 | Constraint Errors |
| 1400-1499 | Semantic Errors |

Common errors: `E_LC_PARSE`, `E_FIELD_ORDER`, `E_DEPTH_EXCEEDED`, `E_HANDLE_NOT_FOUND`

---

## Formal Invariants

These MUST hold at all times:

```
INV-001: decode(encode(v)) == v           # Total Fidelity
INV-002: collapse(v) == collapse(v)       # Handle Idempotence
INV-003: fields[i] < fields[i+1]          # Field Order
INV-004: trans(trans(x, B), A) == x       # Bijection Hold
INV-005: encode(v, t1) == encode(v, t2)   # Time Independence
```

---

## Repository Contents

```
HLXv1.0.0/
├── README.md                           # This file
├── hlx_bootstrap_capsule_v1.0.0.zip    # Complete bootstrap package
└── hlx_bootstrap_capsule_v1.0.0/
    ├── hlx_bootstrap_system_prompt.txt # LLM system prompt
    ├── hlx_codex_v1.0.0.json           # Full specification
    ├── hlx_runtime_conformance.json    # Validation rules
    ├── hlx_mode_switches.json          # Mode configuration
    ├── hlx_rosetta_examples.json       # Cross-track examples
    └── hlx_transfer_envelope.json      # Wire format schema
```

---

## Versioning

- **Codex Version**: 1.0.0 (FROZEN)
- **LC-B Spec**: SD9 compliant
- **Evolution**: SpecDelta patches only (no breaking changes in v1.x)

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
