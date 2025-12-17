# KDE Wayland Graphics Fix for HLX Dev Studio

## Problem

The Tauri native app shows a grey/blank window on KDE Wayland due to a **GBM (Generic Buffer Management) error**:

```
Failed to create GBM buffer of size 1400x900: Invalid argument
```

This is a known compatibility issue between:
- KDE Plasma Wayland compositor
- WebKitGTK (used by Tauri for rendering)
- Hardware-accelerated graphics

The WebView cannot create hardware-accelerated rendering buffers, resulting in no content being displayed.

## Solution

Use the provided **launch script** that disables hardware acceleration and forces X11 backend:

### From Command Line

```bash
cd /home/matt/hlx-dev-studio
./launch-native.sh
```

### From Taskbar/Application Menu

The desktop launcher has been updated to use the fix automatically. Just click the HLX Dev Studio icon.

## What the Fix Does

The `launch-native.sh` script sets two environment variables:

1. **`WEBKIT_DISABLE_COMPOSITING_MODE=1`** - Disables hardware acceleration, using software rendering instead
2. **`GDK_BACKEND=x11`** - Forces X11 backend (more stable than Wayland for WebKitGTK)

## Trade-offs

- **Performance**: Software rendering is slightly slower than hardware acceleration
- **Compatibility**: Works on all KDE Wayland systems without graphics driver issues
- **Stability**: More stable than hardware-accelerated mode on Wayland

## Alternative: Use Browser Version

If you prefer hardware acceleration and don't need native desktop features:

```bash
cd /home/matt/hlx-dev-studio
bun run dev
```

Then open http://localhost:3000 in your browser.

## Technical Details

**Root Cause**: WebKitGTK's hardware acceleration layer cannot allocate GBM buffers on certain Wayland compositors. This is a known issue with WebKitGTK 2.x on KDE Plasma Wayland.

**Future Fix**: Tauri 2.x may resolve this with improved Wayland support, or your graphics drivers may receive updates that fix the GBM buffer allocation issue.

## Files Modified

- `/home/matt/hlx-dev-studio/launch-native.sh` - Launch script with environment variables
- `/home/matt/.local/share/applications/hlx-dev-studio.desktop` - Desktop entry updated to use launch script

---

Generated: 2025-12-17
