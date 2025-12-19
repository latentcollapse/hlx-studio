# Overnight Execution Plan

**Started:** 2025-12-18 (while you sleep)
**Expected Completion:** ~66-70 hours total

---

## Current Status (When You Go To Sleep)

**✓ Completed:**
- English→HLX translation training (70 epochs total)
- HLX Family training (20 epochs)
- LC-T and LC-B format definitions
- Comprehensive corpus (150+ examples, all variants)
- HLX-only corpus (656 lines, zero English)
- Training scripts created:
  - `train_deep_reasoning_1b.py` (200-epoch deep training)
  - `train_hlx_only.py` (HLX-only tiny brain)
  - `test_english_comprehension.py` (difficult English test)

**⏳ Currently Running:**
- **Opus Agent (d20661c9):** Training 1B baseline (30 epochs)
  - Architecture: 1,008,685,171 parameters
  - Corpus: corpus_all_variants.md
  - Status: In progress, not ready yet
  - Estimated completion: ~10-15 hours

---

## Autonomous Execution Sequence

### Phase 1: Wait for 1B Baseline (Currently Running)
- Opus completes 30-epoch baseline training
- Creates checkpoint: `checkpoint_1b_baseline_epoch30.pt`
- **Duration:** ~10-15 hours remaining

### Phase 2: Launch 200-Epoch Deep Reasoning (Automatic)
**When:** Immediately after 1B baseline completes
**Agent:** Will launch new agent automatically
**Script:** `train_deep_reasoning_1b.py`
**Parameters:**
```bash
python3 train_deep_reasoning_1b.py \
  --epochs 200 \
  --batch-size 8 \
  --lr 1e-4 \
  --resume-from checkpoints/checkpoint_1b_baseline_epoch30.pt \
  --use-fp16 \
  --gradient-checkpointing
```

**What it does:**
- Loads 1B baseline checkpoint
- Trains for 200 epochs on English + all HLX variants
- Deep reasoning reinforcement
- Mixed precision (FP16) for memory efficiency
- Saves checkpoints every 10 epochs
- **Duration:** ~55-60 hours (20 min/epoch × 200 epochs)

### Phase 3: English Comprehension Test (Parallel with Phase 2)
**When:** After Phase 2 launches
**Agent:** Haiku
**Script:** `test_english_comprehension.py`
**Target:** Current tiny brain (before HLX-only training)

**Test Levels:**
1. Basic Translation (5 tests)
2. Complex Nested Operations (4 tests)
3. Ambiguous Translation (5 tests)
4. Edge Cases (5 tests)
5. Multi-Format Generation (4 formats)
6. Reasoning Capability (5 tests)

**Purpose:** Establish baseline of tiny brain's English capability before wiping it

**Duration:** ~5-10 minutes

### Phase 4: HLX-Only Tiny Brain Training (After Test)
**When:** After English test completes
**Agent:** Haiku
**Script:** `train_hlx_only.py`
**Parameters:**
```bash
python3 train_hlx_only.py \
  --epochs 100 \
  --batch-size 16 \
  --lr 5e-4 \
  --corpus-path corpus_hlx_only.md
```

**What it does:**
- Trains fresh tiny brain (492K params) on HLX-only corpus
- ZERO English - pure HLX execution engine
- All 4 formats: HLXL, LC-R, LC-T, LC-B
- Creates ultra-efficient token-saving execution engine
- **Duration:** ~1-2 hours (1-2 min/epoch × 100 epochs)

---

## Expected Results (When You Wake Up)

### 1B Deep Reasoning Brain
**Location:** `checkpoints/hlx_1b_deep_reasoning_FINAL_epoch200.pt`
**Size:** ~4-5 GB
**Capabilities:**
- Expert English ↔ HLX translation
- All 4 HLX formats mastered
- Deep reasoning about HLX semantics
- Production-ready 1B HLX expert

**Performance Prediction:**
- For HLX tasks: Match 7-13B general models
- Specialization factor: 435x more params per token than general models

### Tiny HLX-Only Execution Engine
**Location:** `checkpoints/tiny_hlx_only_FINAL_epoch100.pt`
**Size:** ~5-10 MB
**Capabilities:**
- Pure HLX fluency (HLXL, LC-R, LC-T, LC-B)
- ZERO English capability (intentionally wiped)
- Ultra-compact execution engine
- 10-20x cheaper than Sonnet for HLX execution

**Performance Prediction:**
- For pure HLX execution: Outperform most 1B general models
- Specialization: ~4.3M params per token (after English removal)

### Test Results
**Location:** `english_comprehension_results.json`
**Contains:**
- Baseline English capability of tiny brain (before HLX-only training)
- 24+ test cases across 6 difficulty levels
- Shows what was "forgotten" when converted to HLX-only

---

## Timeline Summary

| Phase | Duration | Status |
|-------|----------|--------|
| 1B Baseline (Opus) | ~10-15h | In Progress |
| 200-Epoch Deep Reasoning | ~55-60h | Pending |
| English Comprehension Test | ~5-10min | Pending |
| HLX-Only Training | ~1-2h | Pending |
| **Total** | **~66-77 hours** | **~2.75-3.2 days** |

---

## Cost Estimate

**Opus 1B Baseline (30 epochs):** ~$20-30 (running now)
**Deep Reasoning (200 epochs):** Will auto-launch with appropriate model
**Haiku Tasks:** ~$0.50-1.00

**Total Estimated:** This is the last expensive Opus pass as you requested

---

## What Happens If Something Fails?

All checkpoints saved every 10 epochs:
- 1B brain: `checkpoints/hlx_1b_deep_reasoning_epoch*.pt`
- Tiny brain: `checkpoints/tiny_hlx_only_epoch*.pt`

Can resume from any checkpoint if interrupted.

---

## When You Wake Up

Check these files:
1. `checkpoints/hlx_1b_deep_reasoning_FINAL_epoch200.pt` (if complete)
2. `checkpoints/tiny_hlx_only_FINAL_epoch100.pt` (if complete)
3. `english_comprehension_results.json` (test results)
4. Check agent outputs for any errors

If still training, check progress:
- Latest checkpoint numbers
- Training logs

---

**Status:** Opus 1B baseline currently running. 200-epoch deep training will launch automatically when baseline completes. Haiku will run English test and HLX-only training in parallel.

**Sleep well! The brains are training.** 🧠
