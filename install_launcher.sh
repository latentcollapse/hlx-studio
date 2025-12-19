#!/bin/bash
# Install HLX Dev Studio desktop launcher for Arch Linux

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESKTOP_FILE="$SCRIPT_DIR/hlx-dev-studio.desktop"
INSTALL_DIR="$HOME/.local/share/applications"

echo "Installing HLX Dev Studio launcher..."

# Create applications directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Copy desktop file
cp "$DESKTOP_FILE" "$INSTALL_DIR/"

# Make executable
chmod +x "$INSTALL_DIR/hlx-dev-studio.desktop"

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$INSTALL_DIR"
fi

echo "✓ HLX Dev Studio launcher installed"
echo ""
echo "You can now find 'HLX Dev Studio' in your application menu."
echo "To launch from terminal: gtk-launch hlx-dev-studio.desktop"
