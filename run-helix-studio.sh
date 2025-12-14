#!/bin/bash
# Helix Studio Launcher
cd "$(dirname "$0")/release/linux-unpacked"
./helix-studio --no-sandbox "$@"
