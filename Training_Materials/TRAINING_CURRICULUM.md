# Helix MoE 5.1B Training Curriculum

## Architecture
- **Coordinator**: Qwen3-1.7B base (routing + general HLX + LC-B)
- **ASCII Specialist**: Qwen3-1.7B (HLXL + LC-T + HLXL-LS)
- **Runic Specialist**: Qwen3-1.7B (HLX + LC-R + HLX-LS)
- **Total**: 5.1B params (3.4B active)

## Training Methodology

### Phase 1: General HLX Foundation (50-100 Epochs)
**Goal**: Distill comprehensive HLX family knowledge into both specialists

**Coverage:**
- HLXL syntax and semantics
- LC-T (ASCII-safe text format)
- LC-R (Runic Unicode format)
- LC-B (Binary encoding basics)
- Cross-format translations
- Contract system (900-902, 1000)
- Handle semantics (@handles, &references, ⟁glyph handles)
- Type system and primitives
- Array and object notation
- Bidirectional conversions

**Corpus Size**: 200-300 examples
**Training**: 50-100 epochs on general corpus
**Expected Time**: ~2-3 hours per specialist

### Phase 2: Deep Specialization (200-300 Epochs)
**Goal**: Master specialist track and language server operations

#### ASCII Specialist Track
**Coverage:**
- HLXL high-level syntax (deep)
- LC-T format mastery
- HLXL-LS operations:
  - Code completion
  - Symbol resolution
  - Type inference
  - Diagnostics
  - Refactoring operations
  - Hover information
- ASCII-safe contract notation
- Compact notation optimization
- Edge cases and error handling

**Corpus Size**: 300-500 examples
**Training**: 200-300 epochs on specialization corpus
**Expected Time**: ~6-8 hours

#### Runic Specialist Track
**Coverage:**
- HLX Unicode variant (deep)
- LC-R format mastery
- HLX-LS operations:
  - Code completion with glyphs
  - Symbol resolution
  - Type inference
  - Diagnostics
  - Refactoring operations
  - Hover information
- Unicode glyph contracts (🐊, 🐁, 🐂, ⟁, ⊤, ⊥, ∅)
- Glyph optimization
- Edge cases and error handling

**Corpus Size**: 300-500 examples
**Training**: 200-300 epochs on specialization corpus
**Expected Time**: ~6-8 hours

## Quality Assurance

### Haiku Watchdog System
Two Haiku agents supervise training with points-based grading:

**Metrics Tracked:**
1. **Loss Convergence** (30 points)
   - Smooth decrease: 30 pts
   - Some spikes: 20 pts
   - Erratic: 10 pts
   - Diverging: 0 pts

2. **Validation Accuracy** (30 points)
   - >95% correct: 30 pts
   - 90-95%: 25 pts
   - 80-90%: 20 pts
   - <80%: 10 pts

3. **Format Correctness** (20 points)
   - Perfect formatting: 20 pts
   - Minor errors: 15 pts
   - Major errors: 5 pts

4. **Progress Consistency** (20 points)
   - Steady improvement: 20 pts
   - Plateaus handled: 15 pts
   - Stalls: 10 pts
   - Regression: 0 pts

**Total: 100 points per checkpoint**

**Grading Scale:**
- A (90-100): Excellent progress
- B (80-89): Good progress
- C (70-79): Acceptable, needs attention
- D (60-69): Poor, intervention required
- F (<60): Training failure, restart needed

**Checkpoint Frequency**: Every 10 epochs

### Drift Correction Protocol
If grade drops below B (80 points):
1. **Warning**: Log issue and continue
2. **Intervention** (grade < 70): Adjust learning rate or batch size
3. **Restart** (grade < 60): Restart from best checkpoint

## Training Timeline

### Night 1 (Tonight)
- **00:00-02:00**: Build comprehensive corpora
- **02:00-03:00**: Phase 1 ASCII (general foundation, 50-100 epochs)
- **03:00-04:00**: Phase 1 Runic (general foundation, 50-100 epochs)
- **04:00-10:00**: Phase 2 ASCII (specialization, 200-300 epochs)
- **04:00-10:00**: Phase 2 Runic (specialization, 200-300 epochs) [parallel if memory allows]
- **10:00-11:00**: Testing and validation

**Total**: ~11 hours for complete training

## Success Criteria

### Phase 1 Completion
- ✓ Loss < 0.2
- ✓ Can translate between all HLX formats
- ✓ Understands contract system
- ✓ Handles primitives, arrays, objects correctly

### Phase 2 Completion (ASCII)
- ✓ Loss < 0.15
- ✓ Perfect LC-T format generation
- ✓ HLXL syntax mastery
- ✓ HLXL-LS operations working

### Phase 2 Completion (Runic)
- ✓ Loss < 0.15
- ✓ Perfect LC-R format generation
- ✓ HLX syntax mastery
- ✓ HLX-LS operations working

## Deliverables
- `/models/qwen3_1_7b_ascii_specialist/final_model/`
- `/models/qwen3_1_7b_runic_specialist/final_model/`
- Training logs and metrics
- Validation test results
- Points/grades report
