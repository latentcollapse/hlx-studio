#!/bin/bash
# Master launcher for HLX Dev Studio
# Starts Helix 5.1B brain + frontend

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║            HLX Dev Studio - Launch Sequence              ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Start Helix Brain
echo "[1/2] Starting Helix 5.1B Brain..."
"$SCRIPT_DIR/start_helix_brain.sh"

if [ $? -ne 0 ]; then
    echo "✗ Failed to start Helix brain"
    exit 1
fi

echo ""

# Step 2: Start Frontend
echo "[2/2] Launching HLX Dev Studio frontend..."
cd "$SCRIPT_DIR/frontend"

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              HLX Dev Studio is launching...              ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "Frontend: http://localhost:5173"
echo "Brain API: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop both services."
echo ""

# Start frontend (this blocks)
npm run dev
