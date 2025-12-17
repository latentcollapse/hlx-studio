#!/usr/bin/env bash

# HLX Dev Studio Native Launcher
# Workaround for KDE Wayland + WebKitGTK graphics buffer issues

# Disable hardware acceleration to avoid GBM buffer creation errors
export WEBKIT_DISABLE_COMPOSITING_MODE=1

# Force X11 backend (more stable than Wayland for WebKitGTK)
export GDK_BACKEND=x11

# Launch the native app
exec "$(dirname "$0")/src-tauri/target/release/hlx-dev-studio" "$@"
