# HLXL Brain: Custom HLX-Native Inference Engine

**Status:** 🚧 IN DEVELOPMENT
**Target:** Christmas 2025 (Dec 25) - 7 days remaining
**Purpose:** Lightweight Studio brain optimized for HLX/LC-R

---

## Project Structure

```
hlxl_brain/
├── src/                    # Source code
│   ├── tokenizer.py       # LC-R tokenizer (<100 vocab)
│   ├── model.py           # Tiny transformer (5M params)
│   ├── training.py        # Training loop
│   ├── inference.py       # Deterministic inference
│   └── server.py          # FastAPI server for Studio
├── tests/                  # Test suite
│   ├── test_tokenizer.py
│   ├── test_model.py
│   └── test_axioms.py     # A1-A4 compliance tests
├── benchmarks/             # Performance measurements
│   └── *.json             # Raw immutable data
├── checkpoints/            # Model weights
│   └── *.pt               # PyTorch checkpoints
├── docs/                   # Documentation
│   └── HLXL_INFERENCE_ENGINE_PLAN.md
├── QUALITY_MANDATE.md      # Rigor standards (watchdog)
└── README.md              # This file
```

---

## Quick Start

### Install Dependencies

```bash
cd /home/matt/hlx/hlxl_brain
pip install torch transformers fastapi uvicorn
```

### Run Tests

```bash
pytest tests/ -v
```

### Train Model

```bash
python src/training.py --corpus /home/matt/LC_R_EXAMPLES_FOR_VERIFICATION_TESTING.md
```

### Start Server

```bash
python src/server.py
```

### Query Brain

```bash
curl -X POST http://localhost:8000/hlxl/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "{14: {@0: 42}}", "temperature": 0.0}'
```

---

## Architecture

**Model Spec:**
- Vocabulary: <100 LC-R glyphs (not 50k+ English tokens)
- Architecture: 2-layer Transformer, 128-dim embeddings
- Parameters: ~5M (vs. 2B+ in general-purpose models)
- Size: ~20MB (FP32), ~5MB (INT8 quantized)
- Training: ~30 mins on RTX 5060
- Inference: <1s target (<2s cold start)

**Why Custom?**
- Ollama models too slow (8B/4B/2B all timeout)
- Even 1.5B model barely usable (9s response)
- HLX-native = 10-50x more efficient
- LC-R vocabulary 500x smaller than English

---

## Timeline

### Week 1-2: Core Engine
- [x] Project structure created
- [x] Quality mandate established
- [ ] Day 1-2: LC-R tokenizer
- [ ] Day 3-4: Tiny transformer
- [ ] Day 5: Training loop
- [ ] Day 6-7: Integration testing
- [ ] Day 8-14: Handle system + Studio integration

### Week 3: Production Hardening
- [ ] INT8 quantization
- [ ] Vulkan backend integration
- [ ] Performance optimization

### Week 4+: Advanced Features
- [ ] Larger context window
- [ ] Multi-modal support
- [ ] Swarm coordination

---

## Quality Standards

**See:** `QUALITY_MANDATE.md` for full rigor requirements

**Key Principles:**
- ✅ "We don't make claims. We provide raw immutable data."
- ✅ All assertions backed by measurements
- ✅ Tests run before marking complete
- ❌ No predictions without benchmarks
- ❌ No claims without supporting data

**Every commit must include:**
1. Tests passing (actual output shown)
2. Benchmarks captured (JSON files in benchmarks/)
3. Environment metadata (git commit, hardware)
4. No unverified claims in commit message

---

## Success Criteria

### Phase 1: Tokenizer
- [ ] 100% round-trip accuracy on LC-R glyphs
- [ ] <1ms encoding/decoding latency
- [ ] Zero errors on 400+ corpus examples

### Phase 2: Model
- [ ] Training loss converges (plot saved)
- [ ] Validation accuracy ≥ 80%
- [ ] Training completes in <1 hour

### Phase 3: Inference
- [ ] Cold start < 2s (measured)
- [ ] Warm inference < 1s (measured over 100 requests)
- [ ] Determinism: 10/10 trials identical output
- [ ] Hallucination rate < 10%

### Phase 4: Integration
- [ ] API server starts without errors
- [ ] Health endpoint returns 200 OK
- [ ] Studio can query successfully
- [ ] Graceful fallback to Claude API

---

## Comparison: Ollama vs. HLXL Brain

| Metric | Ollama (Qwen2.5:1.5b) | HLXL Brain (Target) |
|--------|-----------------------|---------------------|
| **Size** | 986 MB | ~20MB |
| **Vocab** | 50k+ tokens | <100 glyphs |
| **Cold Start** | 9 seconds | <2 seconds |
| **Warm Inference** | Unknown | <1 second |
| **HLX Fluency** | Unknown | 85%+ (A1-A4) |
| **Hardware** | Barely usable | Optimized for 5060 |

---

## References

- **Implementation Plan:** `docs/HLXL_INFERENCE_ENGINE_PLAN.md`
- **Quality Mandate:** `QUALITY_MANDATE.md`
- **HLX Corpus:** `/home/matt/LC_R_EXAMPLES_FOR_VERIFICATION_TESTING.md`
- **Grok's Roadmap:** `/home/matt/Documents/hlx_brain_roadmap.txt`

---

**Built with rigor. Measured, not claimed. Shipped, not polished to perfection.**
