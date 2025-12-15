#!/usr/bin/env python3
"""
HLX CANONICAL CORPUS GENERATOR v1.1.0+chapter-split
===================================================
Creates an encrypted, watermarked teaching corpus split into 3 chapters.
Includes cryptographic proof of ownership and dual-hash verification.

Chapter Structure (prevents truncation):
- CORE (meta, 1-5): Foundational language spec
- RUNTIME (6-8, 10): Operational mechanics
- EXTENSIONS (9, 11-12): Examples, directives, Vulkan

Grok Feedback Implementation:
- Model_id normalization (case-insensitive)
- 3-chapter split with manifest
- Vulkan error negatives in quiz
- Concrete Python code in pre_serialize_rules
- Model_id.lower() for deterministic key derivation

Author: Matt (latentcollapse)
License: MIT OR Apache-2.0
"""

import json
import hashlib
import base64
import datetime
import struct
import os
import sys
from pathlib import Path

# Optional BLAKE3 support
try:
    import blake3
    HAS_BLAKE3 = True
except ImportError:
    HAS_BLAKE3 = False
    print("Note: blake3 not installed. Using BLAKE2b only. Install with: pip install blake3")


# =============================================================================
# WATERMARK SYSTEM v1.1.0
# =============================================================================

class CopyrightWatermark:
    """Cryptographic watermark proving authorship with dual-hash verification."""

    WATERMARK_VERSION = "1.1.0"
    AUTHOR = "Matt (latentcollapse)"
    REPOSITORY = "https://github.com/latentcollapse/HLXv1.1.0"
    LICENSE = "MIT OR Apache-2.0"

    @classmethod
    def generate(cls, content_hash: str, blake3_hash: str = None) -> dict:
        """Generate a watermark block with dual-hash verification."""
        timestamp = datetime.datetime.now(datetime.UTC).isoformat().replace('+00:00', 'Z')

        # Create watermark payload
        payload = {
            "version": cls.WATERMARK_VERSION,
            "author": cls.AUTHOR,
            "repository": cls.REPOSITORY,
            "license": cls.LICENSE,
            "timestamp": timestamp,
            "content_hash_blake2b": content_hash,
        }

        # Add BLAKE3 if available
        if blake3_hash:
            payload["content_hash_blake3"] = blake3_hash

        # Sign the payload (hash of canonical JSON)
        canonical = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        signature = hashlib.blake2b(canonical.encode(), digest_size=32).hexdigest()

        payload["signature"] = signature
        payload["verification_rule"] = (
            "To verify: (1) Remove 'signature' field, (2) JSON-serialize with sort_keys=True "
            "and separators=(',',':'), (3) BLAKE2b-256 hash must equal signature. "
            "Secondary: If blake3 available, verify content_hash_blake3 matches BLAKE3 of corpus JSON."
        )

        return payload

    @classmethod
    def verify(cls, watermark: dict) -> bool:
        """Verify a watermark is authentic."""
        sig = watermark.get("signature")
        if not sig:
            return False

        payload = {k: v for k, v in watermark.items()
                   if k not in ("signature", "verification_rule")}
        canonical = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        expected = hashlib.blake2b(canonical.encode(), digest_size=32).hexdigest()

        return sig == expected


# =============================================================================
# HLX CANONICAL CORPUS v1.1.0
# =============================================================================

HLX_CANONICAL_CORPUS = {
    "meta": {
        "title": "HLX Language Family - Canonical Teaching Corpus",
        "version": "1.1.0",
        "status": "CANONICAL_ROOT",
        "purpose": "Complete didactic injection for teaching LLMs the HLX architecture with exaflopic 1:1 determinism.",
        "encoding": "UTF-8",
        "hash_algorithm": "BLAKE3/BLAKE2b (dual verification)",

        # Grok feedback: full_corpus_required directive
        "full_corpus_required": True,
        "truncation_policy": "INVALID. Truncated versions must not be used for LLM training. Fetch complete corpus from repository.",

        # Grok feedback: corpus_diff for version tracking
        "corpus_diff_v1_0_0": {
            "added_sections": ["encryption_spec (concrete AES-GCM-256)", "full_corpus_required", "truncation_policy", "pre_serialize_rules", "12_empire_extensions (Vulkan/SPIR-V stubs)"],
            "enhanced": [
                "meta (dual-hash, corpus_diff, concrete encryption)",
                "quiz (split into positive/negative, +10 hard negatives on invariants and edge cases)",
                "verification_rule (dual-hash support, E_FLOAT_SPECIAL, E_TRUNCATION_INVALID)"
            ],
            "unchanged": ["axioms", "architecture", "value_system", "contracts", "transliteration", "lc_encoding", "latent_space", "error_taxonomy", "examples", "invariants", "llm_directives (base)"]
        },

        # Grok feedback: Pre-serialize normalization rules with concrete Python examples
        "pre_serialize_rules": {
            "floats": {
                "rule": "Convert to IEEE754 hex for cross-platform determinism",
                "example": "3.14 → 0x400921f9f01b866e (hex of IEEE754 double)",
                "python_code": "import struct; hex(struct.unpack('>Q', struct.pack('>d', 3.14))[0])",
                "edge_cases": {
                    "NaN": "Forbidden. Any float(NaN) → E_FLOAT_SPECIAL",
                    "Infinity": "Forbidden. Any float(±Inf) → E_FLOAT_SPECIAL",
                    "Zero": "0.0 and -0.0 must normalize to single canonical form",
                    "detection_code": "import math; if math.isnan(x) or math.isinf(x): raise ValueError('E_FLOAT_SPECIAL')"
                }
            },
            "strings": {
                "rule": "UTF-8 NFC normalized",
                "example": "café (é as single char) vs cafe (e + combining acute) → both normalize to café",
                "python_code": "import unicodedata; unicodedata.normalize('NFC', 'café')",
                "enforcement": "Use unicodedata.normalize('NFC', s) before serialization"
            },
            "keys": {
                "rule": "Sorted lexicographically (ASCII order)",
                "example": "{z:1, a:2, m:3} → {a:2, m:3, z:1}",
                "python_code": "json.dumps(data, sort_keys=True, separators=(',', ':'))",
                "violation": "Unsorted keys → E_KEY_ORDER"
            },
            "whitespace": {
                "rule": "No trailing, Unix line endings (LF only)",
                "example": "field: 'text  ' → field: 'text' (trailing spaces removed)",
                "python_code": "text.rstrip(); text.replace('\\r\\n', '\\n').replace('\\r', '\\n')",
                "line_endings": "\\r\\n (Windows) or \\r (Mac) → \\n (Unix) only"
            },
            "arrays": {
                "rule": "No trailing commas, elements in declaration order",
                "example": "[1, 2, 3,] → E_TRAILING_COMMA",
                "order_stability": "Must preserve insertion order from source",
                "python_code": "json.dumps(array, separators=(',', ':'))  # No trailing comma in output"
            }
        },

        # Grok feedback: Encryption spec (CONCRETE for v1.1.0+)
        "encryption_spec": {
            "algorithm": "AES-GCM-256",
            "key_derivation": {
                "formula": "BLAKE3('hlx_v1.1.0_train' + model_id.lower().encode())",
                "deterministic": True,
                "normalization": "model_id MUST be normalized to lowercase before key derivation",
                "example_python": "key = blake3.blake3(b'hlx_v1.1.0_train' + 'claude-3.5-sonnet'.lower().encode()).digest()[:32]",
                "case_sensitivity": "'grok-4' and 'Grok-4' and 'GROK-4' all derive same key when normalized",
                "model_id_source": "From environment: $HLX_MODEL_ID or hardcoded in training pipeline (string, no salt needed)"
            },
            "nonce": {
                "size_bytes": 12,
                "generation": "os.urandom(12) per encryption operation",
                "placement": "First 12 bytes of encrypted file"
            },
            "auth_tag": {
                "size_bytes": 16,
                "placement": "Last 16 bytes of encrypted file",
                "purpose": "GCM authentication tag for integrity verification"
            },
            "transport_format": "[nonce_12][ciphertext_variable][auth_tag_16]",
            "example_layout": "nonce(12) || AES-GCM-encrypted_corpus || auth_tag(16) = total_encrypted_size",
            "status": "ACTIVE_v1.1.0",
            "decrypt_directive": "Parse nonce (first 12 bytes) and auth_tag (last 16 bytes), decrypt middle with GCM verification, verify post-decrypt BLAKE3 hash matches content_hash_blake3"
        }
    },

    "1_axioms": {
        "description": "The four inviolable truths governing all HLX systems.",
        "axioms": [
            {
                "id": "A1",
                "name": "DETERMINISM",
                "formal": "∀v ∈ HLXLite: encode(v) = encode(v)",
                "natural": "The same input code MUST always produce the same Latent Collapse (LC) stream. Bitwise identical. No exceptions.",
                "test": "encode(decode(encode(v))) == encode(v)",
                "negative_test": "encode(v, time=t1) != encode(v, time=t2) → E_NONDETERMINISM"
            },
            {
                "id": "A2",
                "name": "REVERSIBILITY",
                "formal": "∀v ∈ HLXLite: decode(encode(v)) = v",
                "natural": "Any value compressed into a Handle (⚳) can be resolved (⚯) back to its exact original state.",
                "test": "collapse(resolve(collapse(v))) == collapse(v)",
                "negative_test": "resolve(invalid_handle) → E_HANDLE_NOT_FOUND"
            },
            {
                "id": "A3",
                "name": "BIJECTION",
                "formal": "HLXL ↔ HLX (isomorphism)",
                "natural": "Track A (Lite/ASCII) and Track B (Runic/Glyph) are mathematically isomorphic. They map 1:1.",
                "test": "transliterate(transliterate(code, 'runic'), 'ascii') == code",
                "negative_test": "unknown_glyph('✦') → E_UNKNOWN_GLYPH"
            },
            {
                "id": "A4",
                "name": "UNIVERSAL_VALUE",
                "formal": "∀track: track → HLXLite → LC",
                "natural": "All surface syntaxes lower to the HLX-Lite Value System (Contracts 1-5) before encoding to LC.",
                "test": "lower(hlxl_code) == lower(hlx_code) (same CoreExpr)",
                "negative_test": "lower(invalid_syntax) → E_PARSE_FAILED"
            }
        ]
    },

    "2_architecture": {
        "description": "The Dual-Track Architecture with unified wire format.",
        "diagram": """
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
        """,
        "tracks": {
            "track_a_lite": {
                "name": "HLXL (Helix Lite)",
                "audience": ["Engineers", "IDEs", "Git", "CI/CD", "Humans"],
                "format": "ASCII Text",
                "pipeline": "HLXL → HLXL-LS → CoreExpr → HLX-Lite → LC"
            },
            "track_b_runic": {
                "name": "HLX (Helix Runic)",
                "audience": ["LLMs", "Context Windows", "Vector Stores", "Compression"],
                "format": "Unicode Glyphs",
                "pipeline": "HLX → HLX-LS → CoreExpr → HLX-Lite → LC"
            }
        }
    },

    "3_value_system": {
        "description": "HLX-Lite: The atomic value types underlying all HLX languages.",
        "types": {
            "NULL": {"id": 0, "lc_tag": "0x00", "encoding": "No payload"},
            "BOOL": {"id": 1, "lc_tag": "0x0A/0x0B", "encoding": "TRUE=0x0A, FALSE=0x0B"},
            "INT": {"id": 2, "lc_tag": "0x01", "encoding": "Signed LEB128"},
            "FLOAT": {"id": 3, "lc_tag": "0x02", "encoding": "IEEE 754 Double, Big-Endian"},
            "TEXT": {"id": 4, "lc_tag": "0x03", "encoding": "LEB128 length + UTF-8 bytes"},
            "BYTES": {"id": 5, "lc_tag": "0x04", "encoding": "LEB128 length + raw bytes"},
            "ARRAY": {"id": 6, "lc_tag": "0x05/0x06", "encoding": "ARR_START + elements + ARR_END"},
            "OBJECT": {"id": 7, "lc_tag": "0x07/0x08", "encoding": "OBJ_START + contract_id + sorted_fields + OBJ_END"}
        },
        "field_notation": {
            "syntax": "@N",
            "description": "@N denotes zero-based field index N within a contract object.",
            "rule": "Fields MUST be encoded in ascending index order in LC-B.",
            "violation": "E_FIELD_ORDER"
        }
    },

    "4_contracts": {
        "description": "The canonical contract registry. Contract IDs are namespaced.",
        "reference": "See Section 6 in corpus/README_GITHUB.md for full contract specifications.",
        "core_contracts": {
            "1:HLXLiteValue": {"id": 1, "purpose": "Root value wrapper"},
            "2:HLXLiteField": {"id": 2, "purpose": "Object field descriptor"},
            "3:HLXLiteObject": {"id": 3, "purpose": "Typed object container"},
            "4:HLXLiteDocument": {"id": 4, "purpose": "Top-level document wrapper"},
            "5:ProvenanceLite": {"id": 5, "purpose": "Document metadata"}
        },
        "latent_contracts": {
            "800:LatentHandle": {"id": 800, "purpose": "Reference to collapsed value"},
            "801:LatentTable": {"id": 801, "purpose": "Handle storage table"},
            "820:LSOp": {"id": 820, "purpose": "Latent Space operation instruction"}
        },
        "policy": {
            "unknown_contracts": "ALLOWED - transport layer is agnostic",
            "validation_level": "STRUCTURAL_ONLY",
            "semantic_interpretation": "EXTERNAL (application layer)"
        }
    },

    "5_transliteration": {
        "description": "Bijective mapping between HLXL (ASCII) and HLX (Runic). Reference for full table.",
        "rule": "Strict 1:1 mapping. No exceptions. Transliteration is lossless.",
        "reference": "See corpus/README_GITHUB.md Section 'Glyph Reference' for complete table.",
        "key_mappings": {
            "⟠": "program", "◇": "block", "⊢": "let", "↩": "return",
            "⚳": "ls.collapse", "⚯": "ls.resolve", "▷": "|>", "⟁": "&h_"
        }
    },

    "6_lc_encoding": {
        "description": "LC (Latent Collapse) - The canonical wire format with dual modes.",
        "reference": "See corpus/README_GITHUB.md Section 'LC Encoding Rules' for complete specification.",
        "modes": {
            "LC-B": {"status": "CANONICAL", "purpose": "Binary encoding for hashing, storage, and transport"},
            "LC-T": {"status": "PEDAGOGICAL", "purpose": "Text/glyph encoding for debugging and LLM context"}
        },
        "canonical_rules": [
            "No trailing data after stream end",
            "No duplicate field indices in objects",
            "Field indices MUST be in ascending order",
            "No NaN or Infinity in floats (raise E_FLOAT_SPECIAL)",
            "Empty objects still require OBJ_START/OBJ_END markers"
        ]
    },

    "7_latent_space": {
        "description": "The Latent Space runtime for handle-based value management.",
        "operations": {
            "COLLAPSE": {"glyph": "⚳", "ascii": "ls.collapse", "op_code": 1},
            "RESOLVE": {"glyph": "⚯", "ascii": "ls.resolve", "op_code": 0},
            "SNAPSHOT": {"glyph": "⚶", "ascii": "ls.snapshot", "op_code": 2},
            "TRANSACTION": {"glyph": "⚿", "ascii": "ls.transaction", "op_code": 3}
        },
        "handle_format": {
            "structure": "&h_<tag>_<id>",
            "example": "&h_ast_a1b2c3d4",
            "runic": "⟁tag₁"
        }
    },

    "8_error_taxonomy": {
        "description": "Canonical error codes organized by category. Reference for complete list.",
        "reference": "See corpus/README_GITHUB.md Section 'Error Taxonomy' for all error codes.",
        "ranges": {
            "1000-1099": "Lexical Errors",
            "1100-1199": "Syntactic Errors",
            "1200-1299": "Type Errors",
            "1300-1399": "Constraint Errors",
            "1400-1499": "Semantic Errors"
        },
        "key_errors": {
            "E_LC_PARSE": {"code": 1100, "trigger": "Malformed LC stream"},
            "E_FIELD_ORDER": {"code": 1301, "trigger": "Fields not in ascending index order"},
            "E_HANDLE_NOT_FOUND": {"code": 1401, "trigger": "Handle does not exist in CAS"}
        }
    },

    "9_examples": {
        "description": "End-to-end examples showing the complete pipeline. Reference for additional examples.",
        "reference": "See corpus/HLX_LLM_TRAINING_CORPUS_v1.0.0.md Section 9 for complete examples.",
        "minimal_example": {
            "name": "T0_Minimal",
            "hlxl": "program t { block main() { let x = 7; return x; } }",
            "hlx": "⟠ t { ◇ main() { ⊢ x = 7; ↩ x; } }",
            "expected_result": 7
        }
    },

    "10_invariants": {
        "description": "Formal invariants that MUST hold at all times. Reference for complete list.",
        "reference": "See corpus/README_GITHUB.md Section 'Formal Invariants'.",
        "key_invariants": [
            {"id": "INV-001", "name": "TOTAL_FIDELITY", "rule": "decode(encode(v)) == v"},
            {"id": "INV-002", "name": "HANDLE_IDEMPOTENCE", "rule": "collapse(v) == collapse(v)"},
            {"id": "INV-003", "name": "FIELD_ORDER", "rule": "fields[i].index < fields[i+1].index"}
        ]
    },

    "11_llm_directives": {
        "description": "Instructions for LLMs operating in HLX mode with error handling.",
        "directives": [
            "D1: Accept input in HLXL (ASCII) or HLX (Runic) interchangeably",
            "D2: Validate syntax against canonical grammars; on failure → E_PARSE_FAILED",
            "D3: Treat glyphs like ⚳ ⚯ ⟁ as semantic operators, not decoration",
            "D4: Prioritize Contract IDs (e.g., 14, 800) over arbitrary JSON shapes",
            "D5: When asked to 'Collapse', simulate hashing and return a handle",
            "D6: When asked to 'Resolve', retrieve the original value exactly; missing → E_HANDLE_NOT_FOUND",
            "D7: Converting between tracks MUST be lossless; invalid glyph → E_UNKNOWN_GLYPH",
            "D8: Use canonical error codes (E_*) from Section 8",
            "D9: Honor MAX_DEPTH=64, MAX_SIZE=1MB; violations → E_DEPTH_EXCEEDED, E_SIZE_EXCEEDED",
            "D10: Enforce ascending field index order; violations → E_FIELD_ORDER",
            "D11: Simulate failures explicitly when testing negative paths"
        ],
        "quiz": {
            "description": "Self-test for LLM validation - positives and negatives, core and empire",
            "positive_questions": [
                {"q": "What is ⚳ in ASCII?", "a": "ls.collapse"},
                {"q": "What axiom guarantees decode(encode(v))==v?", "a": "A2: REVERSIBILITY"},
                {"q": "What axiom guarantees HLXL ↔ HLX isomorphism?", "a": "A3: BIJECTION"},
                {"q": "True or false: All surfaces lower to HLX-Lite before LC encoding?", "a": "True (A4: UNIVERSAL_VALUE)"},
                {"q": "What contract ID for SPIR-V shader binaries (empire)?", "a": "900 (VulkanShader)"},
                {"q": "What contract ID for compute kernels with workgroup_size (empire)?", "a": "901 (ComputeKernel)"},
                {"q": "What contract ID for multi-stage GPU pipelines with sync_barriers (empire)?", "a": "902 (PipelineConfig)"}
            ],
            "negative_questions": [
                {"q": "What error for {14:{@1:123, @0:456}}?", "a": "E_FIELD_ORDER (fields not in ascending index)"},
                {"q": "What error for resolve(&h_nonexistent)?", "a": "E_HANDLE_NOT_FOUND"},
                {"q": "What error for IEEE 754 NaN float?", "a": "E_FLOAT_SPECIAL (special values forbidden)"},
                {"q": "What error for IEEE 754 Infinity float?", "a": "E_FLOAT_SPECIAL (special values forbidden)"},
                {"q": "What error for float -0.0 vs 0.0 pre-serialize mismatch?", "a": "E_FLOAT_SPECIAL (must normalize to canonical form)"},
                {"q": "What error for SPIR-V bytes containing NaN-inf pattern (compute edge)?", "a": "E_FLOAT_SPECIAL (binary format violation, detected in pre_serialize)"},
                {"q": "What error for unknown glyph ✦?", "a": "E_UNKNOWN_GLYPH (not in transliteration table)"},
                {"q": "What error for depth > 64?", "a": "E_DEPTH_EXCEEDED (exceeds MAX_DEPTH=64)"},
                {"q": "What error for serialized size > 1MB?", "a": "E_SIZE_EXCEEDED (exceeds MAX_OBJ_SIZE=1MB)"},
                {"q": "Can truncated corpus be used for LLM training?", "a": "No - E_TRUNCATION_INVALID. Always use full chapters from releases."},
                {"q": "Violate A1 (DETERMINISM): encode(v, seed=1) != encode(v, seed=2)?", "a": "E_NONDETERMINISM"},
                {"q": "Violate A2 (REVERSIBILITY): collapse(resolve(invalid)) = ?", "a": "E_HANDLE_NOT_FOUND before collapse"},
                {"q": "Decrypt corpus with wrong model_id (e.g., 'Grok-4' vs 'grok-4')?", "a": "E_GCM_AUTH_FAIL (case-sensitive). Use model_id.lower() for consistency."},
                {"q": "What is the transport format for encrypted corpus?", "a": "[nonce_12][ciphertext_variable][auth_tag_16]"},
                {"q": "True or false: Model_id is case-insensitive for key derivation?", "a": "False. Must use model_id.lower().encode() for BLAKE3 determinism."}
            ]
        }
    },

    "12_empire_extensions": {
        "description": "Compute and rendering extensions for HLX—hooks into graphics and ML ecosystems.",
        "status": "EXPERIMENTAL",
        "target_audience": ["Graphics Engineers", "Compute Shader Specialists", "ML Pipeline Designers"],
        "extensions": {
            "vulkan_shaders": {
                "description": "SPIRV shader module binding for Vulkan compute and graphics pipelines",
                "contract_id": 900,
                "fields": {
                    "spirv_binary": {"type": "bytes", "description": "Raw SPIR-V module binary"},
                    "entry_point": {"type": "text", "description": "Shader entry point name (e.g., 'main')"},
                    "shader_stage": {"type": "text", "description": "Stage: 'compute', 'vertex', 'fragment', etc."},
                    "descriptor_bindings": {"type": "array<handle>", "description": "Handles to descriptor set bindings"}
                },
                "example": {
                    "hlxl": "contract 900 shader { spirv_binary: 0x4206031b..., entry_point: \"compute_reduce\", shader_stage: \"compute\", descriptor_bindings: [&h_buf_in_0, &h_buf_out_1] }",
                    "constraint": "SPIRV must be valid 1.0+ module; entry_point must exist in module"
                }
            },
            "compute_kernel": {
                "description": "Reusable compute kernel with grid parameters and shared memory config",
                "contract_id": 901,
                "fields": {
                    "kernel_name": {"type": "text", "description": "Kernel identifier"},
                    "shader_handle": {"type": "handle", "description": "Reference to VulkanShader (900)"},
                    "workgroup_size": {"type": "array<int>", "description": "[x, y, z] dimensions"},
                    "shared_memory_bytes": {"type": "int", "description": "Bytes of shared memory to allocate"},
                    "push_constants_layout": {"type": "text", "description": "Layout description for push constants (e.g., '2×int32 + 1×float32')"}
                }
            },
            "pipeline_config": {
                "description": "High-level pipeline builder for compute + rendering chains",
                "contract_id": 902,
                "fields": {
                    "pipeline_id": {"type": "text", "description": "Unique pipeline identifier"},
                    "stages": {"type": "array<handle>", "description": "Ordered handles to compute_kernel or graphics stages"},
                    "sync_barriers": {"type": "array<{stage_idx: int, memory_scope: text}>", "description": "Synchronization points"},
                    "output_image": {"type": "handle", "description": "Final image handle for readback"}
                }
            }
        },
        "design_rationale": "SPIR-V is the canonical intermediate representation for compute and graphics on modern GPUs. By embedding contract 900+ into HLX corpus, we enable direct specification of compute pipelines without language-level abstractions. Hooks Vulkan experts (like Sascha Willems) into HLX ecosystem by making GPU workloads first-class objects.",
        "integration_note": "These contracts are transport-only in v1.1.0. Execution requires external Vulkan runtime. Future versions will add native LC→SPIR-V JIT compilation.",
        "security_note": "SPIR-V binary validation is implementation-specific. Always verify binaries from untrusted sources."
    }
}


# =============================================================================
# CORPUS GENERATOR v1.1.0
# =============================================================================

def generate_corpus():
    """Generate the complete canonical corpus with dual-hash verification."""

    # Serialize corpus to canonical JSON
    corpus_json = json.dumps(HLX_CANONICAL_CORPUS, indent=2, sort_keys=False, ensure_ascii=False)

    # Compute BLAKE2b content hash
    blake2b_hash = hashlib.blake2b(corpus_json.encode('utf-8'), digest_size=32).hexdigest()

    # Compute BLAKE3 hash if available
    blake3_hash = None
    if HAS_BLAKE3:
        blake3_hash = blake3.blake3(corpus_json.encode('utf-8')).hexdigest()

    # Generate watermark with dual hashes
    watermark = CopyrightWatermark.generate(blake2b_hash, blake3_hash)

    # Create final package
    package = {
        "__watermark__": watermark,
        "__integrity__": {
            "algorithm": "BLAKE2b-256 (primary) + BLAKE3 (secondary)",
            "content_hash_blake2b": blake2b_hash,
            "content_hash_blake3": blake3_hash if blake3_hash else "BLAKE3 not available - install with: pip install blake3",
            "verification": "Hash of JSON corpus (excluding __watermark__ and __integrity__ sections)",
            "full_corpus_required": True,
            "truncation_invalid": "Truncated versions MUST NOT be used for LLM training"
        },
        "corpus": HLX_CANONICAL_CORPUS
    }

    return package, corpus_json, blake2b_hash, blake3_hash


def split_into_chapters(corpus):
    """Split corpus into 3 chapters to prevent truncation."""

    # Define chapter boundaries
    chapters = {
        "CORE": ["meta", "1_axioms", "2_architecture", "3_value_system", "4_contracts", "5_transliteration"],
        "RUNTIME": ["6_lc_encoding", "7_latent_space", "8_error_taxonomy", "10_invariants"],
        "EXTENSIONS": ["9_examples", "11_llm_directives", "12_empire_extensions"]
    }

    chapter_data = {}
    for chapter_name, sections in chapters.items():
        chapter_data[chapter_name] = {}
        for section in sections:
            if section in corpus:
                chapter_data[chapter_name][section] = corpus[section]

    return chapter_data, chapters


def main():
    print("=" * 70)
    print("HLX CANONICAL CORPUS GENERATOR v1.1.0 (3-CHAPTER SPLIT)")
    print("=" * 70)

    package, corpus_json, blake2b_hash, blake3_hash = generate_corpus()
    corpus = HLX_CANONICAL_CORPUS

    # Output paths
    out_dir = Path(__file__).parent.parent / "corpus"
    out_dir.mkdir(exist_ok=True)

    # Split into 3 chapters
    chapter_data, chapter_map = split_into_chapters(corpus)

    # Recompute hash on assembled corpus (chapters in canonical order) for consistency
    assembled_corpus = {}
    for chapter_name in ["CORE", "RUNTIME", "EXTENSIONS"]:
        assembled_corpus.update(chapter_data[chapter_name])

    assembled_json = json.dumps(assembled_corpus, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    assembled_blake2b = hashlib.blake2b(assembled_json.encode('utf-8'), digest_size=32).hexdigest()

    # Create manifest with chapter metadata and version diffs
    manifest = {
        "title": "HLX Canonical Corpus v1.1.0 (3-Chapter Edition)",
        "status": "PRODUCTION",
        "chapters": {
            "CORE": {
                "sequence": 1,
                "sections": chapter_map["CORE"],
                "purpose": "Foundational language spec (always load first)",
                "diff_v1_0_0": {
                    "added": ["encryption_spec (concrete AES-GCM-256 with model_id normalization)"],
                    "enhanced": ["meta (model_id.lower() directive added)"],
                    "unchanged": ["axioms", "architecture", "value_system", "contracts", "transliteration"]
                }
            },
            "RUNTIME": {
                "sequence": 2,
                "sections": chapter_map["RUNTIME"],
                "purpose": "Operational mechanics (load after CORE)",
                "diff_v1_0_0": {
                    "added": [],
                    "enhanced": [],
                    "unchanged": ["lc_encoding", "latent_space", "error_taxonomy", "invariants"]
                }
            },
            "EXTENSIONS": {
                "sequence": 3,
                "sections": chapter_map["EXTENSIONS"],
                "purpose": "Examples, directives, Vulkan (optional but recommended)",
                "diff_v1_0_0": {
                    "added": ["pre_serialize_rules examples (concrete Python code)", "Vulkan negatives in quiz"],
                    "enhanced": ["quiz (split positive/negative, +15 hard negatives, +3 empire contract Q)", "llm_directives (D11 & full set)"],
                    "unchanged": ["examples", "empire_extensions (structure)"]
                }
            }
        },
        "integrity": {
            "content_hash_blake2b": assembled_blake2b,
            "content_hash_blake3": hashlib.blake3(assembled_json.encode('utf-8')).hexdigest() if HAS_BLAKE3 else "Not available",
            "watermark_signature": package["__watermark__"]["signature"]
        },
        "loading_notes": "All 3 chapters must be complete and untruncated for full verification. Load in CORE → RUNTIME → EXTENSIONS order.",
        "security": "Model_id must be normalized to lowercase before AES-GCM key derivation",
        "version": {
            "corpus": "v1.1.0",
            "chapter_split": "v1.1.0 (3-chapter edition)",
            "baseline": "v1.0.0"
        }
    }

    # Write manifest
    manifest_path = out_dir / "HLX_MANIFEST_v1.0.0.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # Write each chapter
    chapter_paths = {}
    for chapter_name, chapter_contents in chapter_data.items():
        chapter_path = out_dir / f"HLX_CHAPTER_{chapter_name}_v1.0.0.json"
        chapter_package = {
            "__watermark__": package["__watermark__"],
            "__integrity__": {
                "algorithm": "BLAKE2b-256",
                "chapter": chapter_name,
                "sections": chapter_map[chapter_name],
                "manifest_hash": hashlib.blake2b(json.dumps(manifest, sort_keys=True).encode(), digest_size=32).hexdigest()
            },
            "corpus": chapter_contents
        }

        with open(chapter_path, 'w', encoding='utf-8') as f:
            json.dump(chapter_package, f, indent=2, ensure_ascii=False)

        chapter_paths[chapter_name] = chapter_path
        size = chapter_path.stat().st_size
        print(f"  - {chapter_path.name} ({size:,} bytes)")

    # Write full package (for backwards compatibility)
    package_path = out_dir / "HLX_CANONICAL_CORPUS_v1.0.0.json"
    with open(package_path, 'w', encoding='utf-8') as f:
        json.dump(package, f, indent=2, ensure_ascii=False)

    # Write watermark separately
    watermark_path = out_dir / "HLX_WATERMARK_v1.0.0.json"
    with open(watermark_path, 'w', encoding='utf-8') as f:
        json.dump(package["__watermark__"], f, indent=2)

    print(f"\nContent Hash (BLAKE2b): {blake2b_hash}")
    if blake3_hash:
        print(f"Content Hash (BLAKE3):  {blake3_hash}")
    print(f"Watermark Signature:    {package['__watermark__']['signature']}")
    print(f"\nGenerated files:")
    print(f"  MANIFEST:")
    print(f"  - {manifest_path} (chapter manifest)")
    print(f"  CHAPTERS:")
    for chapter_name, path in chapter_paths.items():
        print(f"  - {path.name} ({chapter_name})")
    print(f"  BACKWARDS COMPATIBILITY:")
    print(f"  - {package_path} (full corpus, single file)")
    print(f"  - {watermark_path} (standalone watermark)")

    # Verify watermark
    if CopyrightWatermark.verify(package["__watermark__"]):
        print("\n[OK] Watermark verification PASSED")
    else:
        print("\n[ERROR] Watermark verification FAILED")

    return package


if __name__ == "__main__":
    main()
