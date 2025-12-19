#!/bin/bash
# Stop Helix 5.1B Brain Service

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PIDFILE="$SCRIPT_DIR/.helix_brain.pid"

if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    if ps -p $PID > /dev/null 2>&1; then
        echo "Stopping Helix 5.1B brain (PID: $PID)..."
        kill $PID
        sleep 2

        # Force kill if still running
        if ps -p $PID > /dev/null 2>&1; then
            echo "Force killing..."
            kill -9 $PID
        fi

        echo "✓ Helix brain stopped"
    else
        echo "Helix brain not running (stale PID file)"
    fi
    rm -f "$PIDFILE"
else
    echo "Helix brain not running (no PID file)"
fi
