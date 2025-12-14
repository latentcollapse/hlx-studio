# HLX v1.0.0 CANONICAL SEALING INSTRUCTIONS

## 1. CANONICAL CONTENTS VERIFICATION
Confirm that the canonical capsule consists of EXACTLY these 10 files at ZIP root:

- hlx_codex.json
- hlx_contracts.json
- hlx_runtime_conformance.json
- hlx_grammar.ebnf
- hlx_triggers.yaml
- lc12_manifest_schema.json
- SYSTEM_PROMPT.txt
- README.md
- hlx_examples.hlx
- hlx_examples.hlxl

No subfolders. No duplicates. No version suffixes.

## 2. EXTERNAL HASHING PROCEDURE (NON-LLM)
Run the following in a deterministic shell environment to seal the artifact:

1. Create the canonical ZIP:
   ```bash
   zip -X -r hlx_bootstrap_capsule_v1.0.0.zip .
   ```

2. Compute SHA256 over the ZIP bytes:
   ```bash
   shasum -a 256 hlx_bootstrap_capsule_v1.0.0.zip
   # OR (Linux)
   sha256sum hlx_bootstrap_capsule_v1.0.0.zip
   ```

## 3. README UPDATE INSTRUCTION
Take the resulting 64-character hex digest from Step 2 and replace the placeholder line in `README.md`:

**Find:**
```
CAPSULE_INTEGRITY_HASH_SHA256: COMPUTE_WITH_EXPORTER
```

**Replace with:**
```
CAPSULE_INTEGRITY_HASH_SHA256: <ACTUAL_HEX_DIGEST>
```

*(Note: This stamp records the hash of the artifact state immediately prior to final distribution.)*

## 4. FINALIZATION
- This ZIP is the ONLY authoritative HLX v1.0.0 artifact.
- Any prior ZIPs or folders are superseded.
- Any mismatch between ZIP hash and README hash invalidates the capsule.
