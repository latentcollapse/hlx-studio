#!/bin/bash
# HLX Dev Studio Launcher
cd "$(dirname "$0")/release/linux-unpacked"
./hlx-dev-studio --no-sandbox "$@"
