#!/bin/bash
# HLX Dev Studio Launcher - Native Desktop Application
# Launches the native Tauri desktop application with backend support

set -e

STUDIO_DIR="/home/matt/hlx-dev-studio"
NATIVE_BINARY="$STUDIO_DIR/src-tauri/target/release/hlx-dev-studio"
cd "$STUDIO_DIR"

# Color output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  HLX Dev Studio - Native App          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"

# Check if native binary exists
if [ ! -f "$NATIVE_BINARY" ]; then
    echo -e "${RED}Error: Native binary not found at $NATIVE_BINARY${NC}"
    echo ""
    echo "Please build the native app first:"
    echo "  cd $STUDIO_DIR"
    echo "  /home/matt/.bun/bin/bun run tauri:build"
    exit 1
fi

# Kill any existing instances
echo -e "${YELLOW}Cleaning up old instances...${NC}"
pkill -f "python.*hlx_backend" || true
pkill -f "hlx-dev-studio" || true
sleep 1

# Start backend
echo -e "${GREEN}[1/2] Starting backend server...${NC}"
nohup python hlx_backend/server.py > /tmp/hlx_backend.log 2>&1 &
BACKEND_PID=$!
sleep 3

echo ""
echo -e "${GREEN}✓ HLX Dev Studio is starting!${NC}"
echo ""
echo "  Backend:  http://127.0.0.1:58300"
echo "  Brain:    http://127.0.0.1:58300/brain/status"
echo ""
echo "  Backend Log: tail -f /tmp/hlx_backend.log"
echo ""
echo -e "${BLUE}Launching native desktop application...${NC}"

# Launch the native Tauri app
echo -e "${GREEN}[2/2] Launching native desktop app...${NC}"
"$NATIVE_BINARY" &
APP_PID=$!

echo ""
echo -e "${GREEN}✓ HLX Dev Studio native app launched (PID: $APP_PID)${NC}"
echo ""
echo -e "${BLUE}This is a true native desktop application using Tauri's webview.${NC}"
echo -e "${BLUE}It's much lighter than Electron and integrates with your system.${NC}"
echo ""
echo -e "${GREEN}Press Ctrl+C to stop the backend, or just close the app window.${NC}"
echo ""

# Keep script alive and handle cleanup
cleanup() {
    echo ""
    echo -e "${BLUE}Shutting down HLX Dev Studio...${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    pkill -f "python.*hlx_backend" || true
    pkill -f "hlx-dev-studio" || true
    echo -e "${GREEN}✓ Studio stopped${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Wait for processes
wait $BACKEND_PID 2>/dev/null || true
wait $APP_PID 2>/dev/null || true
