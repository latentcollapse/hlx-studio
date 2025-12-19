#!/bin/bash
# Startup script for Helix 5.1B Brain Service
# Auto-starts with HLX Dev Studio

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BRAIN_DIR="$SCRIPT_DIR/hlxl_brain"
PIDFILE="$SCRIPT_DIR/.helix_brain.pid"
LOGFILE="$SCRIPT_DIR/helix_brain.log"

# Kill existing instance if running
if [ -f "$PIDFILE" ]; then
    OLD_PID=$(cat "$PIDFILE")
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo "Stopping existing Helix brain (PID: $OLD_PID)..."
        kill $OLD_PID 2>/dev/null
        sleep 2
    fi
    rm -f "$PIDFILE"
fi

echo "Starting Helix 5.1B Brain Service..."
echo "Logs: $LOGFILE"

# Start service in background
cd "$BRAIN_DIR"
nohup python3 helix_5_1b_service.py --port 5001 > "$LOGFILE" 2>&1 &
echo $! > "$PIDFILE"

echo "Helix brain started (PID: $(cat $PIDFILE))"
echo "Service available at http://localhost:5001"

# Wait for service to be ready
echo "Waiting for service to initialize..."
for i in {1..30}; do
    if curl -s http://localhost:5001/health > /dev/null 2>&1; then
        echo "✓ Helix 5.1B brain is ready!"
        exit 0
    fi
    sleep 1
done

echo "⚠ Service may still be loading models..."
echo "Check logs at: $LOGFILE"
