# Contributing to HLX Teaching Corpus

Thank you for interest in improving the HLX Language Family documentation and teaching materials. This document outlines guidelines for contributing.

---

## Code of Conduct

- **Be Precise**: Ambiguity is an error. All contributions must be deterministic and verifiable.
- **Preserve Immutability**: Once a corpus version is released, it's frozen. Propose changes via pull request for the next version.
- **Test Against Axioms**: Every addition must validate against the four core axioms (A1-A4).

---

## How to Contribute

### 1. Report Issues
- **Error in docs**: Open an issue with the exact line, error code, and test case
- **Missing coverage**: Identify gaps (e.g., "Contract 103 not documented")
- **Ambiguity**: Quote the problematic text and propose clarification

### 2. Submit Improvements

#### For Corpus Content
All submissions to `/corpus/` must:
1. **Pass watermark verification**: Run `python3 tools/verify_watermark.py` before submitting
2. **Maintain determinism**: No time-dependent or random elements
3. **Cross-reference**: Link related sections (e.g., "See Axiom A2 in Section 1")
4. **Include examples**: Every feature gets a minimal working example

#### For Tools and Scripts
- Write in Python 3.8+ or TypeScript
- Add docstrings and inline comments
- Include unit tests
- Test against the canonical corpus

### 3. Submission Workflow

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/HLXv1.1.0.git
cd HLXv1.1.0

# 2. Create a feature branch
git checkout -b improve/contract-103-vulkan

# 3. Make changes
# - Edit corpus files
# - Add scripts to /tools/
# - Update CHANGELOG.md

# 4. Verify (critical!)
python3 tools/verify_watermark.py corpus/HLX_CANONICAL_CORPUS_v1.0.0.json
# Should output: [✓] WATERMARK VALID

# 5. Commit with clear message
git add .
git commit -m "docs: Add Contract 103 (VulkanShader) with examples"

# 6. Push and open PR
git push origin improve/contract-103-vulkan
```

---

## Contribution Types

### A. Documentation Improvements
- Fix typos or unclear explanations
- Add examples to under-documented sections
- Clarify axiom implications
- Cross-reference related concepts

**Example PR Title**: `docs: Clarify BIJECTION rule with ASCII→Runic examples`

### B. New Contracts
- Define in corpus with contract ID, purpose, fields
- Provide LC-B encoding example
- Add transliteration rules
- Include test vector

**Example PR Title**: `feat: Add Contract 103 (VulkanShader) for compute integration`

### C. Test Vectors
- Add round-trip examples (encode → decode)
- Verify determinism across versions
- Test error conditions
- Document edge cases

**Example PR Title**: `test: Add LC-B encoding vectors for FLOAT special cases`

### D. Verification Tools
- Add to `/tools/` directory
- Must validate against `/corpus/` files
- Include README with usage examples
- Test on corpus files before submission

**Example PR Title**: `tool: Add corpus-diff utility to track version changes`

---

## Corpus Integrity Rules

### ✅ Do:
- Use deterministic algorithms (no randomness)
- Document all dependencies (BLAKE3, LEB128, etc.)
- Cross-reference related concepts
- Provide full examples (HLXL + HLX + LC-B + LC-T)
- Test round-trip (encode → decode → verify equality)

### ❌ Don't:
- Add non-deterministic content (timestamps, random IDs)
- Break existing axioms or invariants
- Modify frozen versions (submit for next version)
- Leave sections truncated
- Add vendor-specific extensions without "Empire Extension" label

---

## Pull Request Checklist

Before submitting, verify:

- [ ] Corpus files pass watermark verification
- [ ] All examples are complete (not truncated)
- [ ] Determinism is preserved (no randomness, no time-dependence)
- [ ] Axioms A1-A4 are honored
- [ ] New contracts have LC-B + LC-T examples
- [ ] Error cases are documented
- [ ] CHANGELOG.md is updated
- [ ] Commit messages are clear and reference issues if applicable

---

## Review Process

1. **Automated**: Watermark verification runs on all PRs
2. **Technical**: Maintainers check for axiom compliance and determinism
3. **Editorial**: Community feedback on clarity and completeness
4. **Merge**: Approved PRs are merged into main branch

---

## Versioning

- **Frozen versions** (v1.0.0, v1.1.0) are immutable; changes go to next version
- **In-development**: main branch accepts contributions for upcoming release
- **Increment by**: Major for breaking changes, Minor for features, Patch for fixes

---

## Questions?

- Open an issue for clarification
- Reference axioms and invariants in discussion
- Test your understanding with the quizzes in training corpus

---

## License

All contributions are licensed under **MIT** OR **Apache-2.0** (dual license).
By submitting a PR, you agree to license your contribution under both licenses.

---

<p align="center">
  <em>Building the empire together, bit by deterministic bit.</em>
</p>
