# Haiku Watchdog System Protocol

## Overview
Two Haiku agents (one per specialist) monitor training and report to Sonnet supervisor every 10 epochs.

## Grading System (100 Points)

### 1. Loss Convergence (30 points)
- **30 pts**: Smooth, consistent decrease
- **25 pts**: Generally decreasing with minor fluctuations
- **20 pts**: Decreasing but with some spikes
- **15 pts**: Plateau but stable
- **10 pts**: Erratic/unstable
- **0 pts**: Diverging/increasing

### 2. Validation Accuracy (30 points)
Test on 10 held-out examples every 10 epochs:
- **30 pts**: ≥95% format-correct outputs
- **25 pts**: 90-94% correct
- **20 pts**: 80-89% correct
- **15 pts**: 70-79% correct
- **10 pts**: 60-69% correct
- **0 pts**: <60% correct

### 3. Format Correctness (20 points)
Check generated outputs match expected format:
- **20 pts**: Perfect format (all outputs valid LC-T/LC-R)
- **15 pts**: 1-2 minor format errors
- **10 pts**: 3-5 format errors
- **5 pts**: 6-10 format errors
- **0 pts**: >10 format errors

### 4. Progress Consistency (20 points)
- **20 pts**: Steady improvement each checkpoint
- **15 pts**: Improving with occasional plateaus
- **10 pts**: Slow progress but moving forward
- **5 pts**: Stalled/not improving
- **0 pts**: Regressing

## Grade Scale
- **A (90-100)**: Excellent - continue
- **B (80-89)**: Good - continue with observation
- **C (70-79)**: Acceptable - flag for Sonnet review
- **D (60-69)**: Poor - Sonnet intervention required
- **F (<60)**: Failure - Sonnet must restart/adjust

## Reporting Format

Every 10 epochs, Haiku agents report:

```
CHECKPOINT REPORT - [ASCII/RUNIC] SPECIALIST
Epoch: 50
Phase: 1 (Foundation) / 2 (Specialization)

METRICS:
- Loss: 0.234 (↓ from 0.289)
- Validation: 92% correct (23/25 samples)
- Format errors: 2
- Progress trend: Steady improvement

GRADING:
- Loss Convergence: 28/30 (smooth decrease)
- Validation Accuracy: 25/30 (92% correct)
- Format Correctness: 15/20 (2 minor errors)
- Progress Consistency: 18/20 (steady)
TOTAL: 86/100 (Grade: B)

STATUS: ✓ Training on track
RECOMMENDATION: Continue
```

## Intervention Triggers

### Grade D (60-69): Sonnet Review Required
Sonnet checks:
1. Is loss stuck/diverging?
2. Are validation errors systematic?
3. Should we adjust learning rate?
4. Should we restart from checkpoint?

### Grade F (<60): Immediate Action
Sonnet must:
1. Stop training
2. Analyze failure mode
3. Adjust hyperparameters OR
4. Restart from last good checkpoint OR
5. Regenerate corpus if data quality issue

## Correction Protocols

### Loss Not Decreasing
1. Check: Is learning rate too high? → Reduce by 50%
2. Check: Is batch size too small? → Can't change mid-training
3. Action: Restart from checkpoint with lower LR

### Validation Errors Increasing
1. Check: Overfitting? → Reduce epochs or add regularization
2. Check: Data quality? → Review corpus examples
3. Action: Stop and investigate

### Format Errors Persistent
1. Check: Tokenizer issue? → Verify special tokens
2. Check: Corpus examples? → Audit format consistency
3. Action: Fix corpus and restart

## Haiku Agent Responsibilities

### Agent 1: ASCII Specialist Monitor
- Watch `/home/matt/hlx-dev-studio/models/qwen3_1_7b_ascii_specialist/training_metrics.jsonl`
- Test outputs every 10 epochs
- Report to Sonnet
- Respond to Sonnet corrections

### Agent 2: Runic Specialist Monitor
- Watch `/home/matt/hlx-dev-studio/models/qwen3_1_7b_runic_specialist/training_metrics.jsonl`
- Test outputs every 10 epochs
- Report to Sonnet
- Respond to Sonnet corrections

## Sonnet Supervisor Responsibilities

1. **Monitor reports** from both Haiku agents
2. **Make intervention decisions** when grades drop
3. **Issue corrections** (adjust LR, restart, etc.)
4. **Track overall progress** across both specialists
5. **Ensure training completes** by morning

## Success Criteria

### Phase 1 Complete (both specialists)
- Grade: B or higher
- Loss: <0.20
- Validation: >85% correct
- All HLX formats understood

### Phase 2 Complete (both specialists)
- Grade: A (>90 points)
- Loss: <0.15
- Validation: >95% correct
- Perfect format mastery for specialist track

## Emergency Protocols

### GPU OOM
- Kill all training processes
- Clear GPU memory
- Restart with batch_size=1 if needed

### Training Stuck (>30 min no progress)
- Check process is running
- Check GPU utilization
- Kill and restart if frozen

### Corpus Issues Discovered
- Stop training immediately
- Fix corpus
- Restart from beginning (don't use corrupted checkpoints)
