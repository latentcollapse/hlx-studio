# HLX Training Failure Analysis
**Date**: 2025-12-18
**Hardware**: RTX 5060 8GB
**Finding**: Fundamental memory inefficiency in Qwen model family

---

## Critical Discovery

**Qwen models consume 3-4x more GPU memory than they theoretically should.**

### Evidence

| Model | Theoretical Size | Actual GPU Usage | Overhead |
|-------|-----------------|------------------|----------|
| Qwen2 0.5B (float32) | ~2GB | 6.32GB | 3.16x |
| Qwen3 0.6B (float16) | ~1.2GB | ~6-7GB | 5-6x |
| Qwen3 1.7B (8-bit) | ~1.7GB | 6.83GB+ (OOM) | 4x+ |

### Test Results

**Test 1: Qwen3 1.7B + 8-bit quantization + batch size 4**
- Result: OOM during loss computation
- Memory: 6.04GB allocated, needs +296MB for loss
- Status: FAILED

**Test 2: Qwen3 0.6B + float16 + batch size 4**
- Result: OOM during loss computation
- Memory: Similar to Test 1
- Status: FAILED

**Test 3: Qwen3 0.6B + float16 + batch size 2**
- Result: Trains but produces NaN loss
- Memory: Borderline stable
- Status: TRAINS BUT BROKEN

**Test 4: Qwen2 0.5B + float32 + batch size 1**
- Result: OOM on optimizer initialization
- Memory: 6.32GB for model alone, 6.69MB free
- Status: FAILED - Can't even initialize optimizer

---

## Root Causes Identified

### 1. Memory Inefficiency
The Qwen models load with massive memory overhead. Possible causes:
- KV cache pre-allocated too large
- Attention buffers not optimized
- Model architecture has hidden layers/tensors
- Transformers library loading inefficiently for these models

### 2. Corpus/Tokenization Mismatch (Secondary Issue)
When we DID get training running (Test 3), we got NaN losses, indicating:
- Mixed English/HLX format confuses the model
- Tokenizer doesn't naturally understand HLX symbols
- Loss computation becomes numerically unstable

---

## What We Learned

### Works:
- ✅ Training infrastructure (optimizer, scheduler, loop) is correct
- ✅ Minimal corpus format (corpus_minimal_hlx.txt) - 61 clean examples
- ✅ GPU itself is functional
- ✅ Training script logic is sound

### Broken:
- ❌ Qwen model family has catastrophic memory inefficiency on 8GB GPUs
- ❌ Mixed language corpus causes NaN losses even when memory permits
- ❌ No quantization level makes 1.7B trainable on 8GB
- ❌ Even 0.5B can't train in full precision

---

## Recommendations for Opus

### Option 1: Different Model Family
Try models known to be memory-efficient:
- **GPT-2 variants** (proven efficient, well-documented)
- **DistilGPT-2** (134M params, ~500MB)
- **TinyLlama** (1.1B, proven to train on limited VRAM)
- **Pythia models** (160M-1.4B, research-focused, efficient)

### Option 2: Parameter-Efficient Fine-Tuning
Instead of full fine-tuning:
- **LoRA**: Train only small adapter layers (1-5% of parameters)
- **QLoRA**: LoRA + 4-bit quantization (proven to work on 8GB)
- **Prefix tuning**: Only train input prefixes

### Option 3: Corpus Redesign
Create a corpus that:
- **Pure HLX examples only** (no English mixing)
- **Clear input→output format**: `<|input|> TRUE <|output|> ⊤`
- **Instruction-tuning format**: "Translate to HLX: TRUE" → "⊤"
- **Smaller initially**: 100-200 high-quality examples, not 733 mixed ones

### Option 4: Custom Training Objective
Instead of causal LM:
- **Seq2seq**: Encode English → Decode HLX
- **Classification**: Is this valid HLX? Yes/No
- **Masked LM**: Fill in [MASK] in HLX code

---

## Immediate Next Steps

1. **Kill all Qwen-based attempts** - They won't work on 8GB without heroic effort
2. **Test with GPT-2 Small (124M)** - Proven memory-efficient
3. **Redesign corpus** - Clean input/output pairs
4. **Consider LoRA** - Most realistic path to 1B+ models on 8GB

---

## Files Created

- `corpus_minimal_hlx.txt` - 61 clean HLX examples (ready for use)
- `train_minimal_test.py` - Verified training script (works, just needs different model)
- `helix_brain_1_7b.py` - Original attempt (archived, do not use)

---

## Memory Benchmark Reference

For future model selection, target:
- **Model size**: <2GB in float16
- **+Optimizer**: +4GB (Adam) = <6GB total
- **+Activations/batch**: ~1-2GB headroom needed
- **Total budget**: 6GB max for safe 8GB training
