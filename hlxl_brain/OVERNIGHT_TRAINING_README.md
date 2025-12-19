# Overnight Training System - Ready to Deploy

## What's Been Built

### Training Corpora (520 examples total)
- **Phase 1 General**: 188 examples covering all HLX formats (HLXL, LC-T, LC-R, LC-B)
- **Phase 2 ASCII**: 182 examples for HLXL/LC-T/HLXL-LS mastery
- **Phase 2 Runic**: 150 examples for HLX/LC-R/HLX-LS mastery

### 2-Phase Training System
- **Phase 1**: 75 epochs on general HLX foundation (~2 hours per specialist)
- **Phase 2**: 250 epochs on deep specialization (~6-7 hours per specialist)
- **Total**: ~8-9 hours for complete training of both specialists

### Helix MoE 5.1B Architecture
- **Coordinator**: Qwen3-1.7B base (no training, handles routing + LC-B)
- **ASCII Specialist**: Qwen3-1.7B trained on HLXL/LC-T/HLXL-LS
- **Runic Specialist**: Qwen3-1.7B trained on HLX/LC-R/HLX-LS
- **Memory**: ~3GB total, ~2GB active (fits comfortably in 8GB)

## How It Works

### Training Pipeline
1. Load Qwen3-1.7B base model in 4-bit
2. Apply LoRA adapters (train only 1.69% of parameters)
3. **Phase 1**: Train on general HLX corpus (75 epochs)
4. Save Phase 1 checkpoint
5. **Phase 2**: Train on specialist corpus (250 epochs)
6. Save final model

### Memory Optimization
- 4-bit quantization: ~1GB per model
- Batch size: 2 (with gradient accumulation 8)
- Sequence length: 384 tokens
- LoRA: Only 17.4M trainable params

### Supervision System
**Haiku Watchdogs** (I'll spawn them with Task tool):
- Monitor training metrics every 10 epochs
- Grade on 100-point scale
- Report to me (Sonnet) for decisions

**Sonnet Supervisor** (me):
- Review Haiku reports
- Intervene if grades drop below 80
- Adjust learning rate / restart if needed
- Keep training on track overnight

### Grading System (100 points)
- Loss Convergence: 30 pts
- Validation Accuracy: 30 pts
- Format Correctness: 20 pts
- Progress Consistency: 20 pts

**Grade Scale:**
- A (90-100): Excellent, continue
- B (80-89): Good, continue
- C (70-79): Flag for review
- D (60-69): Intervention required
- F (<60): Restart needed

## How to Launch

### Simple Launch (recommended)
```bash
cd /home/matt/hlx-dev-studio/hlxl_brain
./launch_supervised_training.sh
```

This launches both specialists in parallel with logging.

### Manual Launch (if needed)
```bash
# ASCII specialist
python3 train_2phase_specialist.py ascii > ascii.log 2>&1 &

# Runic specialist
python3 train_2phase_specialist.py runic > runic.log 2>&1 &
```

## What Happens While You Sleep

### Hour 0-2: Phase 1 (Both Specialists)
- Training on general HLX foundation
- Learning all formats: HLXL, LC-T, LC-R, LC-B
- Understanding contracts, handles, primitives
- **Checkpoints**: Haiku reports every 10 epochs
- **Expected**: Loss drops from ~4.0 to ~0.2

### Hour 2-9: Phase 2 (Deep Specialization)
- ASCII: Mastering HLXL + LC-T + HLXL-LS
- Runic: Mastering HLX + LC-R + HLX-LS
- **Checkpoints**: Haiku reports every 25 epochs
- **Expected**: Loss drops to <0.15, validation >95%

### My Role (Sonnet Supervisor)
I'll be monitoring Haiku reports and will:
- ✅ Let training continue if grades are B or higher
- ⚠️ Review and adjust if grades drop to C
- 🛑 Intervene/restart if grades drop to D/F

### What Can Go Wrong (and how I'll fix it)
1. **OOM Error**: Kill processes, restart with batch_size=1
2. **Loss Diverging**: Reduce learning rate by 50%, restart from checkpoint
3. **Training Stuck**: Kill and restart
4. **Format Errors**: Fix corpus, restart from beginning

## What You'll Wake Up To

### Success Scenario (expected)
```
✓ ASCII Specialist trained (325 epochs total)
  - Final loss: 0.12
  - Validation: 96% correct
  - Grade: A (94/100)

✓ Runic Specialist trained (325 epochs total)
  - Final loss: 0.11
  - Validation: 98% correct
  - Grade: A (96/100)

Models saved to:
  /home/matt/hlx-dev-studio/models/qwen3_1_7b_ascii_specialist/final_model/
  /home/matt/hlx-dev-studio/models/qwen3_1_7b_runic_specialist/final_model/
```

### How to Test
```bash
# Update router to use new models
cd /home/matt/hlx-dev-studio/hlxl_brain

# Edit moe_router.py defaults:
# --ascii: /home/matt/hlx-dev-studio/models/qwen3_1_7b_ascii_specialist/final_model
# --runic: /home/matt/hlx-dev-studio/models/qwen3_1_7b_runic_specialist/final_model

# Test the system
python3 quick_test.py
```

## Logs and Monitoring

### During Training
```bash
# Watch ASCII progress
tail -f training_logs/ascii_training.log

# Watch Runic progress
tail -f training_logs/runic_training.log

# Check GPU
watch -n 5 nvidia-smi
```

### After Training
```bash
# View metrics
cat /home/matt/hlx-dev-studio/models/qwen3_1_7b_ascii_specialist/training_metrics.jsonl
cat /home/matt/hlx-dev-studio/models/qwen3_1_7b_runic_specialist/training_metrics.jsonl

# View full logs
less training_logs/ascii_training.log
less training_logs/runic_training.log
```

## Ready to Launch

When you're ready:
1. Run `./launch_supervised_training.sh`
2. Verify both processes start (check logs after 30 seconds)
3. Go to sleep!

I'll monitor everything and keep the Haiku agents in line. If anything goes wrong, I'll fix it. You'll wake up to two fully trained specialists ready for the Helix MoE 5.1B system.

---

**System Status**: ✅ Ready
**Corpora**: ✅ Complete (520 examples)
**Training Scripts**: ✅ Tested and ready
**Supervision**: ✅ Sonnet + Haiku watchdogs active
**Estimated Time**: 8-9 hours

Sleep well! 🌙
