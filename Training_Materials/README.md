# Training Materials - Frozen Working System

This folder contains a **frozen snapshot** of the working training system used to create the Helix 5.1B MoE specialists.

## 📦 Contents

### Training Corpora (520 examples total)
- `corpus_phase1_general.jsonl` - 188 examples for Phase 1 foundation
- `corpus_phase2_ascii_specialist.jsonl` - 182 examples for ASCII specialist (HLXL/LC-T/HLXL-LS)
- `corpus_phase2_runic_specialist.jsonl` - 150 examples for Runic specialist (HLX/LC-R/HLX-LS)

### Training Scripts
- `train_2phase_specialist.py` - Main 2-phase training script (Phase 1: 75 epochs, Phase 2: 250 epochs)
- `launch_supervised_training.sh` - Master launch script for both specialists

### Architecture
- `moe_router.py` - MoE routing system (Coordinator + ASCII + Runic specialists)

### Documentation
- `TRAINING_CURRICULUM.md` - Complete training methodology
- `OVERNIGHT_TRAINING_README.md` - User guide for overnight training
- `WATCHDOG_PROTOCOL.md` - Supervision and monitoring protocol

## 🎯 How to Use

### Train a New Specialist
```bash
cd /home/matt/hlx-dev-studio/Training_Materials

# ASCII specialist
python3 train_2phase_specialist.py ascii

# Runic specialist
python3 train_2phase_specialist.py runic
```

### Launch Supervised Training
```bash
./launch_supervised_training.sh
```

This launches both specialists sequentially with full logging.

## 📊 Training Configuration

**Model**: Qwen3-1.7B
**Method**: QLoRA (4-bit quantization + LoRA)
**Trainable Parameters**: 17.4M (1.69% of model)

**Phase 1** (75 epochs, ~2 hours):
- General HLX foundation
- All formats: HLXL, LC-T, LC-R, LC-B
- Learning rate: 2e-4

**Phase 2** (250 epochs, ~6-7 hours):
- Deep specialization
- Track-specific corpus
- Learning rate: 1e-4

**Memory**: ~5.3GB peak (fits in 8GB VRAM)

## ✅ Validation Results

These settings produced:
- **ASCII Specialist**: Final loss 0.0138, validation >95%
- **Runic Specialist**: Final loss ~0.011, validation >98%
- **Total Training Time**: ~16-18 hours for both specialists

## 🔒 Why Frozen?

This snapshot preserves the exact configuration that successfully trained the Helix 5.1B specialists. If you need to:
- Retrain a specialist from scratch
- Experiment with different base models
- Add more training examples
- Reproduce the results

You can use these materials as a known-good baseline.

## 📝 Notes

- Corpora are in instruction-response format
- All examples include format hints and explanations
- Training automatically saves checkpoints
- Phase 1 checkpoint is preserved before Phase 2
- Final models saved to `/home/matt/hlx-dev-studio/models/`

---

**Created**: December 19, 2025
**Status**: Production-tested, working configuration
**Purpose**: Archival and reproducibility
