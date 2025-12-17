# HLX Dev Studio - Native App Quick Start

## Launch the Application

### Option 1: Simple Script (Recommended)
```bash
/home/matt/hlx-dev-studio/launch-studio.sh
```

This will:
- Start the Python backend service
- Launch the native Tauri desktop application
- Display logs for monitoring

### Option 2: Direct Binary
```bash
/home/matt/hlx-dev-studio/src-tauri/target/release/hlx-dev-studio
```

Note: This requires the backend service to be running separately.

### Option 3: From Application Menu
1. Copy the desktop file:
   ```bash
   cp /home/matt/hlx-dev-studio/hlx-dev-studio.desktop ~/.local/share/applications/
   ```
2. Search for "HLX Dev Studio" in your application menu
3. Click to launch

---

## What You're Getting

### A True Native Application
- **Not a browser window** - It's a real desktop app using Tauri
- **Not Electron** - Uses system WebKit (13 MB vs 300+ MB)
- **Native UI** - GTK3 window manager integration
- **System integration** - Works with your desktop environment

### Key Improvements Over Dev Server
| Aspect | Dev Server | Native App |
|--------|-----------|-----------|
| Size | N/A | 13 MB |
| Memory | High (Node.js) | Low (native) |
| Startup | Slow | Fast |
| Look & Feel | Browser | Native |
| Distribution | Complex | Simple .deb/.rpm |

---

## Backend Service

The Python backend still runs as a separate service at:
- **URL**: http://127.0.0.1:58300
- **Brain API**: http://127.0.0.1:58300/brain
- **Started by**: launch-studio.sh script
- **Logs**: `/tmp/hlx_backend.log`

---

## Stopping the Application

### Via Script
- Press `Ctrl+C` in the terminal where you ran `launch-studio.sh`
- Or just close the application window

### Manual Cleanup
```bash
# Kill the app
pkill -f "hlx-dev-studio"

# Kill the backend
pkill -f "python.*hlx_backend"

# View logs
tail -f /tmp/hlx_backend.log
```

---

## Distributing the Application

### For Debian/Ubuntu Systems
```bash
# Install
sudo apt install /path/to/"HLX Dev Studio_1.0.1_amd64.deb"

# Later uninstall
sudo apt remove hlx-dev-studio
```

Location: `/home/matt/hlx-dev-studio/src-tauri/target/release/bundle/deb/`

### For RedHat/Fedora Systems
```bash
# Install
sudo dnf install /path/to/"HLX Dev Studio-1.0.1-1.x86_64.rpm"

# Later uninstall
sudo dnf remove hlx-dev-studio
```

Location: `/home/matt/hlx-dev-studio/src-tauri/target/release/bundle/rpm/`

---

## Troubleshooting

### App Won't Launch
Check if dependencies are available:
```bash
ldd /home/matt/hlx-dev-studio/src-tauri/target/release/hlx-dev-studio | grep "not found"
```

If anything shows as "not found", install the missing library.

### Backend Service Fails to Start
Check the log:
```bash
tail -50 /tmp/hlx_backend.log
```

Ensure Python and required packages are installed:
```bash
cd /home/matt/hlx-dev-studio
python hlx_backend/server.py
```

### Port Already in Use
If port 58300 is in use:
```bash
lsof -i :58300
# Kill the process using the port
kill -9 <PID>
```

---

## Development Changes

### To Modify the Frontend
1. Edit files in `/home/matt/hlx-dev-studio/` (React components, etc.)
2. Run `bun run tauri:build` to rebuild
3. Relaunch the app

### To Modify the Backend
1. Edit files in `/home/matt/hlx-dev-studio/hlx_backend/`
2. Restart the backend service
3. No need to rebuild the native app

### To Update Version
1. Edit version in:
   - `/home/matt/hlx-dev-studio/src-tauri/tauri.conf.json`
   - `/home/matt/hlx-dev-studio/src-tauri/Cargo.toml`
   - `/home/matt/hlx-dev-studio/package.json`
2. Run `bun run tauri:build`

---

## System Requirements

### Minimum
- Linux (x86_64 architecture)
- GTK 3.0+
- WebKit2GTK 4.1+
- 2 GB RAM
- 50 MB disk space for app + dependencies

### Tested On
- Ubuntu 22.04+
- Fedora 39+
- Any modern Linux distribution with GTK3 support

### Dependencies Installed Automatically
- libgtk-3-0
- libwebkit2gtk-4.1-0
- libjavascriptcoregtk-4.1-0
- libcairo2
- libpango-1.0-0

---

## Architecture

```
User Interaction
      ↓
┌─────────────────────────────────────┐
│   Native Tauri Application          │  ← This is what you launch
│   (GTK3 Window + System Integration) │
├─────────────────────────────────────┤
│   React + TypeScript Frontend       │  ← Your UI components
│   (Bundled in the binary)           │
├─────────────────────────────────────┤
│   Tauri Runtime                     │  ← Bridge to system
│   (Window management, IPC)          │
├─────────────────────────────────────┤
│   System Libraries                  │  ← Shared by OS
│   WebKit2GTK, GTK3, GLib            │
└─────────────────────────────────────┘
      ↓
┌─────────────────────────────────────┐
│   Python Backend Service            │  ← Separate process
│   (HLX Brain, compilation)          │  ← Port 58300
│   (Separate from the desktop app)   │
└─────────────────────────────────────┘
```

---

## File Locations Reference

| Item | Path |
|------|------|
| **Native Binary** | `/home/matt/hlx-dev-studio/src-tauri/target/release/hlx-dev-studio` |
| **Launch Script** | `/home/matt/hlx-dev-studio/launch-studio.sh` |
| **Desktop Entry** | `/home/matt/hlx-dev-studio/hlx-dev-studio.desktop` |
| **Source Config** | `/home/matt/hlx-dev-studio/src-tauri/tauri.conf.json` |
| **Rust Backend** | `/home/matt/hlx-dev-studio/src-tauri/src/` |
| **React Frontend** | `/home/matt/hlx-dev-studio/` (source) |
| **Built Frontend** | `/home/matt/hlx-dev-studio/dist/` |
| **DEB Package** | `/home/matt/hlx-dev-studio/src-tauri/target/release/bundle/deb/` |
| **RPM Package** | `/home/matt/hlx-dev-studio/src-tauri/target/release/bundle/rpm/` |
| **Backend Logs** | `/tmp/hlx_backend.log` |
| **Documentation** | `/home/matt/hlx-dev-studio/TAURI_BUILD_SUMMARY.md` |

---

## Getting Help

### Check the Full Documentation
```bash
cat /home/matt/hlx-dev-studio/TAURI_BUILD_SUMMARY.md
```

### View Application Logs
```bash
# Backend logs
tail -f /tmp/hlx_backend.log

# Check if app is running
pgrep -a "hlx-dev-studio"
```

### Test the Backend Independently
```bash
cd /home/matt/hlx-dev-studio
python hlx_backend/server.py
# Then test: curl http://127.0.0.1:58300/brain/status
```

---

## Success Indicators

You'll know everything is working when:
- [x] A native desktop window appears (not a browser)
- [x] The UI matches your React components
- [x] Backend API calls work (try the Brain features)
- [x] Window can be resized and moved normally
- [x] Close button works properly
- [x] Application appears in system window manager

Enjoy your native HLX Dev Studio application!
