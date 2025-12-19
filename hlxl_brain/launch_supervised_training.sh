#!/bin/bash
# Master training launcher with Haiku supervision
# Sonnet oversees the entire operation

echo "============================================================"
echo "Helix MoE 5.1B - Supervised 2-Phase Training"
echo "============================================================"
echo "Starting training with Haiku watchdog agents..."
echo ""

# Create logs directory
mkdir -p training_logs

# Launch ASCII specialist training in background
echo "[1/2] Launching ASCII Specialist training..."
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
python3 train_2phase_specialist.py ascii > training_logs/ascii_training.log 2>&1 &
ASCII_PID=$!
echo "  ASCII training PID: $ASCII_PID"

# Wait for ASCII to get a head start (avoid initial memory contention)
sleep 10

# Launch Runic specialist training in background
echo "[2/2] Launching Runic Specialist training..."
python3 train_2phase_specialist.py runic > training_logs/runic_training.log 2>&1 &
RUNIC_PID=$!
echo "  Runic training PID: $RUNIC_PID"

echo ""
echo "============================================================"
echo "Both training jobs launched!"
echo "============================================================"
echo "ASCII PID: $ASCII_PID"
echo "Runic PID: $RUNIC_PID"
echo ""
echo "Logs:"
echo "  ASCII: training_logs/ascii_training.log"
echo "  Runic: training_logs/runic_training.log"
echo ""
echo "Haiku watchdog agents will monitor progress."
echo "Sonnet supervisor will intervene if needed."
echo "============================================================"
echo ""
echo "Training Status:"
echo "  Phase 1: ~2 hours (75 epochs each)"
echo "  Phase 2: ~6-7 hours (250 epochs each)"
echo "  Total: ~8-9 hours"
echo ""
echo "Sleep well! Training will complete overnight."
echo "============================================================"

# Keep script alive to monitor processes
while kill -0 $ASCII_PID 2>/dev/null || kill -0 $RUNIC_PID 2>/dev/null; do
    sleep 60
done

echo ""
echo "============================================================"
echo "Training Complete!"
echo "============================================================"
echo "Check training_logs/ for details"
echo "Models saved to:"
echo "  /home/matt/hlx-dev-studio/models/qwen3_1_7b_ascii_specialist/final_model"
echo "  /home/matt/hlx-dev-studio/models/qwen3_1_7b_runic_specialist/final_model"
echo "============================================================"
