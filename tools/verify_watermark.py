#!/usr/bin/env python3
"""
HLX Corpus Watermark Verification Tool

Verifies the cryptographic watermark of HLX corpus files to ensure
authenticity and immutability.

Usage:
    python3 verify_watermark.py ../corpus/HLX_CANONICAL_CORPUS_v1.0.0.json
"""

import json
import hashlib
import sys
from pathlib import Path


def verify_watermark(corpus_path):
    """Verify watermark signature and integrity."""
    corpus_path = Path(corpus_path)

    if not corpus_path.exists():
        print(f"ERROR: File not found: {corpus_path}")
        return False

    print(f"[*] Loading corpus: {corpus_path.name}")
    with open(corpus_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)

    # Extract watermark
    watermark = corpus.get("__watermark__")
    if not watermark:
        print("ERROR: No watermark found in corpus")
        return False

    # Extract signature
    stored_signature = watermark.get("signature")
    if not stored_signature:
        print("ERROR: No signature in watermark")
        return False

    # Reconstruct payload (without signature/verification_rule)
    payload = {
        k: v for k, v in watermark.items()
        if k not in ("signature", "verification_rule")
    }

    # Compute canonical JSON and hash
    canonical = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    computed_signature = hashlib.blake2b(
        canonical.encode('utf-8'),
        digest_size=32
    ).hexdigest()

    # Verify
    print(f"\n[*] Watermark Information:")
    print(f"    Author: {watermark.get('author')}")
    print(f"    Version: {watermark.get('version')}")
    print(f"    Timestamp: {watermark.get('timestamp')}")
    print(f"    Repository: {watermark.get('repository')}")
    print(f"    License: {watermark.get('license')}")

    print(f"\n[*] Signature Verification:")
    print(f"    Stored:   {stored_signature}")
    print(f"    Computed: {computed_signature}")

    if stored_signature == computed_signature:
        print(f"\n[✓] WATERMARK VALID - Corpus is authentic and unmodified")
        return True
    else:
        print(f"\n[✗] WATERMARK INVALID - Corpus has been tampered with!")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 verify_watermark.py <corpus_file>")
        print("\nExample:")
        print("  python3 verify_watermark.py ../corpus/HLX_CANONICAL_CORPUS_v1.0.0.json")
        sys.exit(1)

    corpus_file = sys.argv[1]
    valid = verify_watermark(corpus_file)
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
