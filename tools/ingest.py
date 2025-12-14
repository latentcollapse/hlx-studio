#!/usr/bin/env python3
"""
HLX CORPUS PRODUCTION INGEST TOOL v1.1.0
========================================
Decrypt, verify, and ingest HLX corpus for LLM training.

Handles:
- AES-GCM-256 decryption with deterministic key derivation
- Dual-hash verification (BLAKE2b + BLAKE3)
- Chapter manifest verification
- Complete corpus assembly from 3 chapters
- Model_id normalization (lowercase)

Author: Matt (latentcollapse)
License: MIT OR Apache-2.0
"""

import json
import hashlib
import sys
from pathlib import Path

# Optional BLAKE3 support
try:
    import blake3
    HAS_BLAKE3 = True
except ImportError:
    HAS_BLAKE3 = False

# Optional AES-GCM support
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    HAS_AES_GCM = True
except ImportError:
    HAS_AES_GCM = False


def ingest_corpus(manifest_path: str, model_id: str = None) -> dict:
    """
    Production ingestion: decrypt (if needed), verify, and assemble corpus.

    Args:
        manifest_path: Path to HLX_MANIFEST_v1.0.0.json
        model_id: Model ID for AES-GCM key derivation (e.g., 'grok-4')
                 Must be normalized to lowercase

    Returns:
        Complete corpus dict with all sections, ready for training

    Raises:
        SystemExit on any integrity violation
    """

    manifest_file = Path(manifest_path)
    corpus_dir = manifest_file.parent

    if not manifest_file.exists():
        print(f"[E_MANIFEST_NOT_FOUND] {manifest_path}")
        sys.exit(1)

    # Load and verify manifest
    with open(manifest_file, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    print("=" * 70)
    print("HLX CORPUS PRODUCTION INGEST v1.1.0")
    print("=" * 70)
    print(f"\n[*] Manifest: {manifest_file.name}")
    print(f"    Status: {manifest.get('status')}")
    print(f"    Title: {manifest.get('title')}")

    # Normalize model_id if provided
    if model_id:
        model_id = model_id.lower()
        print(f"\n[*] Model ID (normalized): {model_id}")

    # Load all chapters in sequence
    assembled_corpus = {}
    chapter_order = ["CORE", "RUNTIME", "EXTENSIONS"]

    print(f"\n[*] Loading chapters...")
    for seq, chapter_name in enumerate(chapter_order, 1):
        chapter_info = manifest["chapters"].get(chapter_name)
        if not chapter_info:
            print(f"[W] Chapter {chapter_name} not in manifest (skipping)")
            continue

        chapter_file = corpus_dir / f"HLX_CHAPTER_{chapter_name}_v1.0.0.json"

        if not chapter_file.exists():
            # Try encrypted version
            encrypted_file = corpus_dir / f"HLX_CHAPTER_{chapter_name}_v1.0.0.json.enc"
            if encrypted_file.exists():
                print(f"    [{seq}] {chapter_name}: Loading encrypted...")
                if not model_id or not HAS_AES_GCM:
                    print(f"[E_ENCRYPTED_NO_MODEL] Encrypted chapter needs model_id and cryptography library")
                    sys.exit(1)

                chapter_data = decrypt_chapter(encrypted_file, model_id)
            else:
                print(f"[E_CHAPTER_NOT_FOUND] {chapter_file.name}")
                sys.exit(1)
        else:
            print(f"    [{seq}] {chapter_name}: Loading plaintext...")
            with open(chapter_file, 'r', encoding='utf-8') as f:
                chapter_pkg = json.load(f)

            chapter_data = chapter_pkg.get("corpus", {})

        # Verify chapter sections
        expected_sections = set(chapter_info["sections"])
        actual_sections = set(chapter_data.keys())

        if expected_sections != actual_sections:
            missing = expected_sections - actual_sections
            extra = actual_sections - expected_sections
            print(f"[E_CHAPTER_INCOMPLETE] {chapter_name}")
            if missing:
                print(f"  Missing: {missing}")
            if extra:
                print(f"  Extra: {extra}")
            sys.exit(1)

        print(f"        Sections: {', '.join(expected_sections)} ✓")

        # Merge into assembled corpus
        assembled_corpus.update(chapter_data)

    # Verify complete structure
    print(f"\n[*] Verifying complete corpus...")
    required_sections = [
        "meta", "1_axioms", "2_architecture", "3_value_system",
        "4_contracts", "5_transliteration", "6_lc_encoding",
        "7_latent_space", "8_error_taxonomy", "9_examples",
        "10_invariants", "11_llm_directives", "12_empire_extensions"
    ]

    missing = [s for s in required_sections if s not in assembled_corpus]
    if missing:
        print(f"[E_CORPUS_INCOMPLETE] Missing sections: {missing}")
        sys.exit(1)

    print(f"    All {len(required_sections)} sections present ✓")

    # Compute hashes for verification (MUST use canonical form)
    # Canonical form: indent=2, ensure_ascii=False, but compute hash on compact form
    corpus_canonical = json.dumps(assembled_corpus, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    blake2b_computed = hashlib.blake2b(corpus_canonical.encode('utf-8'), digest_size=32).hexdigest()

    expected_blake2b = manifest["integrity"]["content_hash_blake2b"]
    if blake2b_computed != expected_blake2b:
        print(f"[E_BLAKE2B_MISMATCH] Hash verification failed")
        print(f"  Expected: {expected_blake2b}")
        print(f"  Computed: {blake2b_computed}")
        print(f"  Note: Ensure all chapters are present and untruncated")
        sys.exit(1)

    print(f"    BLAKE2b hash: {blake2b_computed[:16]}... ✓")

    # Secondary BLAKE3 verification if available
    if HAS_BLAKE3:
        blake3_computed = blake3.blake3(corpus_canonical.encode('utf-8')).hexdigest()
        expected_blake3 = manifest["integrity"]["content_hash_blake3"]

        if expected_blake3 != "Not available" and blake3_computed != expected_blake3:
            print(f"[E_BLAKE3_MISMATCH] Secondary hash failed")
            sys.exit(1)

        print(f"    BLAKE3 hash: {blake3_computed[:16]}... ✓")

    # Check for truncation indicators
    if "(truncated" in corpus_canonical:
        print(f"[E_TRUNCATION_DETECTED] Corpus contains truncation marker")
        sys.exit(1)

    print(f"\n[✓] CORPUS INGESTION COMPLETE")
    print(f"    Chapters: CORE + RUNTIME + EXTENSIONS")
    print(f"    Sections: {len(assembled_corpus)}")
    print(f"    Status: READY FOR TRAINING")

    return assembled_corpus


def decrypt_chapter(encrypted_file: Path, model_id: str) -> dict:
    """
    Decrypt AES-GCM-256 encrypted chapter.

    Format: [nonce_12][ciphertext_variable][auth_tag_16]
    Key: BLAKE3('hlx_v1.1.0_train' + model_id.lower().encode())
    """

    if not HAS_AES_GCM:
        print(f"[E_NO_AES_GCM] AES-GCM not available. Install: pip install cryptography")
        sys.exit(1)

    encrypted_bytes = encrypted_file.read_bytes()

    if len(encrypted_bytes) < 28:
        print(f"[E_INVALID_ENCRYPTED] File too small to be valid encrypted chapter")
        sys.exit(1)

    try:
        # Parse format
        nonce = encrypted_bytes[:12]
        ciphertext = encrypted_bytes[12:-16]
        auth_tag = encrypted_bytes[-16:]

        # Derive key deterministically
        key_material = b'hlx_v1.1.0_train' + model_id.lower().encode()
        if HAS_BLAKE3:
            key = blake3.blake3(key_material).digest()[:32]
        else:
            key = hashlib.blake2b(key_material, digest_size=32).digest()

        # Decrypt
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext + auth_tag, None)

        chapter_pkg = json.loads(plaintext.decode('utf-8'))
        return chapter_pkg.get("corpus", {})

    except Exception as e:
        print(f"[E_GCM_DECRYPT_FAIL] Decryption failed: {e}")
        print(f"[E_GCM_AUTH_FAIL] Possible: wrong model_id, corrupted file, or tampered data")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <manifest_path> [model_id]")
        print(f"\nExamples:")
        print(f"  {sys.argv[0]} corpus/HLX_MANIFEST_v1.0.0.json")
        print(f"  {sys.argv[0]} corpus/HLX_MANIFEST_v1.0.0.json grok-4")
        print(f"\nFor encrypted chapters, model_id is required.")
        sys.exit(1)

    manifest_path = sys.argv[1]
    model_id = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        corpus = ingest_corpus(manifest_path, model_id)
        print(f"\n[READY] Corpus ready for training. Sections: {list(corpus.keys())}")
    except Exception as e:
        print(f"[E_INTEGRITY_FAIL] Ingestion failed: {e}")
        sys.exit(1)
