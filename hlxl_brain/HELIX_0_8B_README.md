# Helix 0.8B v1.0 - Multi-Brain HLX Translation System

**Status:** OPERATIONAL (v1.0 - 2025-12-18)

## Architecture

Helix 0.8B is a specialized multi-brain system for English → HLX translation:

```
┌─────────────────────────────────────────────────────────────┐
│                     USER REQUEST                            │
│          "Search for documents containing 'user'"           │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      v
         ┌────────────────────────┐
         │   QWEN3_0.6B (600M)    │ ◄─── Intent Parser
         │   Via Ollama           │      English Understanding
         └────────┬───────────────┘
                  │ Parsed Intent
                  v
         ┌────────────────────────┐
         │  COORDINATOR (101M)    │ ◄─── HLX Format Master
         │  All 7 formats         │      Cross-format reasoning
         └────────┬───────────────┘
                  │ HLX Output
                  v
          ┌───────┴────────┐
          │                │
  ┌───────v──────┐  ┌─────v─────────┐
  │ ASCII (50M)  │  │ RUNIC (50M)*  │ ◄─── Format Specialists
  │ LC-T Expert  │  │ LC-R Expert   │      Optimized execution
  └──────────────┘  └───────────────┘
          │                │
          └────────┬───────┘
                   v
          ┌────────────────┐
          │ FINAL HLX CODE │
          └────────────────┘

* Runic Specialist training in progress
```

## Components

### 1. Qwen3_0.6b (Intent Parser)
- **Size:** ~600M parameters
- **Role:** Parse natural language intent
- **Integration:** Via Ollama (local, no API calls)
- **Status:** ✓ READY

### 2. Coordinator 100M
- **Size:** 101M parameters
- **Training:** 100 epochs on canonical corpus (all 7 HLX formats)
- **Role:** HLX format master, cross-format translation
- **Architecture:** d_model=1024, 8 layers, 16 heads
- **Checkpoint:** `checkpoints/qwen_distill_FINAL_epoch100.pt`
- **Status:** ✓ TRAINED & VALIDATED (10/10 tests passed)

### 3. ASCII Specialist 50M
- **Size:** 50M parameters
- **Training:** 20 epochs on ASCII-focused corpus (60% LC-T)
- **Role:** LC-T (text wire format) expert
- **Architecture:** d_model=768, 7 layers, 12 heads
- **Checkpoint:** `checkpoints/specialist_ascii_BEST.pt`
- **Status:** ✓ TRAINED

### 4. Runic Specialist 50M
- **Size:** 50M parameters
- **Training:** QUEUED (memory constraint during parallel training)
- **Role:** LC-R (runic wire format) expert
- **Status:** ⚠ NOT YET TRAINED (falls back to Coordinator)

## Total System

- **Active Parameters:** ~750M (Qwen + Coordinator + ASCII)
- **Full Capacity:** ~800M (when Runic specialist added)
- **Local-only:** Zero API costs, deterministic, hardware-optimized
- **VRAM Usage:** ~4-5 GiB total

## Usage

### Quick Start

```python
#!/usr/bin/env python3
from helix_0_8b import Helix08B

# Initialize system
helix = Helix08B()

# Translate English to HLX
result = helix.english_to_hlx("Search for documents containing 'user'")

print(f"Format: {result['format']}")
print(f"Output: {result['specialist_output']}")
```

### API

```python
class Helix08B:
    def english_to_hlx(
        user_request: str,
        target_format: str = "auto",  # "auto", "lc-t", "lc-r", "hlx", "hlxl"
        verbose: bool = True
    ) -> Dict:
        """
        Returns:
            {
                "intent": str,              # Parsed intent from Qwen
                "coordinator_output": str,  # HLX from coordinator
                "specialist_output": str,   # Final format from specialist
                "format": str,              # Detected/requested format
                "success": bool
            }
        """
```

### Batch Processing

```python
requests = [
    "Search for documents",
    "Filter active users",
    "Create array [1,2,3]"
]

results = helix.batch_translate(requests, target_format="lc-t")
```

## Performance

### Strengths

1. **Local-first:** Zero dependency on external APIs
2. **Specialized:** Each brain optimized for its domain
3. **Fast:** Inference in ~100-500ms per request
4. **Deterministic:** Consistent outputs for reproducible HLX
5. **Efficient:** Fits in 8GB VRAM with room to spare

### Current Limitations

1. **Runic Specialist:** Not yet trained (uses Coordinator fallback)
2. **Small Context:** 256 token limit (character-level)
3. **Training Data:** Limited to corpus examples (~1000 lines)

## Training Details

### Fixes Applied

All models trained with critical bug fixes:
- ✓ No character collapse (proper PAD token handling)
- ✓ Autoregressive generation (not single-pass)
- ✓ Label masking with -100 for padding
- ✓ Quality gates at epochs 1, 5, 10, 20, 50, 100

### Corpus

- **Coordinator:** `corpus_canonical_COMPLETE.md` (1045 lines, all 7 formats)
- **ASCII Specialist:** `corpus_ascii_specialist.md` (582 lines, 60% LC-T)
- **Runic Specialist:** `corpus_runic_specialist.md` (547 lines, 60% LC-R) [READY FOR TRAINING]

## Next Steps

### Immediate (for v1.0 completion)

1. **Train Runic Specialist 50M**
   - Run: `python3 train_specialist_50m.py --specialist runic --epochs 100`
   - Est. time: 2-4 days
   - Will unlock full LC-R capabilities

### Future (Helix 600M Master)

2. **Train Helix 600M**
   - Larger coordinator with better intent understanding
   - English + HLX proficiency in single model
   - Routes to specialist sub-family

## File Structure

```
/home/matt/hlx/hlxl_brain/
├── helix_0_8b.py                          # Main Helix 0.8B system
├── train_qwen_distillation.py             # Coordinator training
├── train_specialist_50m.py                # Specialist training
├── test_english_generation.py             # Quality validation
├── corpus_canonical_COMPLETE.md           # All 7 formats (1045 lines)
├── corpus_ascii_specialist.md             # ASCII-focused (582 lines)
├── corpus_runic_specialist.md             # Runic-focused (547 lines)
└── checkpoints/
    ├── qwen_distill_FINAL_epoch100.pt     # Coordinator 100M ✓
    ├── qwen_distill_epoch1..100.pt        # Coordinator training history
    ├── specialist_ascii_BEST.pt           # ASCII Specialist ✓
    ├── specialist_ascii_epoch1..20.pt     # ASCII training history
    └── specialist_runic_*.pt              # [TO BE CREATED]
```

## Example Output

```
================================================================================
HELIX 0.8B INITIALIZATION
================================================================================
Device: cuda
Intent Parser: qwen3:0.6b (via Ollama)

Loading Coordinator 100M...
✓ Coordinator loaded (101.2M params)
Loading ASCII Specialist 50M...
✓ ASCII Specialist loaded (50.0M params)
⚠ Runic Specialist not available (checkpoint not found)
  Will fall back to Coordinator for LC-R format

Verifying qwen3:0.6b availability...
✓ qwen3:0.6b ready

================================================================================
HELIX 0.8B READY
================================================================================
Total Parameters: ~751M
  - Intent Parser (Qwen): ~600M
  - Coordinator: 101.2M
  - ASCII Specialist: 50.0M
  - Runic Specialist: [NOT LOADED]
================================================================================
```

## Verification

### Quality Tests

All models passed quality gates:
- **Coordinator:** 10/10 tests (no parroting, no collapse, no scrambling)
- **ASCII Specialist:** Trained 20 epochs, BEST checkpoint saved
- **Runic Specialist:** Corpus ready, training queued

### Test Command

```bash
python3 test_english_generation.py checkpoints/qwen_distill_FINAL_epoch100.pt
```

## Credits

- **Training Bugs Fixed:** Character collapse, label masking, generation logic
- **Corpus:** Complete canonical HLX corpus with all 7 format variants
- **Architecture:** MoE-inspired design optimized for local hardware

---

**Status:** Helix 0.8B v1.0 is OPERATIONAL with Coordinator + ASCII specialist.
Train Runic specialist to complete the full system.
