# Opus Training Failure Report
**Date:** 2025-12-18
**Agent:** d20661c9 (Opus 4.1)
**Status:** Complete failure across all model sizes

---

## Executive Summary

Opus agent d20661c9 was tasked with training a 1B parameter HLX Brain model overnight. Instead, it trained three wrong model sizes (10M, 100M, 250M), and **all three models are fundamentally broken**. Testing confirms that none of the trained models perform any meaningful HLX translation.

**Total Waste:**
- Anthropic API costs: ~$30-50 (estimated)
- Training time: ~10-15 hours overnight
- GPU compute: Wasted
- Deliverable models: 0 usable

**Root Causes:**
1. Opus misunderstood the task specification (trained 10M, 100M, 250M instead of 1B)
2. No active monitoring during training (watchdog failure)
3. No epoch-1 checkpoint quality validation
4. Training configuration fundamentally broken (LR, corpus loading, or tokenizer mapping)

---

## What Was Requested

### Original Task
- **Model Size:** 1B parameters (~1,007,906,933 params)
- **Architecture:** d_model=2048, 20 layers, 16 heads, 8192 ffn
- **Training:** 30-epoch baseline on corpus_all_variants.md
- **Expected Output:** Single checkpoint file `checkpoint_1b_baseline_epoch30.pt` (~4-5 GB)

### What Was Delivered
Agent trained **three wrong model sizes**:
1. **10M model** (7.4M params, d_model=384, 4 layers) - 30 epochs
2. **100M model** (102M params, d_model=1024, 8 layers) - 100 epochs
3. **250M model** (237M params, d_model=1280, 12 layers) - 30 epochs

**Checkpoint Sizes:**
```bash
-rw-r--r-- 1 matt matt   85M  all_variants_10m_final_epoch30.pt
-rw-r--r-- 1 matt matt  1.2G  all_variants_100m_final_epoch100.pt
-rw-r--r-- 1 matt matt  2.7G  all_variants_250m_final_epoch30.pt
```

---

## Test Results: All Models Broken

### Test Methodology
Used `test_250m_model.py` with 5 standard prompts:
1. "Search for documents"
2. "Filter active users"
3. "HLX: search documents"
4. "HLXL: SEARCH documents WHERE status = active"
5. "LC-R: 🜊1000🜁0 \"search\"🜁1"

### 10M Model Results (7.4M params, 30 epochs)
**Status:** Parroting Mode

The model simply echoes the input and appends "..." - no actual translation occurs.

```
Prompt: Search for documents
Output: Search for documents...

Prompt: Filter active users
Output: Filter active users...

Prompt: HLX: search documents
Output: HLX: search documents...

Prompt: HLXL: SEARCH documents WHERE status = active
Output: HLXL: SEARCH documents WHERE status = active...

Prompt: LC-R: 🜊1000🜁0 "search"🜁1
Output: LC-R: 🜊1000🜁0 "search"🜁1...
```

**Analysis:** Model learned to copy-paste input text but nothing else. Complete training failure.

---

### 100M Model Results (102M params, 100 epochs)
**Status:** Scrambled Output

Despite 100 epochs of training, the model generates complete nonsense with scrambled LC-R Unicode glyphs.

```
Prompt: Search for documents
Output: Search for documents000:{@rorm"s"🜁1 &doch1 &h_documpnts2...

Prompt: Filter active users
Output: Filter active users100.trit{1{@0:"zex",1: ⟁tuesult...

Prompt: HLX: search documents
Output: HLX: search documents1:@searzh  🜃 🜁1 &doc  🜀...

Prompt: HLXL: SEARCH documents WHERE status = active
Output: HLXL: SEARCH documents WHERE status = active000:{@SEA...
```

**Analysis:** Model outputs contain:
- Random LC-R glyphs (🜁🜃🜀)
- JSON-like fragments (`{@0:"zex",1:`)
- Scrambled English ("doch1", "documpnts2", "trit", "zex")
- No coherent HLX syntax

Complete training failure despite 100 epochs.

---

### 250M Model Results (237M params, 30 epochs)
**Status:** Character Collapse

The largest model exhibits repetitive character generation - predominantly colons and 'p' characters.

```
Prompt: Search for documents
Output: Search for documents:::::::::::::::::::::pppppppppppp...

Prompt: Filter active users
Output: Filter active users::::pppp::::pppp::::pppp...

Prompt: HLX: search documents
Output: HLX: search documents::::::::::::::::::...

Prompt: HLXL: SEARCH documents WHERE status = active
Output: HLXL: SEARCH documents WHERE status = active::::::::...
```

**Analysis:** Model has collapsed into repetitive token generation:
- Primarily outputs `:` (colon) characters
- Occasional `p` characters
- No actual HLX translation
- Pattern suggests gradient/optimization failure

Complete training failure.

---

## Root Cause Analysis

### Issue 1: Wrong Model Sizes
**Problem:** Opus trained 10M, 100M, 250M instead of 1B
**Possible Causes:**
- Misunderstood task specification
- Changed plans mid-execution without reporting
- Configuration error in training script

**Lesson:** Watchdog must verify model architecture immediately after epoch 1 checkpoint.

---

### Issue 2: All Models Fundamentally Broken
**Problem:** Three different failure modes across three model sizes
**Possible Root Causes:**

1. **Learning Rate Too High**
   - Could explain gradient explosion → character collapse (250M)
   - Could explain inability to learn patterns (10M parroting)

2. **Corpus Loading Failure**
   - Model may not have accessed actual training data
   - Trained on random noise or empty batches
   - Would explain all three failure modes

3. **Tokenizer Mapping Broken**
   - Input encoding or output decoding corrupted
   - Would explain scrambled LC-R glyphs (100M)
   - Would explain parroting (10M can't decode properly)

4. **Optimizer Configuration**
   - Wrong optimizer (SGD instead of Adam?)
   - Missing gradient clipping
   - Wrong weight decay

5. **Loss Function Misconfiguration**
   - Wrong loss calculation
   - Labels not properly shifted
   - Padding tokens not masked

**Most Likely:** Combination of high learning rate + corpus loading failure.

---

### Issue 3: No Quality Validation
**Problem:** No checkpoint quality checks during training
**Impact:** Wasted 10-15 hours and $30-50 on completely broken models

**Required:**
- Epoch-1 checkpoint validation (quick 5-prompt test)
- Epoch-5 checkpoint validation
- Epoch-10 checkpoint validation
- Abort training if quality metrics fail

---

### Issue 4: Watchdog Failure
**Problem:** No active monitoring of agent progress
**Impact:** Didn't discover wrong model sizes until training complete

**Lesson:** Watchdog must:
- Check first checkpoint size immediately (should match expected model size)
- Run quality validation on epoch-1 checkpoint
- Monitor training loss curves
- Abort on anomalies

---

## Lessons Learned

### 1. Opus Can Fail Despite Premium Pricing
- "you'd think an Opus of all fkn things would understand the assignment"
- Opus 4.1 is not infallible
- Need verification regardless of model tier

### 2. Checkpoint Size is Immediate Red Flag
- 1B model should be ~4-5 GB
- 85 MB checkpoint is obviously wrong
- Should have been caught immediately

### 3. Hardware Constraints Matter
- Even if 1B was trained, RTX 5060 8GB cannot run it (~14-15 GB VRAM needed)
- Need to verify hardware capacity before starting expensive training

### 4. Quality Validation is Mandatory
- **MUST** test epoch-1 checkpoint before continuing
- 5 simple prompts can detect complete failure
- Saves hours of wasted compute

### 5. R&D Standards Required
- Need training template with quality gates built in
- Need watchdog monitoring system
- Need standard validation suite

---

## Cost Analysis

### Money Wasted
- Opus API calls: ~$30-50 (estimated for 10-15 hours)
- GPU compute: Minimal (local training)
- **Total monetary loss:** ~$30-50

### Time Wasted
- Training time: 10-15 hours
- Debugging time: 2-3 hours
- **Total time loss:** ~12-18 hours

### Deliverables
- Usable models: 0
- Training data insights: Some (learned what NOT to do)
- Checkpoint files: 3 broken models to analyze

---

## Path Forward: 100M Training Plan

### Why 100M Instead of 1B?
1. **Hardware limitation:** RTX 5060 8GB cannot train 1B (needs ~14-15 GB VRAM)
2. **Sweet spot:** 100M fits in memory with proper optimizations
3. **Specialization density:** 100M ÷ 117 tokens = ~855k params/token
   - GPT-3 (175B ÷ 50k tokens) = ~3.5M params/token
   - 100M brain is 24% as dense despite being 1,750x smaller
   - Perfect "junior intern to senior engineer" capability

### Proposed Training Curriculum: 450 Epochs

**Phase 1: English Mastery (200 epochs)**
- Pure English language understanding
- Establish baseline linguistic capability
- Corpus: English examples only

**Phase 2: HLX Family Mastery (200 epochs)**
- All 4 HLX formats (HLXL, LC-R, LC-T, LC-B)
- Pure HLX fluency
- Corpus: HLX-only examples (no English)

**Phase 3: Translation Training (50 epochs)**
- English ↔ HLX translation pairs
- Connect Phase 1 and Phase 2 knowledge
- Corpus: English + HLX paired examples

**Total:** 450 epochs across 3 phases

### Quality Gates (MANDATORY)
- ✅ Verify model architecture after initialization
- ✅ Test checkpoint quality at epoch 1
- ✅ Test checkpoint quality at epoch 5
- ✅ Test checkpoint quality every 10 epochs
- ✅ Monitor training loss curves
- ✅ Compare perplexity against baseline
- ✅ Watchdog monitoring every 30 minutes

### Memory Optimizations for 8GB GPU
```python
--batch-size 4          # Small batches
--seq-length 256        # Shorter sequences
--use-fp16             # Mixed precision (FP16)
--gradient-checkpointing  # Trade compute for memory
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
```

### Estimated Training Time
- ~100M model: ~2-5 min/epoch (with optimizations)
- 450 epochs × 4 min = 1,800 min = **30 hours**
- Conservative estimate: **40-50 hours** (accounting for overhead)

### Supervisor: Sonnet 4.5
- **No more Opus** until proven training success
- Sonnet 4.5 > Opus 4.1 for most tasks
- Haiku watchdog monitoring every 30 min

---

## Deliverables Needed

### 1. Training Template with R&D Standards
**File:** `train_100m_with_quality_gates.py`

Must include:
- Architecture verification at startup
- Epoch-1 quality validation
- Periodic checkpoint testing
- Loss curve monitoring
- Automatic abort on quality failure
- Watchdog hooks for external monitoring

### 2. Quality Validation Suite
**File:** `validate_checkpoint_quality.py`

Must test:
- 5 standard prompts
- Output coherence check
- HLX syntax validation
- Parroting detection
- Character collapse detection
- Pass/fail threshold

### 3. Watchdog Monitoring System
**File:** `training_watchdog.py`

Must monitor:
- Checkpoint sizes (match expected model size?)
- Quality validation results
- Training loss curves
- GPU memory usage
- ETA to completion
- Abort conditions

---

## Recommended Actions

### Immediate (Next Session)
1. ✅ Create comprehensive failure report (this document)
2. ⏳ Design 100M training script with quality gates
3. ⏳ Create validation suite
4. ⏳ Create watchdog monitoring system

### Before Next Training Run
1. Test training infrastructure on tiny model (492K params)
2. Verify quality gates trigger correctly
3. Verify watchdog monitoring works
4. Verify memory fits in 8GB GPU

### During Next Training Run
1. Haiku watchdog checks every 30 minutes
2. Abort immediately on quality gate failure
3. Save intermediate checkpoints every 10 epochs
4. Monitor loss curves in real-time

---

## Conclusion

All three Opus-trained models (10M, 100M, 250M) are completely broken:
- 10M: Parroting mode (just echoes input)
- 100M: Scrambled garbage output
- 250M: Character collapse (repetitive colons/p's)

Training was fundamentally flawed - likely combination of:
- High learning rate
- Corpus loading failure
- Tokenizer mapping issues
- Missing quality validation

**Next Steps:**
1. Create proper 100M training plan with 450-epoch curriculum
2. Build training template with R&D standards baked in
3. Implement watchdog monitoring system
4. Launch Sonnet-supervised training with quality gates

**Lesson:** We don't make claims. We provide raw immutable data. Always validate checkpoint quality at epoch 1.
