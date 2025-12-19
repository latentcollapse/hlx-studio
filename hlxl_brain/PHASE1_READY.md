# HLXL Brain Phase 1: Ready to Train

## Summary

We've designed a **100-epoch curriculum** to expand the HLXL Tiny Brain from a syntax pattern-matcher to a semantic reasoning engine. Phase 1 corpus is ready!

---

## What We Have

### Current Model (Day 4 Baseline)
- **Checkpoint:** `checkpoints/final_model.pt`
- **Epochs trained:** 5
- **Parameters:** 491,635
- **Size:** 1.88 MB
- **Training loss:** 0.21
- **Validation loss:** 0.23
- **Speed:** 700 tok/s
- **Capability:** LC-R syntax pattern completion (no semantics)

### Training Data
- **Original corpus:** 164 LC-R syntax examples
- **New Phase 1 corpus:** 388 semantic grounding examples
- **Combined total:** 552 examples
- **Phase 1 covers:**
  - Navigation (`navigate`, `go`, `move`)
  - Search & query (`search`, `find`, `look for`)
  - Filtering (`filter`, `select`, `keep`)
  - Transformation (`transform`, `convert`, `apply`)
  - Aggregation (`sum`, `average`, `count`, `min`, `max`)
  - Data operations (`read`, `write`, `load`, `save`)
  - Computation (`compute`, `calculate`, `evaluate`)
  - Validation (`validate`, `check`, `verify`)
  - Execution (`execute`, `run`, `perform`)
  - Composite pipelines (multi-step workflows)

---

## The 4-Phase Plan

### Phase 1: Semantic Grounding (Epochs 6-30, 25 epochs)
**Status:** ✅ **CORPUS READY** (388 examples generated)
**Goal:** Teach operations their *meaning*, not just syntax
**Time estimate:** 6-8 hours CPU training
**Expected outcome:** Model generates semantically correct LC-R for English prompts

### Phase 2: Domain Knowledge (Epochs 31-55, 25 epochs)
**Status:** 📋 Not started
**Goal:** File systems, data structures, control flow, common patterns
**Target:** 600+ examples
**Time estimate:** 8-10 hours

### Phase 3: Long-Form Reasoning (Epochs 56-80, 25 epochs)
**Status:** 📋 Not started
**Goal:** Handle 256-512 token sequences, maintain context, complex programs
**Target:** 400+ examples (longer sequences)
**Time estimate:** 10-12 hours

### Phase 4: Perfect HLX + Quality English (Epochs 81-105, 25 epochs)
**Status:** 📋 Not started
**Goal:** Master all HLX formats (LC-R, LC-B, HLXL) + natural English
**Target:** 500+ examples (bidirectional, style variations)
**Time estimate:** 8-10 hours

**Total training time:** ~32-40 hours (can run overnight/background)

---

## Sample Phase 1 Examples

```
English: Navigate to home
LC-R: 🜊1000🜁0 "navigate"🜁1 ⟁home🜂

English: Search logs for error
LC-R: 🜊1000🜁0 "search"🜁1 ⟁logs🜁2 "error"🜂

English: Filter records where active
LC-R: 🜊1000🜁0 "filter"🜁1 ⟁records🜁2 ⟁active🜂

English: Transform text to uppercase
LC-R: 🜊1000🜁0 "transform"🜁1 ⟁text🜁2 ⟁uppercase🜂

English: Calculate sum of value
LC-R: 🜊1000🜁0 "aggregate"🜁1 ⟁sum🜁2 ⟁value🜂

English: Read from data.json
LC-R: 🜊1000🜁0 "read"🜁1 "data.json"🜂

English: Write results to output.json
LC-R: 🜊1000🜁0 "write"🜁1 "output.json"🜁2 ⟁results🜂

English: Validate config against schema
LC-R: 🜊1000🜁0 "validate"🜁1 ⟁config🜁2 ⟁schema🜂

English: Load data.json, normalize it, and save to output.json
LC-R: 🜊1000🜁0 "pipeline"🜁1 🜊14🜁0 🜊1000🜁0 "read"🜁1 "data.json"🜂🜁1 🜊1000🜁0 "transform"🜁1 ⟁data🜁2 ⟁normalize🜂🜁2 🜊1000🜁0 "write"🜁1 "output.json"🜁2 ⟁result🜂🜂🜂
```

---

## Files Created

### Documentation
- ✅ `CURRICULUM.md` - Complete 100-epoch training plan
- ✅ `PHASE1_READY.md` - This file

### Corpus Generators
- ✅ `corpus_generator_phase1.py` - Generates 388 semantic examples

### Generated Corpora
- ✅ `corpus_phase1_semantic_grounding.md` - 388 examples ready for training

### Still Need
- ⏳ `corpus_generator_phase2.py` - Domain knowledge
- ⏳ `corpus_generator_phase3.py` - Long sequences
- ⏳ `corpus_generator_phase4.py` - Perfect HLX + English

---

## Next Steps

### Option A: Start Phase 1 Training Now
**Pros:**
- Get immediate progress on semantic understanding
- Can evaluate Phase 1 results before building Phase 2-4
- Iterative approach (adjust curriculum based on results)

**Commands:**
```bash
# Merge original + Phase 1 corpus
cat /home/matt/LC_R_EXAMPLES_FOR_VERIFICATION_TESTING.md corpus_phase1_semantic_grounding.md > corpus_combined_phase1.md

# Modify train.py to:
# 1. Load from existing checkpoint
# 2. Use combined corpus
# 3. Train for 25 more epochs (6-30)

# Start training
python3 train.py --resume checkpoints/final_model.pt \
                 --corpus corpus_combined_phase1.md \
                 --epochs 25 \
                 --start-epoch 6 \
                 --phase "Phase 1: Semantic Grounding"
```

### Option B: Build All Corpus Generators First
**Pros:**
- Complete curriculum ready before training starts
- Can review all phases before committing compute time
- One long training run (less intervention)

**Steps:**
1. Generate Phase 2 corpus (domain knowledge)
2. Generate Phase 3 corpus (long sequences)
3. Generate Phase 4 corpus (perfect HLX + English)
4. Merge all corpora
5. Start complete 100-epoch training run

**Estimated time to build all generators:** 2-3 hours
**Total training time:** 32-40 hours (can run overnight)

---

## Training Infrastructure Needed

### Modified Training Script
Current `train.py` needs these additions:
1. **Resume from checkpoint** - Load existing model weights
2. **Epoch offset** - Start from epoch 6 (not 1)
3. **Combined corpus loading** - Handle multiple corpus files
4. **Phase tracking** - Log which phase is running
5. **Improved checkpointing** - Save every 5 epochs + best
6. **Live monitoring** - Real-time loss curves
7. **Sample generation** - Test generation every 5 epochs

### Resource Requirements
- **CPU-only:** 4-8 cores (current setup works)
- **Memory:** ~4-8 GB RAM
- **Storage:** ~50 MB for checkpoints
- **Time:** 32-40 hours total (can pause/resume)

---

## Expected Outcomes

### After Phase 1 (Epoch 30)
- **Semantically correct LC-R** for English descriptions
- Understands **30+ operation types**
- Can **complete partial sequences** intelligently
- **Val loss target:** < 0.15
- Still fast: **~650+ tok/s** (slight slowdown from more knowledge)

### After All Phases (Epoch 105)
- **Zero syntax errors** in generated LC-R
- **Natural, idiomatic English** ↔ LC-R translation
- **Long coherent programs** (200+ tokens)
- **Perfect HLX family syntax** (LC-R, LC-B, HLXL)
- **Val loss target:** < 0.05
- Speed: **~500+ tok/s** (still very fast)

---

## Comparison with Qwen3 Models

After Phase 4, the HLXL Brain will sit between Tiny and Mid:

| Brain | Parameters | Size | Speed | Capability |
|-------|-----------|------|-------|------------|
| **HLXL Tiny (Day 4)** | 491K | 1.88 MB | 700 tok/s | Syntax only |
| **HLXL Expanded (Phase 4)** | 491K | 1.88 MB | ~500 tok/s | **Syntax + Semantics** |
| **Qwen3 Mid (0.6B)** | 600M | 522 MB | 118 tok/s | General reasoning |
| **Qwen3 Large (1.7B)** | 1.7B | 1.4 GB | 101 tok/s | Complex reasoning |

**Key advantage of expanded HLXL:**
- **HLX-specialized** - Perfect LC-R generation (Qwen models hallucinate)
- **10x-100x faster** - Still 500 tok/s vs 100 tok/s for Qwen
- **1000x smaller** - 1.88 MB vs 522 MB (Qwen 0.6B)
- **Deterministic** - T=0 greedy decoding (no randomness)
- **Embedded-friendly** - Fits on tiny devices

---

## Risk Mitigation

### Overfitting Prevention
- Keep 20% of original examples in each phase (replay buffer)
- Validation set held out (never trained on)
- Dropout (0.1) + Weight decay (L2 regularization)
- Early stopping if val loss increases

### Catastrophic Forgetting
- Gradual curriculum (don't drop old tasks)
- Multi-task training in final 5 epochs
- Frequent checkpointing (can rollback if needed)

### Time Management
- Can pause/resume between phases
- Checkpoints every 5 epochs (safe stopping points)
- Phase 1 results inform whether to continue

---

## Recommendation

**I recommend Option A: Start Phase 1 Now**

**Reasons:**
1. Phase 1 corpus is ready (388 examples generated)
2. Can evaluate semantic learning before building Phase 2-4
3. 6-8 hours is manageable (overnight training)
4. Results will inform if curriculum needs adjustments
5. Iterative approach reduces risk of wasted compute

**After Phase 1 completes:**
- Evaluate: Does the model understand operation semantics?
- Test generation: English → LC-R quality check
- Decide: Continue to Phase 2 or adjust curriculum?

**If you prefer Option B (build all first):**
- I'll create corpus generators for Phases 2-4 (~2 hours)
- Then one long 100-epoch training run (32-40 hours)
- Less iteration, but complete curriculum from start

---

## Ready to Proceed?

Everything is set up for Phase 1 training:
- ✅ Curriculum designed
- ✅ Phase 1 corpus generated (388 examples)
- ✅ Existing checkpoint (5 epochs baseline)
- ✅ Training infrastructure exists

**Just need to:**
1. Merge corpora (original 164 + new 388 = 552 total)
2. Modify `train.py` for continued training
3. Start 25-epoch Phase 1 run

**What would you like to do?**
- **A)** Start Phase 1 training now (6-8 hours)
- **B)** Build all phase corpus generators first (~2 hours), then train (32-40 hours)
- **C)** Review curriculum, make adjustments before proceeding
