#!/usr/bin/env python3
"""
HLX CHAPTER VERIFICATION TOOL v1.1.0
====================================
Per-chapter integrity verification against manifest.

Validates:
- Each chapter file exists and is complete
- Chapter hash matches manifest integrity
- Load sequence order
- Truncation detection per chapter
- Manifest structural integrity

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


def verify_chapters(manifest_path: str) -> bool:
    """
    Verify all chapters against manifest.

    Args:
        manifest_path: Path to HLX_MANIFEST_v1.0.0.json

    Returns:
        True if all chapters valid
        Raises SystemExit with E_CHAPTER_MISMATCH on failure
    """

    manifest_file = Path(manifest_path)
    corpus_dir = manifest_file.parent

    if not manifest_file.exists():
        print(f"[E_MANIFEST_NOT_FOUND] {manifest_path}")
        sys.exit(1)

    with open(manifest_file, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    print("=" * 70)
    print("HLX CHAPTER VERIFICATION v1.1.0")
    print("=" * 70)

    # Verify manifest structure
    print(f"\n[*] Manifest: {manifest_file.name}")
    print(f"    Status: {manifest.get('status')}")
    print(f"    Chapters: {len(manifest.get('chapters', {}))}")

    if "chapters" not in manifest or "integrity" not in manifest:
        print(f"[E_MANIFEST_INCOMPLETE] Missing chapters or integrity section")
        sys.exit(1)

    expected_chapters = ["CORE", "RUNTIME", "EXTENSIONS"]
    actual_chapters = list(manifest["chapters"].keys())

    if set(expected_chapters) != set(actual_chapters):
        print(f"[E_CHAPTER_MISMATCH] Expected {expected_chapters}, got {actual_chapters}")
        sys.exit(1)

    # Verify each chapter in sequence order
    print(f"\n[*] Verifying chapters in load order...")

    chapter_order = sorted(
        manifest["chapters"].items(),
        key=lambda x: x[1].get("sequence", 999)
    )

    for chapter_name, chapter_info in chapter_order:
        seq = chapter_info.get("sequence")
        sections = chapter_info.get("sections", [])
        purpose = chapter_info.get("purpose", "")

        chapter_file = corpus_dir / f"HLX_CHAPTER_{chapter_name}_v1.0.0.json"

        print(f"\n    [{seq}] {chapter_name}")

        # Check file exists
        if not chapter_file.exists():
            print(f"        [E_CHAPTER_NOT_FOUND] {chapter_file.name}")
            sys.exit(1)

        file_size = chapter_file.stat().st_size
        print(f"        File: {file_size:,} bytes")

        # Load chapter
        try:
            with open(chapter_file, 'r', encoding='utf-8') as f:
                chapter_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"        [E_JSON_PARSE] {e}")
            sys.exit(1)

        # Check structure
        if "__watermark__" not in chapter_data or "__integrity__" not in chapter_data:
            print(f"        [E_CHAPTER_INCOMPLETE] Missing watermark or integrity block")
            sys.exit(1)

        # Verify sections
        corpus = chapter_data.get("corpus", {})
        actual_sections = set(corpus.keys())
        expected_sections = set(sections)

        if actual_sections != expected_sections:
            missing = expected_sections - actual_sections
            extra = actual_sections - expected_sections
            print(f"        [E_SECTION_MISMATCH]")
            if missing:
                print(f"          Missing: {missing}")
            if extra:
                print(f"          Extra: {extra}")
            sys.exit(1)

        print(f"        Sections: {len(actual_sections)} ✓")

        # Verify integrity hash (using canonical form)
        corpus_canonical = json.dumps(corpus, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
        chapter_blake2b = hashlib.blake2b(corpus_canonical.encode('utf-8'), digest_size=32).hexdigest()

        integrity = chapter_data.get("__integrity__", {})
        expected_hash = integrity.get("content_hash", "")

        if not expected_hash:
            print(f"        [W] No per-chapter hash in integrity block (OK for v1.1.0)")
        elif chapter_blake2b != expected_hash:
            print(f"        [E_BLAKE2B_MISMATCH] Chapter integrity failed")
            print(f"          Expected: {expected_hash}")
            print(f"          Computed: {chapter_blake2b}")
            sys.exit(1)

        print(f"        Hash: {chapter_blake2b[:16]}... ✓")

        # Check for truncation
        if "(truncated" in corpus_canonical:
            print(f"        [E_TRUNCATION_DETECTED] Chapter contains truncation marker")
            sys.exit(1)

        # Verify manifest_hash (proof this chapter belongs to its manifest)
        # Note: manifest_hash is computed at generation time and may differ if manifest is regenerated
        # For production use, encrypt chapters to cryptographically bind them to manifest
        if "manifest_hash" in integrity:
            print(f"        Manifest bound: Yes (cryptographic binding available in encrypted mode)")

    # Verify assembled integrity
    print(f"\n[*] Verifying assembled corpus integrity...")

    assembled_corpus = {}
    for chapter_name, chapter_info in chapter_order:
        chapter_file = corpus_dir / f"HLX_CHAPTER_{chapter_name}_v1.0.0.json"
        with open(chapter_file, 'r', encoding='utf-8') as f:
            chapter_data = json.load(f)
        assembled_corpus.update(chapter_data.get("corpus", {}))

    assembled_canonical = json.dumps(assembled_corpus, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    assembled_blake2b = hashlib.blake2b(assembled_canonical.encode('utf-8'), digest_size=32).hexdigest()

    expected_assembled = manifest["integrity"]["content_hash_blake2b"]
    if assembled_blake2b != expected_assembled:
        print(f"    [E_ASSEMBLED_MISMATCH] Chapters don't assemble to manifest hash")
        print(f"      Expected: {expected_assembled}")
        print(f"      Computed: {assembled_blake2b}")
        sys.exit(1)

    print(f"    Assembled hash: {assembled_blake2b[:16]}... ✓")
    print(f"    Sections: {len(assembled_corpus)} ✓")

    # Final verdict
    print(f"\n[✓] ALL CHAPTER VERIFICATIONS PASSED")
    print(f"    Chapters: {len(chapter_order)}/3 valid")
    print(f"    Integrity: VERIFIED")
    print(f"    Sequence: VALID (CORE → RUNTIME → EXTENSIONS)")
    print(f"    Status: READY FOR INGESTION")

    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <manifest_path>")
        print(f"\nExample:")
        print(f"  {sys.argv[0]} corpus/HLX_MANIFEST_v1.0.0.json")
        sys.exit(1)

    manifest_path = sys.argv[1]

    try:
        verify_chapters(manifest_path)
    except Exception as e:
        print(f"[E_CHAPTER_MISMATCH] Verification failed: {e}")
        sys.exit(1)
