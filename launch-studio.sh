#!/bin/bash
# Helix Studio Launch Script
# Created: 2025-12-16

echo "╔════════════════════════════════════╗"
echo "║   🚀 Launching Helix Studio...    ║"
echo "╚════════════════════════════════════╝"
echo ""

# Check if build exists
if [ ! -f "src-tauri/target/release/helix-studio" ]; then
    echo "❌ Error: Helix Studio binary not found!"
    echo ""
    echo "Please build the app first:"
    echo "  ~/.bun/bin/bun run tauri:build"
    echo ""
    exit 1
fi

echo "✅ Found Helix Studio binary"
echo "📂 Location: $(pwd)/src-tauri/target/release/helix-studio"
echo ""
echo "Starting app..."
echo ""

# Launch the app
cd src-tauri/target/release
./helix-studio --no-sandbox &

# Wait a moment and check if it started
sleep 2

if pgrep -f "helix-studio" > /dev/null; then
    echo "✅ Helix Studio launched successfully!"
    echo ""
    echo "If the window doesn't appear, check for errors above."
else
    echo "❌ Warning: Process may not have started correctly"
    echo "Try running manually:"
    echo "  cd src-tauri/target/release && ./helix-studio --no-sandbox"
fi

echo ""
