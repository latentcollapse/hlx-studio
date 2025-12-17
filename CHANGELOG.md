# Changelog - HLX Teaching Corpus

All notable changes to the HLX teaching corpus are documented here.

## [1.1.0] - 2025-12-14

### Added
- **Watermark Verification Tool**: `tools/verify_watermark.py` validates corpus authenticity via BLAKE2b-256 signature
- **Encryption Specification**: AES-GCM-256 with BLAKE3 key derivation protocol documented
- **Enhanced LLM Directives**: Expanded D1-D10 with error handling examples and negative test paths
- **Interactive Quizzes**: Inline validation scenarios (e.g., field ordering, LC-T parsing)
- **Verify Watermark Script**: Cryptographic proof of ownership with reproducible signature
- **CONTRIBUTING.md**: Guidelines for extending the corpus

### Changed
- **Repository Focus**: Cleaned to contain ONLY corpus materials (v1.1.0 canonical edition)
- **Documentation**: Expanded training corpus to 720 lines with full coverage of all 11 sections
- **Corpus Organization**: Structured as `corpus/` directory with canonical, raw, and watermark files

### Fixed
- Removed IDE/studio dependencies from v1.1.0 release (kept in hlx-dev-studio repo)
- Eliminated file size bloat (removed Electron builds, node_modules references)

### Technical Details
- **Watermark Algorithm**: BLAKE2b-256(canonical_json)
- **Watermark Signature**: `a7d6b60d4008efd9a897ca930f1e1841b25bbf1debe50bfb85c8be05b129b394`
- **Content Hash**: `32f91dbdfe95d3b98429204c521522a6664042e321bcb8fb6c7912ce40becf4c`
- **Format**: JSON (canonical) + Markdown (pedagogical) + Watermark (proof)

---

## [1.0.0] - Initial Release

### Features
- Complete HLX-Lite specification with 4 axioms
- Value system with 8 primitive types
- LC-B (binary) and LC-T (text) wire formats
- Contract registry (core, latent, execution contracts)
- Full transliteration table (ASCII ↔ Runic)
- Formal invariants (INV-001 through INV-006)
- 5 complete end-to-end examples
- Error taxonomy with canonical error codes
- 10 LLM operation directives

### Documentation
- Comprehensive README with quick-start
- Dual-track architecture visualization
- Glyph reference tables
- Contract specification details
- LC encoding rules and constraints

---

## Verification

To verify corpus authenticity:

```bash
python3 tools/verify_watermark.py corpus/HLX_CANONICAL_CORPUS_v1.0.0.json
```

Expected output:
```
[✓] WATERMARK VALID - Corpus is authentic and unmodified
```

---

## Future Roadmap

### v1.2.0 (Planned)
- Encrypted corpus with AES-GCM-256 (key: BLAKE3('hlx_v1.2.0_bootstrap'))
- Merkle tree proof for corpus sections
- CI/CD validation (GitHub Actions)
- Test vectors for round-trip verification

### v2.0.0 (Future)
- Runtime extensions (Vulkan, compute shaders)
- Machine learning model integration
- Optimized corpus for specific LLM architectures

---

## Author

**Matt (latentcollapse)**

Repository: https://github.com/latentcollapse/HLXv1.1.0

---

## License

Dual-licensed under **MIT** OR **Apache-2.0** at your option.
