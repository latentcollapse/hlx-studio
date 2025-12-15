# HLX Corpus Usage Guide

## Quick Start

To verify and ingest the corpus for training:

```bash
# 1. Verify integrity of all files
python3 tools/verify_full.py corpus/HLX_MANIFEST_v1.0.0.json

# 2. Ingest (assemble chapters)
python3 tools/ingest.py corpus/HLX_MANIFEST_v1.0.0.json
```

---

## Tool Reference

### `verify_full.py`

Validates the entire corpus package. Checks the manifest signature, then verifies the SHA-256 and BLAKE2b hashes of every chapter file.

```bash
python3 tools/verify_full.py <manifest_path>
```

**Exit Codes:**
- `0`: Success (All files valid)
- `1`: Verification failed (Hash mismatch, missing file, or invalid JSON)

### `ingest.py`

The primary production tool. It reads the manifest, loads the three chapters (CORE, RUNTIME, EXTENSIONS) in the correct order, verifies their content against the manifest hashes, and assembles them into a single Python dictionary object ready for training.

```bash
python3 tools/ingest.py <manifest_path> [model_id]
```

- `model_id`: Optional. Required only if using encrypted chapters.

### `chapter_verify.py`

Verifies a single chapter file against the manifest. Useful for partial updates or debugging.

```bash
python3 tools/chapter_verify.py <manifest_path> <chapter_name>
```
Example: `python3 tools/chapter_verify.py corpus/HLX_MANIFEST_v1.0.0.json CORE`

### `verify_watermark.py`

Verifies the cryptographic watermark embedded in the `HLX_WATERMARK_v1.0.0.json` file. This proves the corpus has not been tampered with since signing.

```bash
python3 tools/verify_watermark.py
```

---

## Chapter Structure

The HLX corpus is split into three files to ensure integrity and prevent context truncation.

| Sequence | Chapter | Filename | Description |
|----------|---------|----------|-------------|
| 1 | **CORE** | `HLX_CHAPTER_CORE_v1.0.0.json` | The 4 Axioms, Architecture Map, and HLX-Lite Value System. **MUST LOAD FIRST.** |
| 2 | **RUNTIME** | `HLX_CHAPTER_RUNTIME_v1.0.0.json` | Contracts, Transliteration rules, and LC Encoding specs. |
| 3 | **EXTENSIONS** | `HLX_CHAPTER_EXTENSIONS_v1.0.0.json` | Latent Space operations, Error Taxonomy, Invariants, and Examples. |

**Important:** The `ingest.py` tool automatically handles this sequencing. If loading manually, you **MUST** respect this order.

---

## Troubleshooting

### `E_TRUNCATION_DETECTED` / `E_CHAPTER_MISMATCH`
**Cause:** A chapter file is incomplete or corrupted.
**Fix:** Redownload the release bundle. Run `verify_full.py` to identify the corrupted file.

### `E_BLAKE2B_MISMATCH`
**Cause:** The assembled corpus content does not match the master hash in the manifest.
**Fix:** Ensure you are using the correct version of all three chapter files. Do not mix versions (e.g., v1.0.0 CORE with v1.1.0 RUNTIME).

### `E_NO_AES_GCM`
**Cause:** Attempting to decrypt encrypted chapters without the `cryptography` library.
**Fix:** Install the library: `pip install cryptography`

### `E_LOAD_ORDER`
**Cause:** Chapters were loaded out of sequence (e.g., EXTENSIONS before CORE).
**Fix:** Use `ingest.py` which handles ordering automatically, or fix your manual loading logic.
