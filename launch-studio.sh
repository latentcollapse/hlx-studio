#!/bin/bash
# HLX Dev Studio Launch Script
# Created: 2025-12-16

echo "╔════════════════════════════════════╗"
echo "║  🚀 Launching HLX Dev Studio...   ║"
echo "╚════════════════════════════════════╝"
echo ""

# Check if build exists
if [ ! -f "src-tauri/target/release/hlx-dev-studio" ]; then
    echo "❌ Error: HLX Dev Studio binary not found!"
    echo ""
    echo "Please build the app first:"
    echo "  ~/.bun/bin/bun run tauri:build"
    echo ""
    exit 1
fi

echo "✅ Found HLX Dev Studio binary"
echo "📂 Location: $(pwd)/src-tauri/target/release/hlx-dev-studio"
echo ""
echo "Starting app..."
echo ""

# Launch the app
cd src-tauri/target/release
./hlx-dev-studio --no-sandbox &

# Wait a moment and check if it started
sleep 2

if pgrep -f "hlx-dev-studio" > /dev/null; then
    echo "✅ HLX Dev Studio launched successfully!"
    echo ""
    echo "If the window doesn't appear, check for errors above."
else
    echo "❌ Warning: Process may not have started correctly"
    echo "Try running manually:"
    echo "  cd src-tauri/target/release && ./hlx-dev-studio --no-sandbox"
fi

echo ""
