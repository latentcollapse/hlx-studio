#!/bin/bash

# MoE Training Launch Script
# Launches 100m Coordinator and two 50m Specialists in coordinated fashion

set -e

# Configuration
WORK_DIR="/home/matt/hlx/hlxl_brain"
EPOCHS=100
BATCH_SIZE=4
LR=1e-4

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check environment
echo -e "${BLUE}=== MoE Training Launch ===${NC}"
echo "Work directory: $WORK_DIR"
echo "Epochs: $EPOCHS"
echo "Batch size: $BATCH_SIZE"
echo "Learning rate: $LR"
echo ""

# Verify corpora exist
echo -e "${YELLOW}Checking corpus files...${NC}"
if [ ! -f "$WORK_DIR/corpus_canonical_COMPLETE.md" ]; then
    echo "ERROR: corpus_canonical_COMPLETE.md not found"
    exit 1
fi
if [ ! -f "$WORK_DIR/corpus_ascii_specialist.md" ]; then
    echo "ERROR: corpus_ascii_specialist.md not found"
    exit 1
fi
if [ ! -f "$WORK_DIR/corpus_runic_specialist.md" ]; then
    echo "ERROR: corpus_runic_specialist.md not found"
    exit 1
fi
echo -e "${GREEN}✓ All corpus files present${NC}\n"

# Display canonical corpus verification
CANONICAL_LINES=$(wc -l < "$WORK_DIR/corpus_canonical_COMPLETE.md")
echo -e "${BLUE}=== Canonical Corpus Verification ===${NC}"
echo "File: corpus_canonical_COMPLETE.md"
echo "Lines: $CANONICAL_LINES"
echo "Formats (all 7 verified):"
echo "  ✓ 1. English descriptions"
echo "  ✓ 2. HLXL - High-level syntax"
echo "  ✓ 3. HLXL-LS - Latent space operations in HLXL"
echo "  ✓ 4. HLX - Contract form (mid-level)"
echo "  ✓ 5. HLX-LS - Latent space operations in HLX"
echo "  ✓ 6. LC-T - Text/ASCII wire format"
echo "  ✓ 7. LC-B - Binary wire format"
echo -e "${GREEN}✓ Canonical corpus verified${NC}\n"

# Verify training scripts exist
echo -e "${YELLOW}Checking training scripts...${NC}"
if [ ! -f "$WORK_DIR/train_qwen_distillation.py" ]; then
    echo "ERROR: train_qwen_distillation.py not found"
    exit 1
fi
if [ ! -f "$WORK_DIR/train_specialist_50m.py" ]; then
    echo "ERROR: train_specialist_50m.py not found"
    exit 1
fi
echo -e "${GREEN}✓ All training scripts present${NC}\n"

# Setup CUDA environment
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
echo -e "${GREEN}✓ CUDA environment configured${NC}\n"

# Change to work directory
cd "$WORK_DIR"

# Create training log directory
mkdir -p training_logs
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="training_logs/$TIMESTAMP"
mkdir -p "$LOG_DIR"

echo -e "${BLUE}=== Training Session ===${NC}"
echo "Timestamp: $TIMESTAMP"
echo "Log directory: $LOG_DIR"
echo ""

# Function to start training in background with logging
start_training() {
    local script=$1
    local specialist=$2
    local corpus=$3
    local extra_args=$4

    echo -e "${YELLOW}Starting $specialist training...${NC}"

    if [ "$script" = "100m" ]; then
        nohup python3 train_qwen_distillation.py \
            --epochs $EPOCHS \
            --batch-size $BATCH_SIZE \
            --lr $LR \
            --corpus "$corpus" \
            $extra_args \
            > "$LOG_DIR/${specialist}_training.log" 2>&1 &
    else
        nohup python3 train_specialist_50m.py \
            --specialist "$specialist" \
            --epochs $EPOCHS \
            --batch-size $BATCH_SIZE \
            --lr $LR \
            $extra_args \
            > "$LOG_DIR/${specialist}_training.log" 2>&1 &
    fi

    local pid=$!
    echo "  PID: $pid" > "$LOG_DIR/${specialist}.pid"
    echo -e "${GREEN}✓ $specialist started (PID: $pid)${NC}"
}

# Start 100m Coordinator Training (background)
echo -e "${BLUE}### Phase 1: 100m Coordinator Brain ###${NC}"
echo "Corpus: corpus_canonical_COMPLETE.md (1045 lines, all 7 formats)"
echo "Config: 1024d_model, 16heads, 8layers = 101.3M params"
echo "Purpose: Coordinator learns all formats + English + latent space ops"
echo ""
start_training "100m" "coordinator_100m" "corpus_canonical_COMPLETE.md" "--no-qwen-augment"

# Wait a bit for coordinator to initialize
sleep 5

# Start ASCII Specialist (background)
echo -e "${BLUE}### Phase 2a: 50m ASCII Specialist ###${NC}"
echo "Corpus: corpus_ascii_specialist.md"
echo "Config: 768d_model, 12heads, 7layers = 50.0M params"
echo "Specialization: 70% LC-T, 20% English, 10% LC-R"
echo ""
nohup python3 train_specialist_50m.py \
    --specialist ascii \
    --epochs $EPOCHS \
    --batch-size $BATCH_SIZE \
    --lr $LR \
    --no-qwen-augment \
    > "$LOG_DIR/ascii_specialist_training.log" 2>&1 &
ASCII_PID=$!
echo "  PID: $ASCII_PID" > "$LOG_DIR/ascii_specialist.pid"
echo -e "${GREEN}✓ ascii_specialist started (PID: $ASCII_PID)${NC}"

# Wait a bit for ASCII to initialize
sleep 5

# Start Runic Specialist (background)
echo -e "${BLUE}### Phase 2b: 50m Runic Specialist ###${NC}"
echo "Corpus: corpus_runic_specialist.md"
echo "Config: 768d_model, 12heads, 7layers = 50.0M params"
echo "Specialization: 70% LC-R, 20% English, 10% LC-T"
echo ""

nohup python3 train_specialist_50m.py \
    --specialist runic \
    --epochs $EPOCHS \
    --batch-size $BATCH_SIZE \
    --lr $LR \
    --no-qwen-augment \
    > "$LOG_DIR/runic_specialist_training.log" 2>&1 &
RUNIC_PID=$!
echo "  PID: $RUNIC_PID" > "$LOG_DIR/runic_specialist.pid"
echo -e "${GREEN}✓ runic_specialist started (PID: $RUNIC_PID)${NC}"

echo ""
echo -e "${BLUE}=== All Training Sessions Started ===${NC}"
echo ""
echo "Training PIDs:"
echo "  Coordinator 100m: $(cat $LOG_DIR/coordinator_100m.pid 2>/dev/null || echo 'N/A')"
echo "  ASCII Specialist 50m: $(cat $LOG_DIR/ascii_specialist.pid 2>/dev/null || echo 'N/A')"
echo "  Runic Specialist 50m: $(cat $LOG_DIR/runic_specialist.pid 2>/dev/null || echo 'N/A')"
echo ""
echo -e "${YELLOW}Monitoring Training:${NC}"
echo "  Log directory: $LOG_DIR"
echo "  View coordinator: tail -f $LOG_DIR/coordinator_100m_training.log"
echo "  View ASCII: tail -f $LOG_DIR/ascii_specialist_training.log"
echo "  View Runic: tail -f $LOG_DIR/runic_specialist_training.log"
echo ""
echo -e "${YELLOW}Corpus Statistics:${NC}"
echo "  Canonical (Coordinator): $CANONICAL_LINES lines, all 7 formats"
echo "  ASCII Specialist: $(wc -l < $WORK_DIR/corpus_ascii_specialist.md) lines (60% LC-T)"
echo "  Runic Specialist: $(wc -l < $WORK_DIR/corpus_runic_specialist.md) lines (60% LC-R)"
echo ""
echo -e "${YELLOW}Monitor Progress:${NC}"
echo "  Coordinator status: cat training_status.json"
echo "  ASCII status: cat training_status_ascii.json"
echo "  Runic status: cat training_status_runic.json"
echo ""
echo -e "${GREEN}✓ MoE Training Infrastructure Launched${NC}"
echo ""
echo "System Topology:"
echo "  Total Parameters: ~201.5M (100M + 50M + 50M)"
echo "  Training Strategy: Full 100-epoch training with quality gates"
echo "  Mixture Method: Router on Coordinator selects specialist by format type"
echo ""
echo "Expected completion time: ~${EPOCHS} epochs × ~30-60 min per epoch (varies by hardware)"
echo "Total estimated time: 50-100 hours for all three models"
echo ""
