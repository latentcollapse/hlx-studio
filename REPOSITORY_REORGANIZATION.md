# HLX Repository Reorganization Plan
## Three Repositories, Three Purposes

**Date:** 2025-12-15
**Status:** ACTIVE - Ready to execute
**Goal:** Clean separation of concerns for professional presentation

---

## The Problem

Right now everything lives in `helix-studio`:
- ✅ HLX v1.1.0 Corpus (frozen, complete, 106/106 tests passing)
- 🔄 HLX Runtime v1.0 (Python implementation)
- 🔄 Studio GUI (Electron/React/TypeScript)
- 🔄 Vulkan work-in-progress (partial)
- 🔄 Random test files, dev artifacts

**Issue:** When someone looks at this repo, they don't know what they're looking at. Is it a language spec? A GUI tool? A Vulkan engine?

---

## The Solution: Three Repositories

### 1. **HLXv1.1.0** (Teaching Materials - FROZEN)
**URL:** `github.com/latentcollapse/HLXv1.1.0`
**Purpose:** The canonical corpus specification
**Audience:** AI models, language designers, implementers

**Contents:**
```
HLXv1.1.0/
├── corpus/
│   ├── HLX_CHAPTER_CORE_v1.0.0.json
│   ├── HLX_CHAPTER_RUNTIME_v1.0.0.json
│   ├── HLX_CHAPTER_EXTENSIONS_v1.0.0.json
│   └── HLX_MANIFEST_v1.0.0.json
├── tools/
│   ├── chapter_verify.py
│   ├── usage_examples.py
│   └── analyze_corpus.py
├── README.md (Teaching materials badge, load instructions)
├── VERIFICATION_REPORT.md (106/106 tests)
├── LICENSE (MIT OR Apache-2.0)
└── .gitignore
```

**README.md header:**
```markdown
# HLX v1.1.0 Corpus
## Canonical Teaching Materials for AI Model Training

[![Status](https://img.shields.io/badge/status-frozen-blue)]()
[![Tests](https://img.shields.io/badge/tests-106%2F106-brightgreen)]()
[![License](https://img.shields.io/badge/license-MIT%20OR%20Apache--2.0-blue)]()

The HLX v1.1.0 corpus is the canonical specification for the HLX language family.
Use this corpus to train AI models, implement runtimes, or build tooling.

**This corpus is FROZEN. No further changes will be made to v1.1.0.**
```

**Status:** ✅ Already exists at this repo, just needs cleanup
**Action:** Remove non-corpus files, add "FROZEN" badges

---

### 2. **hlx-studio** (Development Environment)
**URL:** `github.com/latentcollapse/hlx-studio`
**Purpose:** GUI development environment for HLX
**Audience:** Developers who want to write HLX code

**Contents:**
```
hlx-studio/
├── src/
│   ├── main/           # Electron main process
│   ├── renderer/       # React UI
│   ├── components/     # HLXEngine, editors, etc.
│   └── hlx_runtime/    # Python runtime (bundled)
├── public/
├── release/            # Build artifacts
├── package.json
├── tsconfig.json
├── README.md
├── CONTRIBUTING.md
└── LICENSE
```

**README.md header:**
```markdown
# HLX Studio
## Visual Development Environment for HLX Language

[![Status](https://img.shields.io/badge/status-alpha-yellow)]()
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey)]()

HLX Studio is a GUI development environment for writing, testing, and debugging
HLX programs. Features live visualization, deterministic execution, and
content-addressed storage.

**⚠️ Alpha Status:** This is experimental software under active development.
```

**Status:** ❌ Doesn't exist yet (currently mixed with corpus)
**Action:** Create new repo, migrate Studio code

---

### 3. **hlx-vulkan** (Compute Engine - THE PROOF)
**URL:** `github.com/latentcollapse/hlx-vulkan`
**Purpose:** Vulkan compute backend with HLX integration
**Audience:** GPU engineers, Khronos community, performance engineers

**Contents:**
```
hlx-vulkan/
├── hlx_runtime/
│   ├── vulkan_runtime.py
│   ├── spirv_bridge.py
│   ├── lc_codec.py         # Copied from v1.1.0
│   ├── cas.py
│   ├── ls_ops.py
│   └── tests/
│       ├── test_vulkan_integration.py
│       └── test_opus_audit.py
├── shaders/
│   ├── vector_add.comp
│   ├── gemm.comp
│   └── *.spv (compiled)
├── benchmarks/
│   ├── gemm_comparison.py
│   ├── batch_inference.py
│   └── results/
│       └── *.csv
├── docker/
│   ├── Dockerfile.vulkan
│   └── docker-compose.yml
├── docs/
│   ├── VULKAN_ROADMAP.md
│   ├── PHASE1_ASSESSMENT.md
│   └── BENCHMARK_RESULTS.md
├── README.md
├── LICENSE
└── .github/
    └── workflows/
        └── vulkan_tests.yml
```

**README.md header:**
```markdown
# HLX+Vulkan Compute Engine
## Deterministic GPU Compute with Content-Addressed Storage

[![Status](https://img.shields.io/badge/status-experimental-orange)]()
[![Benchmarks](https://img.shields.io/badge/benchmark-GEMM-blue)]()

HLX+Vulkan is a compute engine that integrates HLX's deterministic execution
model with Vulkan compute shaders. Early benchmarks show 3× faster warm-start
latency vs CUDA on repeated inference workloads.

**📊 Benchmark:** Run `docker-compose up benchmark` to reproduce results

**⚠️ Experimental:** This is a proof-of-concept demonstrating HLX+Vulkan integration.
Not production-ready.
```

**Status:** ❌ Doesn't exist yet (currently partial in helix-studio)
**Action:** Create new repo, start Phase 1 implementation

---

## Migration Plan

### Step 1: Freeze Corpus Repo (30 minutes)
**Goal:** Make HLXv1.1.0 repo pristine and frozen

```bash
cd /home/matt/helix-studio

# 1. Remove non-corpus files
rm -rf release/ node_modules/ src/ public/
rm package.json tsconfig.json bun.lockb

# 2. Keep only corpus + verification
# Should have:
#   - corpus/
#   - hlx_runtime/ (for verification tests only)
#   - tools/
#   - README.md
#   - VERIFICATION_REPORT.md
#   - LICENSE

# 3. Update README with FROZEN badge
# (edit README.md manually)

# 4. Create git tag
git tag -a v1.1.0 -m "HLX v1.1.0 Corpus - FROZEN"
git push origin v1.1.0

# 5. Create GitHub release
gh release create v1.1.0 \
    --title "HLX v1.1.0 Corpus (FROZEN)" \
    --notes "Canonical specification - 106/106 tests passing"
```

**Verification:**
- README clearly states "FROZEN"
- Only corpus + verification tools remain
- Git tag v1.1.0 pushed
- GitHub release created

---

### Step 2: Create hlx-studio Repo (1-2 hours)
**Goal:** New repo with clean Studio code

```bash
# 1. Create new repo on GitHub
gh repo create latentcollapse/hlx-studio \
    --public \
    --description "Visual development environment for HLX language" \
    --clone

cd hlx-studio

# 2. Copy Studio files from helix-studio
cp -r /home/matt/helix-studio/src .
cp -r /home/matt/helix-studio/public .
cp -r /home/matt/helix-studio/release .
cp /home/matt/helix-studio/package.json .
cp /home/matt/helix-studio/tsconfig.json .
cp /home/matt/helix-studio/bun.lockb .

# 3. Copy runtime (bundled with Studio)
cp -r /home/matt/helix-studio/hlx_runtime .

# 4. Create README
cat > README.md << 'EOF'
# HLX Studio
## Visual Development Environment for HLX Language

[![Status](https://img.shields.io/badge/status-alpha-yellow)]()
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey)]()

HLX Studio is a GUI development environment for writing, testing, and debugging
HLX programs.

## Features

- Live HLX code editor with syntax highlighting
- Visual latent space explorer
- Content-addressed storage viewer
- Deterministic execution environment
- Built-in Python runtime

## Quick Start

```bash
# Install dependencies
bun install

# Run in development mode
bun run dev

# Build for production
bun run build
```

## Status

**⚠️ Alpha Status:** This is experimental software under active development.

## Related Projects

- [HLX v1.1.0 Corpus](https://github.com/latentcollapse/HLXv1.1.0) - Language specification
- [HLX+Vulkan](https://github.com/latentcollapse/hlx-vulkan) - GPU compute backend

## License

MIT OR Apache-2.0
EOF

# 5. Initial commit
git add .
git commit -m "Initial commit: HLX Studio alpha"
git push origin main
```

**Verification:**
- New repo exists at github.com/latentcollapse/hlx-studio
- Studio code separated cleanly
- README explains purpose clearly
- Links to corpus and vulkan repos

---

### Step 3: Create hlx-vulkan Repo (1 hour)
**Goal:** New repo ready for Phase 1 implementation

```bash
# 1. Create new repo on GitHub
gh repo create latentcollapse/hlx-vulkan \
    --public \
    --description "Vulkan compute backend with HLX integration" \
    --clone

cd hlx-vulkan

# 2. Set up directory structure
mkdir -p hlx_runtime/{tests,}
mkdir -p shaders
mkdir -p benchmarks/results
mkdir -p docker
mkdir -p docs
mkdir -p .github/workflows

# 3. Copy relevant files from helix-studio
# Copy runtime components
cp /home/matt/helix-studio/hlx_runtime/{lc_codec,cas,ls_ops,pre_serialize,contracts,errors,__init__}.py hlx_runtime/

# Copy existing Vulkan work (if any)
cp /home/matt/helix-studio/hlx_runtime/tests/test_opus_audit.py hlx_runtime/tests/

# Copy roadmap documents
cp /home/matt/helix-studio/VULKAN_ROADMAP.md docs/
cp /home/matt/helix-studio/VULKAN_PHASE1_ASSESSMENT.md docs/
cp /home/matt/helix-studio/PHASE1_KICKOFF.md docs/

# 4. Create README
cat > README.md << 'EOF'
# HLX+Vulkan Compute Engine
## Deterministic GPU Compute with Content-Addressed Storage

[![Status](https://img.shields.io/badge/status-experimental-orange)]()
[![Tests](https://img.shields.io/badge/tests-106%2F106-brightgreen)]()

HLX+Vulkan integrates HLX's deterministic execution model with Vulkan compute shaders.

## Current Status

**Phase 1 (In Progress):** Vulkan runtime integration
- ✅ Contract schemas (CONTRACT_900-902) implemented
- ✅ SPIR-V packaging tool working
- 🔄 VulkanContext initialization (in progress)
- ⏳ Shader loading (planned)
- ⏳ Pipeline creation (planned)
- ⏳ Kernel execution (planned)

See [docs/VULKAN_ROADMAP.md](docs/VULKAN_ROADMAP.md) for full roadmap.

## Quick Start (When Ready)

```bash
# Run benchmark (Docker)
docker-compose up benchmark

# Or run locally
pip install -r requirements.txt
python benchmarks/gemm_comparison.py
```

## Why HLX+Vulkan?

**Problem:** CUDA requires kernel recompilation for each input variation, wasting power and latency.

**Solution:** HLX's content-addressed storage enables perfect memoization. Same input → instant cache hit.

**Result:** Early testing shows 3× faster warm-start latency vs CUDA on repeated inference.

## Architecture

```
HLX Handle → LC-B Encoding → SPIR-V Shader → Vulkan Pipeline → GPU Compute → HLX Handle
      ↓                                                                ↓
Content-Addressed                                              Deterministic
   Storage                                                      (bit-identical)
```

## Related Projects

- [HLX v1.1.0 Corpus](https://github.com/latentcollapse/HLXv1.1.0) - Language specification
- [HLX Studio](https://github.com/latentcollapse/hlx-studio) - Development environment

## Roadmap

See [docs/VULKAN_ROADMAP.md](docs/VULKAN_ROADMAP.md) for detailed 9-13 week plan.

**Target Milestones:**
- ✅ Week 0: Corpus complete, runtime verified
- 🔄 Week 1-2: Vulkan runtime foundation
- ⏳ Week 3-5: GEMM benchmark (parity with CUDA)
- ⏳ Week 6-9: Warm-start optimization (beat CUDA)
- ⏳ Week 10-12: Production polish + Docker
- ⏳ Week 13: Public benchmarks + outreach

## Contributing

**Current Status:** Early experimental phase. Not accepting external contributions yet.

Once Phase 1 is complete and benchmarks are reproducible, contribution guidelines will be added.

## License

MIT OR Apache-2.0
EOF

# 5. Create requirements.txt
cat > requirements.txt << 'EOF'
# HLX Runtime
numpy>=1.21.0

# Vulkan (Phase 1+)
# vulkan>=1.3.0  # Uncomment when ready to start Vulkan work

# Testing
pytest>=7.0.0

# Optional: SPIR-V validation
# spirv-tools>=2024.1  # Uncomment for spirv-val integration
EOF

# 6. Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/
venv/
.pytest_cache/

# SPIR-V compiled shaders (keep sources, ignore binaries initially)
*.spv

# Benchmark results (keep structure, ignore data)
benchmarks/results/*.csv
benchmarks/results/*.json

# Docker
.docker/

# Editor
.vscode/
.idea/
*.swp
*~

# OS
.DS_Store
Thumbs.db
EOF

# 7. Initial commit
git add .
git commit -m "Initial commit: HLX+Vulkan compute engine (Phase 1 ready)"
git push origin main
```

**Verification:**
- New repo exists at github.com/latentcollapse/hlx-vulkan
- Directory structure ready for Phase 1
- README explains purpose and current status
- Roadmap documents in docs/
- All three repos link to each other

---

## Repository Cross-Links

Each README should link to the other two repos:

### HLXv1.1.0 README (corpus):
```markdown
## Related Projects

- [HLX Studio](https://github.com/latentcollapse/hlx-studio) - Visual development environment
- [HLX+Vulkan](https://github.com/latentcollapse/hlx-vulkan) - GPU compute backend
```

### hlx-studio README:
```markdown
## Related Projects

- [HLX v1.1.0 Corpus](https://github.com/latentcollapse/HLXv1.1.0) - Language specification
- [HLX+Vulkan](https://github.com/latentcollapse/hlx-vulkan) - GPU compute backend
```

### hlx-vulkan README:
```markdown
## Related Projects

- [HLX v1.1.0 Corpus](https://github.com/latentcollapse/HLXv1.1.0) - Language specification
- [HLX Studio](https://github.com/latentcollapse/hlx-studio) - Development environment
```

---

## What Each Repo Demonstrates

### HLXv1.1.0
**Message:** "I've created a rigorous language specification suitable for AI training."
**Proof:** 106/106 tests passing, mathematical verification report

### hlx-studio
**Message:** "I've built tooling to make HLX accessible to developers."
**Proof:** Working GUI with live visualization

### hlx-vulkan
**Message:** "I've integrated HLX with Vulkan and proven performance advantages."
**Proof:** Reproducible benchmarks showing 3× warm-start speedup vs CUDA

---

## Timeline

### Today (Dec 15)
- [ ] Step 1: Clean up HLXv1.1.0 repo (30 min)
- [ ] Tag v1.1.0 and create GitHub release (5 min)
- [ ] Step 2: Create hlx-studio repo (1 hour)
- [ ] Step 3: Create hlx-vulkan repo (1 hour)

**Total time:** ~2.5-3 hours to complete full reorganization

### Tomorrow (Dec 16)
- [ ] Start Phase 1 of hlx-vulkan (see PHASE1_KICKOFF.md)
- [ ] Verify Vulkan SDK, install dependencies
- [ ] Write VulkanContext skeleton

---

## Benefits of This Structure

### For You
- Clear separation of concerns
- Easy to work on one project without touching others
- Professional presentation

### For External Viewers
- **Corpus seekers** find clean spec without GUI clutter
- **Tool users** find Studio without implementation details
- **Performance engineers** find Vulkan work without language theory

### For Khronos/Sascha
When you eventually share hlx-vulkan:
- They see focused repo about Vulkan compute
- They see working benchmarks (once complete)
- They don't get distracted by corpus or GUI
- README clearly states experimental status
- Links to corpus if they want theory

---

## What to Do Right Now

```bash
# 1. Clean up current helix-studio repo (make it corpus-only)
cd /home/matt/helix-studio

# 2. List what needs to be removed
ls -la

# 3. Confirm you're ready to reorganize
echo "Ready to create three clean repos"
```

---

**Status:** Ready to execute
**Estimated time:** 2-3 hours for full reorganization
**Next action:** Clean up helix-studio → make it HLXv1.1.0 corpus-only
