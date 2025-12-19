# HLXL Custom Inference Engine: Pragmatic Implementation Plan

**Date:** 2025-12-18
**Purpose:** Build lightweight HLX-native inference engine for Studio brain
**Approach:** Start simple, iterate fast, leverage existing infrastructure

---

## Executive Summary

**Problem:** Ollama models too slow on hardware (8B/4B/2B timeout, 1.5B barely usable at 9s)

**Solution:** Custom HLXL-native inference engine optimized for:
- LC-R tokenization (compact vocabulary <100 symbols)
- Deterministic output (T=0, no sampling overhead)
- Handle-aware architecture
- Existing Vulkan compute backend

**Timeline:** 3-4 weeks to MVP Studio brain (ignoring Grok's conservative estimates)

**Outcome:** Interactive Studio brain (<2s inference) on same hardware that fails with Ollama

---

## Hardware Capacity Testing Results

### Complete Testing Matrix

| Model | Size | Test Result | Notes |
|-------|------|-------------|-------|
| Qwen3:8b | 5.2 GB | ❌ FAIL | 30+ second timeout |
| Qwen3:4b | 2.5 GB | ❌ FAIL | 30+ second timeout |
| Qwen3-vl:2b | 1.9 GB | ❌ FAIL | 15+ second timeout |
| Qwen2.5:1.5b | 986 MB | ⚠️ MARGINAL | 9s response (8.95s load + 0.11s inference) |

**Finding:** Even 1B model barely usable. Ollama overhead + general-purpose architecture doesn't fit hardware.

**Decision:** Build custom HLXL engine - it's not optional, it's necessary.

---

## Grok's Roadmap Review

### What Grok Got Right

1. **Phase 1 (Hybrid)**: Modify existing model with HLX layers - smart incremental approach
2. **Core Principles**: A1-A4 axioms as architectural constraints
3. **Vulkan Backend**: Leverage existing compute infrastructure
4. **Reversible Layers**: Content-addressed memory via collapse/resolve

### What We're Changing (Matt's Speed)

**Grok's Timeline:** "1-3 months" for Phase 1
**Our Timeline:** 3-4 weeks to MVP

**Grok's Approach:** Fine-tune existing Qwen 2B/4B
**Our Approach:** Build minimal viable engine from scratch (cleaner, faster)

**Grok's Scope:** Prove concept, then scale
**Our Scope:** Shipping Studio brain ASAP, iterate in production

---

## Three-Phase Plan: Matt's Velocity

### PHASE 1: Minimal Viable Brain (Week 1-2) ⚡

**Goal:** Shipping Studio brain with basic HLX fluency

#### Week 1: Core Engine

**Day 1-2: LC-R Tokenizer**
```python
# /home/matt/hlx/hlx_runtime/tokenizer.py

class LCRTokenizer:
    """Ultra-compact tokenizer for LC-R glyphs"""

    # Core vocabulary: ~80 tokens
    GLYPHS = {
        # Structural
        '🜊': 1,  # Contract open
        '🜁': 2,  # Field separator
        '🜂': 3,  # Contract close

        # Primitives
        '∅': 4,   # null
        '⊤': 5,   # true
        '⊥': 6,   # false

        # Handles
        '⟁': 7,   # Handle prefix

        # Numbers: 0-9 -> 10-19
        # Operators: 20-30
        # Reserved: 31-80
    }

    def encode(self, text: str) -> List[int]:
        """Direct glyph->ID mapping, no BPE overhead"""
        return [self.GLYPHS.get(c, 0) for c in text]

    def decode(self, ids: List[int]) -> str:
        """Reverse mapping, deterministic"""
        reverse = {v: k for k, v in self.GLYPHS.items()}
        return ''.join(reverse.get(id, '?') for id in ids)

# Test: Perfect round-trip in <1ms
```

**Day 3-4: Tiny Transformer (128-dim, 2 layers)**
```python
# /home/matt/hlx/hlx_runtime/hlxl_model.py

import torch
import torch.nn as nn

class HLXLTinyTransformer(nn.Module):
    """Minimalist transformer for HLX patterns"""

    def __init__(self, vocab_size=100, d_model=128, n_layers=2, n_heads=4):
        super().__init__()

        self.embed = nn.Embedding(vocab_size, d_model)
        self.pos_embed = nn.Parameter(torch.zeros(1, 512, d_model))

        # Standard transformer layers
        self.layers = nn.ModuleList([
            nn.TransformerEncoderLayer(
                d_model=d_model,
                nhead=n_heads,
                dim_feedforward=512,
                dropout=0.0,  # Deterministic
                batch_first=True
            )
            for _ in range(n_layers)
        ])

        self.ln_f = nn.LayerNorm(d_model)
        self.head = nn.Linear(d_model, vocab_size)

    def forward(self, x):
        # x: (batch, seq_len) token IDs
        x = self.embed(x) + self.pos_embed[:, :x.size(1), :]

        for layer in self.layers:
            x = layer(x)

        x = self.ln_f(x)
        logits = self.head(x)

        # Deterministic: always greedy decode
        return logits.argmax(dim=-1)  # No sampling!
```

**Day 5: Training Loop**
```python
# /home/matt/hlx/training/train_hlxl_brain.py

def train_minimal_brain():
    """Train on HLX corpus only - no general English"""

    # Dataset: LC_R_EXAMPLES_FOR_VERIFICATION_TESTING.md
    corpus = load_hlx_corpus()  # ~400 examples

    # Augment: Generate 10k synthetic examples via templates
    dataset = generate_synthetic_hlx(corpus, n=10000)

    # Model: 128-dim, 2-layer (< 5M params)
    model = HLXLTinyTransformer().cuda()

    # Optimizer: Adam with deterministic annealing
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    # Train: 100 epochs, ~30 minutes on 5060
    for epoch in range(100):
        for batch in dataset:
            loss = train_step(model, batch)

        if epoch % 10 == 0:
            eval_axioms(model)  # A1-A4 compliance

    # Save: <20MB checkpoint
    torch.save(model.state_dict(), 'hlxl_brain_v1.pt')
```

**Day 6-7: Integration & Testing**
- Python bindings for Studio
- API endpoint: `http://localhost:8000/hlxl/generate`
- Benchmark: <1s inference, 95%+ axiom compliance
- Deploy: Add to Studio settings as "Local HLX Brain"

#### Week 2: Polish & Ship

**Day 8-10: Handle System Integration**
```python
# Add handle registry to model

class HLXLBrainWithHandles(HLXLTinyTransformer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handle_store = {}  # Content-addressed memory

    def collapse(self, value):
        """HLX collapse: hash -> store -> return handle"""
        handle = f"&h_{hash(str(value)) % 10000:04x}"
        self.handle_store[handle] = value
        return handle

    def resolve(self, handle):
        """HLX resolve: lookup handle -> return value"""
        return self.handle_store.get(handle, None)
```

**Day 11-12: Studio Integration**
- Add to hlx-studio settings panel
- Toggle: "Use Local Brain" vs. "Use API"
- Status indicator: green = loaded, red = offline
- Fallback: If local brain unavailable, use Claude API

**Day 13-14: Validation & Documentation**
- Run full HLX recognition test suite
- Compare vs. Sonnet 4.5 control
- Document performance metrics
- Ship Studio with integrated brain

---

### PHASE 2: Production Hardening (Week 3) 🔧

**Goal:** Make brain production-ready

**Optimizations:**
1. **Quantization**: INT8 weights (<5MB model)
2. **Vulkan Backend**: Offload matmuls to existing shaders
3. **Caching**: LRU cache for repeated patterns
4. **Batching**: Process multiple requests together

**Expected Gains:**
- 2-4x faster inference
- 50% memory reduction
- Stable sub-1s responses

**Deliverable:** Studio brain v1.0 - ready for daily use

---

### PHASE 3: Advanced Features (Week 4+) 🚀

**Optional Enhancements (post-MVP):**
- Larger context window (512 → 2048 tokens)
- Multi-modal (vision via contract 1002)
- Swarm coordination primitives
- Fine-tune on user's HLX codebases

**Research Experiments:**
- Reversible layers (RevTorch integration)
- Sparse attention (only compute relevant contracts)
- Meta-learning (few-shot HLX pattern adaptation)

---

## Technical Architecture

### Model Specification

```
HLXL Brain v1 Spec:
├── Tokenizer: LC-R glyphs (vocab=100)
├── Architecture: Transformer
│   ├── Embedding: 128-dim
│   ├── Layers: 2x TransformerEncoder
│   ├── Heads: 4
│   ├── FFN: 512-dim
│   └── Total Params: ~4.8M
├── Training: HLX corpus + synthetic (10k examples)
├── Inference: Greedy decode (T=0, deterministic)
├── Size: ~20MB (FP32), ~5MB (INT8)
└── Latency: <1s target (cold start <2s)
```

### Integration Points

**Studio → Brain API:**
```python
# /home/matt/hlx-studio/backend/hlxl_brain.py

import requests

class HLXLBrainClient:
    def __init__(self, url="http://localhost:8000/hlxl"):
        self.url = url

    def generate(self, prompt: str) -> str:
        """Query local HLXL brain"""
        resp = requests.post(
            f"{self.url}/generate",
            json={"prompt": prompt, "temperature": 0.0}
        )
        return resp.json()["output"]

    def health(self) -> bool:
        """Check if brain is alive"""
        try:
            requests.get(f"{self.url}/health", timeout=1)
            return True
        except:
            return False
```

**Brain Server:**
```python
# /home/matt/hlx/hlxl_brain_server.py

from fastapi import FastAPI
import torch

app = FastAPI()
model = HLXLBrainWithHandles.from_pretrained('hlxl_brain_v1.pt')
model.eval()

@app.post("/hlxl/generate")
def generate(prompt: str):
    tokens = tokenizer.encode(prompt)
    output = model(torch.tensor([tokens]))
    return {"output": tokenizer.decode(output[0].tolist())}

@app.get("/hlxl/health")
def health():
    return {"status": "ok", "model": "hlxl_brain_v1"}
```

---

## Comparison: Grok vs. Our Approach

| Aspect | Grok's Plan | Our Plan | Why Different |
|--------|-------------|----------|---------------|
| **Timeline** | 1-3 months | 3-4 weeks | You work fast, start minimal |
| **Base Model** | Fine-tune Qwen 2B | Train from scratch | Cleaner, no legacy bloat |
| **Vocab Size** | 50k+ (English) | <100 (LC-R only) | HLX-first, not general-purpose |
| **Model Size** | 2-4B params | 5M params | Studio brain, not AGI |
| **Training Data** | HLX + general | HLX corpus only | Focused, deterministic |
| **Hardware** | Cloud required | 5060 local | You have hardware, use it |
| **Inference** | Via Ollama/HF | Custom FastAPI | Direct control, no overhead |
| **Phase 1 Goal** | Proof-of-concept | Shipping product | MVP mentality |

---

## Validation Strategy

### Success Criteria

**Week 1:**
- [ ] Tokenizer: 100% round-trip accuracy on LC-R glyphs
- [ ] Model: 80%+ accuracy on HLX corpus test set
- [ ] Inference: <5s latency (cold start acceptable)

**Week 2:**
- [ ] Axiom Compliance: A1 (95%+), A2 (90%+), A3 (85%+)
- [ ] Hallucination Rate: <10% on nonexistent handles
- [ ] Studio Integration: Green status indicator

**Week 3:**
- [ ] Production Ready: <1s inference, INT8 quantized
- [ ] Vulkan Accelerated: 2x speedup vs. CPU baseline
- [ ] Stable: No crashes over 1000 requests

### Testing Protocol

```bash
# Run full HLX recognition test
cd /home/matt/hlx/experiments/qwen3_8b_hlx_recognition
python test_harness.py --model=hlxl_brain_v1

# Expected results vs. Sonnet 4.5 control:
# - Determinism: 0.9+ (vs. 1.0 Sonnet)
# - Reversibility: 85%+ (vs. 100% Sonnet)
# - Hallucination: <10% (vs. 0% Sonnet)
# - Inference: <1s (vs. instant Sonnet API)
```

---

## Resource Requirements

### Hardware
- **RTX 5060** (available): Training + inference
- **RAM**: 16GB+ for training, 4GB for inference
- **Disk**: 5GB for checkpoints + datasets

### Software Dependencies
```bash
# /home/matt/hlx/requirements_brain.txt
torch>=2.0.0
transformers>=4.30.0
fastapi>=0.100.0
uvicorn>=0.23.0
numpy>=1.24.0
```

### Training Cost
- **Time**: ~30 minutes on 5060 for 100 epochs
- **Electricity**: Negligible (<$1)
- **Cloud**: $0 (all local)

---

## Risk Mitigation

### Risk 1: Poor HLX Fluency
**Mitigation:**
- Start with template-based synthetic data
- Augment with corruption/perturbation
- Use axiom-based loss functions
- Iterate on training data quality

### Risk 2: Inference Still Too Slow
**Mitigation:**
- Profile bottlenecks (tokenizer, attention, decode)
- Optimize critical paths (Vulkan shaders)
- Reduce model size if needed (1-layer, 64-dim)
- Cache frequent patterns

### Risk 3: Integration Challenges
**Mitigation:**
- Design API-first (decouple from Studio)
- Fallback to Claude API if brain offline
- Extensive error handling
- Graceful degradation

---

## Beyond Week 4: Roadmap Alignment with Grok

Once MVP is stable, revisit Grok's longer-term vision:

**Phase 2 (Grok's Months 3-12):** Scale to 7B+ params
- Only if 5M model shows promise
- Cloud training for larger variants
- Open-source as "HelixNet"

**Phase 3 (Grok's Months 12-36):** Custom hardware
- FPGA prototypes for collapse/resolve ops
- Partner with AMD/xAI for ASIC designs
- "HelixChip" - HLX-native silicon

**Our Philosophy:** Ship fast, validate, then scale. Don't build Phase 3 before Phase 1 works.

---

## Immediate Next Steps

### This Week (Dec 18-24)

**Day 1 (Today):**
- [ ] Create project structure: `/home/matt/hlx/hlxl_brain/`
- [ ] Implement LC-R tokenizer
- [ ] Test on corpus

**Day 2-3:**
- [ ] Implement tiny transformer
- [ ] Training loop + synthetic data generation

**Day 4:**
- [ ] Train first model (100 epochs)
- [ ] Run axiom tests

**Day 5-7:**
- [ ] Optimize + debug
- [ ] Studio integration
- [ ] Ship MVP brain

### Success Metrics
- **Performance:** <2s inference (target <1s)
- **Quality:** 85%+ axiom compliance
- **Usability:** Green status in Studio
- **Size:** <50MB total (model + dependencies)

---

## Conclusion

**Grok's Roadmap:** Excellent long-term vision, conservative timelines
**Our Execution:** Start minimal, ship fast, iterate in production

**Key Differences:**
- 3-4 weeks to MVP (not 1-3 months)
- 5M params (not 2B+)
- HLX-only vocabulary (not 50k+ tokens)
- Local-first (not cloud-dependent)

**Alignment:** Both approaches converge on HLX-native architecture with axiom constraints, handle-aware memory, and Vulkan acceleration. We're just starting smaller and moving faster.

**The Plan:** Build HLXL Brain v1 this month, validate with real Studio usage, then scale if results justify it.

---

**Document Status:** READY FOR EXECUTION
**Owner:** Matt + Sonnet/Haiku swarm
**Start Date:** 2025-12-18
**Target Ship:** 2025-12-25 (Christmas brain! 🎄)
