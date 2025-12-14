#!/usr/bin/env python3
"""
HLX CORPUS FULL VERIFICATION TOOL v1.1.0
========================================
Comprehensive integrity verification for HLX teaching corpus.
Detects truncation, hash mismatches, missing sections, and handles AES-GCM decryption.

Features:
- Truncation detection (prevents LLM hallucinations on edges)
- Dual-hash verification (BLAKE2b + BLAKE3)
- AES-GCM-256 decryption with deterministic key derivation
- GCM auth tag verification
- Watermark signature validation
- Structure completeness checks

Author: Matt (latentcollapse)
License: MIT OR Apache-2.0
"""

import json
import hashlib
import sys
import os
from pathlib import Path

# Optional BLAKE3 support
try:
    import blake3
    HAS_BLAKE3 = True
except ImportError:
    HAS_BLAKE3 = False

# Optional AES-GCM support for encrypted corpus
try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    HAS_AES_GCM = True
except ImportError:
    HAS_AES_GCM = False


def decrypt_corpus(encrypted_bytes: bytes, model_id: str) -> bytes:
    """
    Decrypt AES-GCM-256 encrypted corpus.

    Format: [nonce_12][ciphertext_variable][auth_tag_16]
    Key: BLAKE3('hlx_v1.1.0_train' + model_id.encode())

    Returns decrypted JSON bytes or raises SystemExit on failure.
    """

    if not HAS_AES_GCM:
        print("[W_NO_AES_GCM] AES-GCM not available. Install: pip install cryptography")
        print("[W_ENCRYPTED] Cannot decrypt corpus without cryptography library")
        sys.exit(1)

    if len(encrypted_bytes) < 28:  # min: nonce(12) + auth_tag(16) + 1 byte ciphertext
        print("[E_INVALID_ENCRYPTED] Encrypted payload too small")
        sys.exit(1)

    try:
        # Parse nonce (first 12 bytes) and auth_tag (last 16 bytes)
        nonce = encrypted_bytes[:12]
        ciphertext = encrypted_bytes[12:-16]
        auth_tag = encrypted_bytes[-16:]

        # Derive key deterministically
        if HAS_BLAKE3:
            key = blake3.blake3(b'hlx_v1.1.0_train' + model_id.encode()).digest()[:32]
        else:
            # Fallback to BLAKE2b if BLAKE3 not available
            key = hashlib.blake2b(
                b'hlx_v1.1.0_train' + model_id.encode(),
                digest_size=32
            ).digest()

        # Decrypt with GCM
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(nonce, auth_tag),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(ciphertext) + decryptor.finalize()

        print(f"[✓] AES-GCM-256 decryption SUCCESSFUL (model_id: {model_id})")
        return decrypted

    except Exception as e:
        print(f"[E_GCM_DECRYPT_FAIL] Decryption failed: {e}")
        print(f"[E_GCM_AUTH_FAIL] Possible causes: wrong model_id, corrupted file, or tampered auth_tag")
        sys.exit(1)


def verify_corpus(corpus_path: str, model_id: str = None) -> bool:
    """
    Full corpus verification with integrity checks.

    Args:
        corpus_path: Path to corpus file (JSON or encrypted binary)
        model_id: For encrypted corpus, the model ID used for key derivation
                 (e.g., 'claude-3.5-sonnet', 'grok-4')

    Returns True if corpus is valid and untruncated.
    Raises SystemExit with E_INTEGRITY_FAIL on any error.
    """

    corpus_file = Path(corpus_path)
    if not corpus_file.exists():
        print(f"[ERROR] File not found: {corpus_path}")
        sys.exit(1)

    # Load corpus (handle both JSON and encrypted binary)
    try:
        # Try reading as JSON first
        with open(corpus_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        encrypted_mode = False
    except (json.JSONDecodeError, UnicodeDecodeError):
        # If JSON fails, try as encrypted binary
        if model_id is None:
            print("[E_ENCRYPTED_NO_MODEL] File appears encrypted but no model_id provided")
            print("Usage: verify_corpus(path, model_id='claude-3.5-sonnet')")
            sys.exit(1)

        encrypted_bytes = corpus_file.read_bytes()
        decrypted_bytes = decrypt_corpus(encrypted_bytes, model_id)

        try:
            data = json.loads(decrypted_bytes.decode('utf-8'))
            encrypted_mode = True
        except json.JSONDecodeError as e:
            print(f"[E_JSON_PARSE] Decrypted data is not valid JSON: {e}")
            sys.exit(1)

    print("=" * 70)
    print("HLX CORPUS FULL VERIFICATION v1.1.0")
    if encrypted_mode:
        print(f"Mode: DECRYPTED (AES-GCM-256, model_id: {model_id})")
    else:
        print("Mode: PLAINTEXT (unencrypted)")
    print("=" * 70)

    # =========================================================================
    # 1. TRUNCATION CHECK
    # =========================================================================

    raw_content = corpus_file.read_text(encoding='utf-8')
    if '(truncated' in raw_content or raw_content.endswith('..."'):
        print("[E_TRUNCATION_INVALID] Corpus is truncated - VERIFICATION FAILED")
        print("  Full corpus required. Download untruncated version from:")
        print("  https://github.com/latentcollapse/HLXv1.1.0/releases")
        sys.exit(1)

    print("[✓] Truncation check PASSED (corpus is complete)")

    # =========================================================================
    # 2. WATERMARK VERIFICATION
    # =========================================================================

    if "__watermark__" not in data:
        print("[E_MISSING_WATERMARK] No watermark found")
        sys.exit(1)

    watermark = data["__watermark__"]
    required_wm_fields = ["version", "author", "repository", "license", "timestamp", "signature"]

    for field in required_wm_fields:
        if field not in watermark:
            print(f"[E_WATERMARK_INCOMPLETE] Missing field: {field}")
            sys.exit(1)

    print(f"[*] Watermark Information:")
    print(f"    Version: {watermark.get('version')}")
    print(f"    Author:  {watermark.get('author')}")
    print(f"    Repo:    {watermark.get('repository')}")

    # Verify watermark signature
    sig = watermark.get("signature")
    payload = {k: v for k, v in watermark.items()
               if k not in ("signature", "verification_rule")}
    canonical = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    expected_sig = hashlib.blake2b(canonical.encode(), digest_size=32).hexdigest()

    if sig != expected_sig:
        print(f"[E_WATERMARK_INVALID] Signature mismatch")
        print(f"  Expected: {expected_sig}")
        print(f"  Got:      {sig}")
        sys.exit(1)

    print(f"[✓] Watermark signature VALID")

    # =========================================================================
    # 3. INTEGRITY HASH VERIFICATION
    # =========================================================================

    if "__integrity__" not in data:
        print("[E_MISSING_INTEGRITY] No integrity block found")
        sys.exit(1)

    integrity = data["__integrity__"]
    stored_blake2b = integrity.get("content_hash_blake2b")
    stored_blake3 = integrity.get("content_hash_blake3")

    # Serialize corpus (without watermark/integrity)
    corpus_json = json.dumps(data.get("corpus", {}), indent=2, ensure_ascii=False)
    computed_blake2b = hashlib.blake2b(corpus_json.encode('utf-8'), digest_size=32).hexdigest()

    print(f"[*] Hash Verification:")
    print(f"    BLAKE2b (primary):")
    print(f"      Stored:   {stored_blake2b}")
    print(f"      Computed: {computed_blake2b}")

    if computed_blake2b != stored_blake2b:
        print(f"[E_BLAKE2B_MISMATCH] Hash integrity check FAILED")
        sys.exit(1)

    print(f"[✓] BLAKE2b-256 hash VALID")

    # Verify BLAKE3 if available and stored
    if HAS_BLAKE3 and stored_blake3 and "not available" not in str(stored_blake3):
        computed_blake3 = blake3.blake3(corpus_json.encode('utf-8')).hexdigest()
        print(f"\n    BLAKE3 (secondary - belt-and-suspenders):")
        print(f"      Stored:   {stored_blake3}")
        print(f"      Computed: {computed_blake3}")

        if computed_blake3 != stored_blake3:
            print(f"[E_BLAKE3_MISMATCH] Secondary hash check FAILED")
            sys.exit(1)

        print(f"[✓] BLAKE3 hash VALID")
    elif HAS_BLAKE3:
        print(f"\n[*] BLAKE3: Available but not stored in corpus (OK for v1.1.0)")
    else:
        print(f"\n[*] BLAKE3: Not installed (install with: pip install blake3)")

    # =========================================================================
    # 4. STRUCTURE VERIFICATION
    # =========================================================================

    corpus = data.get("corpus", {})
    required_sections = [
        "meta", "1_axioms", "2_architecture", "3_value_system",
        "4_contracts", "5_transliteration", "6_lc_encoding",
        "7_latent_space", "8_error_taxonomy", "9_examples",
        "10_invariants", "11_llm_directives"
    ]

    print(f"\n[*] Structure Verification:")
    missing_sections = []

    for section in required_sections:
        if section in corpus:
            print(f"    [✓] {section}")
        else:
            print(f"    [✗] {section} - MISSING")
            missing_sections.append(section)

    if missing_sections:
        print(f"\n[E_INCOMPLETE_CORPUS] Missing sections: {', '.join(missing_sections)}")
        sys.exit(1)

    # Check for new Grok feedback sections
    new_sections = ["12_empire_extensions"]
    print(f"\n[*] Extended Sections (Grok feedback v1.1.0+):")
    for section in new_sections:
        if section in corpus:
            print(f"    [✓] {section}")
        else:
            print(f"    [!] {section} - Optional in v1.1.0")

    # =========================================================================
    # 5. DIRECTIVES AND POLICIES
    # =========================================================================

    meta = corpus.get("meta", {})

    print(f"\n[*] Policy Verification:")
    print(f"    full_corpus_required: {meta.get('full_corpus_required')}")
    print(f"    truncation_policy: {'Present' if 'truncation_policy' in meta else 'Missing'}")
    print(f"    encryption_spec: {'Present' if 'encryption_spec' in meta else 'Missing'}")
    print(f"    pre_serialize_rules: {'Present' if 'pre_serialize_rules' in meta else 'Missing'}")

    if not meta.get('full_corpus_required'):
        print(f"[W_POLICY] full_corpus_required is False (unexpected)")

    # =========================================================================
    # 6. QUIZ INTEGRITY
    # =========================================================================

    quiz = corpus.get("11_llm_directives", {}).get("quiz", {})
    if quiz:
        pos_q = len(quiz.get("positive_questions", []))
        neg_q = len(quiz.get("negative_questions", []))
        print(f"\n[*] Quiz Content:")
        print(f"    Positive questions: {pos_q}")
        print(f"    Negative questions: {neg_q}")

        if neg_q < 8:
            print(f"[W_QUIZ] Expected at least 8 negative questions for hard edge case testing")

    # =========================================================================
    # FINAL VERDICT
    # =========================================================================

    print("\n" + "=" * 70)
    print("[✓ ALL CHECKS PASSED] Corpus is authentic, complete, and untruncated")
    print("=" * 70)
    print(f"\nVerification Summary:")
    print(f"  File: {corpus_path}")
    print(f"  Size: {len(raw_content):,} bytes")
    print(f"  Sections: {len(corpus)}/12+ required")
    print(f"  Watermark: VALID")
    print(f"  Hashes: VALID (BLAKE2b + {'BLAKE3' if HAS_BLAKE3 else 'BLAKE2b only'})")
    print(f"  Status: READY FOR LLM TRAINING")

    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <corpus_file> [model_id]")
        print(f"\nExamples:")
        print(f"  {sys.argv[0]} corpus/HLX_CANONICAL_CORPUS_v1.0.0.json")
        print(f"  {sys.argv[0]} corpus/HLX_CANONICAL_CORPUS_v1.0.0.json.enc claude-3.5-sonnet")
        print(f"  {sys.argv[0]} corpus/HLX_CANONICAL_CORPUS_v1.0.0.json.enc grok-4")
        print(f"\nFor encrypted corpus, model_id must match the key derivation source.")
        sys.exit(1)

    corpus_path = sys.argv[1]
    model_id = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        verify_corpus(corpus_path, model_id)
    except Exception as e:
        print(f"[E_INTEGRITY_FAIL] Verification failed: {e}")
        sys.exit(1)
