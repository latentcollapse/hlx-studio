# HLX v1.1.0 Release Packaging Plan

## Overview
Complete the final 5% of v1.1.0 by creating release bundles and updating documentation. Corpus is mathematically sound—this is pure release engineering.

## Current State
- ✅ 3-chapter corpus structure (CORE, RUNTIME, EXTENSIONS)
- ✅ Manifest with integrity hashes + chapter_diff
- ✅ 5 verification tools (verify_full, ingest, chapter_verify, verify_watermark, create_canonical_corpus)
- ✅ Mathematical perfection achieved (dual-hash, deterministic encryption, truncation-proof)
- ⚠️ README outdated (v1.0.0, doesn't mention 3-chapter structure)
- ❌ No release .zips (corpus files not bundled)
- ❌ No USAGE.md guide for tools

## Tasks

### 1. Update README_GITHUB.md
**File:** `corpus/README_GITHUB.md`

**Changes:**
- Update version badge: `1.0.0` → `1.1.0`
- Update status badge: `FROZEN` → `PRODUCTION`
- Add **3-Chapter Structure** section:
  - Explain why split (truncation prevention)
  - List chapters: CORE (14KB), RUNTIME (4KB), EXTENSIONS (10KB)
  - Load sequence: CORE → RUNTIME → EXTENSIONS
- Add **Tools Reference** section:
  - `verify_full.py`: Full corpus integrity check
  - `ingest.py`: Production ingestion (decrypt + verify + assemble)
  - `chapter_verify.py`: Per-chapter integrity validation
  - `verify_watermark.py`: Watermark signature check
  - `create_canonical_corpus.py`: Regenerate corpus from source
- Add **Release Bundles** section:
  - Link to .zip releases (untruncated corpus)
  - Installation instructions

**Why:** README is user-facing and currently misleading (shows v1.0.0, no chapter info)

---

### 2. Create USAGE.md
**File:** `corpus/USAGE.md`

**Content:**
- **Quick Start** (3 lines to verify + ingest)
- **Tool Reference** (detailed command examples for each tool)
- **Chapter Structure** (when to load which chapters)
- **Encryption** (how to decrypt with model_id)
- **Troubleshooting** (E_TRUNCATION_INVALID, E_CHAPTER_MISMATCH, etc.)

**Why:** Users need practical examples to use the tooling

---

### 3. Create Release Script
**File:** `tools/release.py`

**Purpose:** Bundle corpus into release .zips

**Functionality:**
```python
def create_release_bundle():
    """
    Creates untruncated .zip bundles for v1.1.0 release.

    Outputs:
    - HLX_v1.1.0_COMPLETE.zip (all chapters + manifest + tools)
    - HLX_v1.1.0_CHAPTERS_ONLY.zip (chapters + manifest, no tools)
    - HLX_v1.1.0_TOOLS_ONLY.zip (verification tools only)
    """

    # Bundle 1: Complete (corpus + tools)
    with zipfile.ZipFile('HLX_v1.1.0_COMPLETE.zip', 'w', compression=zipfile.ZIP_DEFLATED) as z:
        z.write('corpus/HLX_CHAPTER_CORE_v1.0.0.json')
        z.write('corpus/HLX_CHAPTER_RUNTIME_v1.0.0.json')
        z.write('corpus/HLX_CHAPTER_EXTENSIONS_v1.0.0.json')
        z.write('corpus/HLX_MANIFEST_v1.0.0.json')
        z.write('corpus/HLX_WATERMARK_v1.0.0.json')
        z.write('corpus/README_GITHUB.md')
        z.write('corpus/USAGE.md')
        z.write('tools/verify_full.py')
        z.write('tools/ingest.py')
        z.write('tools/chapter_verify.py')
        z.write('tools/verify_watermark.py')

    # Bundle 2: Chapters only
    with zipfile.ZipFile('HLX_v1.1.0_CHAPTERS_ONLY.zip', 'w', compression=zipfile.ZIP_DEFLATED) as z:
        z.write('corpus/HLX_CHAPTER_CORE_v1.0.0.json')
        z.write('corpus/HLX_CHAPTER_RUNTIME_v1.0.0.json')
        z.write('corpus/HLX_CHAPTER_EXTENSIONS_v1.0.0.json')
        z.write('corpus/HLX_MANIFEST_v1.0.0.json')
        z.write('corpus/README_GITHUB.md')

    # Bundle 3: Tools only
    with zipfile.ZipFile('HLX_v1.1.0_TOOLS_ONLY.zip', 'w', compression=zipfile.ZIP_DEFLATED) as z:
        z.write('tools/verify_full.py')
        z.write('tools/ingest.py')
        z.write('tools/chapter_verify.py')
        z.write('tools/verify_watermark.py')
        z.write('corpus/USAGE.md')

    # Verify zips are untruncated
    verify_zip_integrity('HLX_v1.1.0_COMPLETE.zip')

    print("[✓] Release bundles created")
```

**Why:** Ensures untruncated distribution, GitHub release-ready

---

### 4. Optional: Load-Order Validation in ingest.py
**File:** `tools/ingest.py`

**Enhancement:** Add explicit load-sequence check

```python
def validate_load_sequence(manifest):
    """Verify chapters loaded in correct sequence."""
    expected = ["CORE", "RUNTIME", "EXTENSIONS"]
    actual = sorted(manifest["chapters"], key=lambda k: manifest["chapters"][k]["sequence"])

    if actual != expected:
        print(f"[E_LOAD_ORDER] Expected {expected}, got {actual}")
        sys.exit(1)
```

**Why:** Prevents accidental out-of-order loading (low risk, nice-to-have)

---

## Execution Order

1. **Update README_GITHUB.md** (2 min)
   - Version badges
   - 3-chapter structure section
   - Tools reference

2. **Create USAGE.md** (5 min)
   - Quick start
   - Tool examples
   - Troubleshooting

3. **Create tools/release.py** (5 min)
   - Bundle logic
   - Zip creation
   - Integrity verification

4. **Run release.py** (1 min)
   - Generate .zip bundles
   - Verify untruncated

5. **Optional: Enhance ingest.py** (2 min)
   - Add load-order validation

6. **Commit & Push** (2 min)
   - `git add corpus/ tools/`
   - `git commit -m "release: v1.1.0 final - docs + untruncated .zips"`
   - `git push v1.1 main`

**Total time:** ~15 minutes

---

## Critical Files

- `corpus/README_GITHUB.md` (update)
- `corpus/USAGE.md` (create)
- `tools/release.py` (create)
- `tools/ingest.py` (optional enhancement)

---

## Success Criteria

✅ README reflects v1.1.0 + 3-chapter structure
✅ USAGE.md provides practical tool examples
✅ 3 release .zips generated (COMPLETE, CHAPTERS_ONLY, TOOLS_ONLY)
✅ Zips verified as untruncated
✅ GitHub release-ready

---

## Notes

- **No mathematical changes** - corpus is already bulletproof
- **Pure packaging** - making v1.1.0 accessible to users
- **Optional load-order validation** - nice-to-have, not critical
- **v1.2.0 prep** - encrypted chapters + BLAKE3 primary (future work)
