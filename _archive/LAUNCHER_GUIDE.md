# HLX Dev Studio Launcher Guide

## Quick Start

You now have a desktop launcher for HLX Dev Studio! Here's how to use it:

### Method 1: Desktop File (Recommended)

The launcher is installed at:
```
~/.local/share/applications/hlx-dev-studio.desktop
```

**To use it:**

1. Search for "HLX Dev Studio" in your application menu (KDE: press Super key and type "HLX")
2. Click the icon to launch
3. Or right-click and "Add to Favorites" to pin to taskbar

### Method 2: Direct Script Execution

Run from terminal:
```bash
/home/matt/hlx-dev-studio/launch-studio.sh
```

Or from anywhere:
```bash
./launch-studio.sh
```

## What It Does

The launcher automatically:
1. Kills any old instances of the studio
2. Starts the Python backend server (port 58300)
3. Starts the Bun frontend dev server (port 3001)
4. Opens your browser to http://localhost:3001/
5. Keeps running in a terminal window
6. Handles cleanup when you press Ctrl+C

## Customizing the Icon

### Replace with Your Own Icon

The current icon is at: `/home/matt/hlx-dev-studio/icon.png`

**To use a different icon:**

1. Place your custom icon (PNG format, 512x512 recommended) at:
   ```bash
   /home/matt/hlx-dev-studio/icon.png
   ```

2. Or edit the desktop file to point to a different location:
   ```bash
   nano ~/.local/share/applications/hlx-dev-studio.desktop
   ```
   
   Change the `Icon=` line to your icon path.

3. Refresh the desktop database:
   ```bash
   update-desktop-database ~/.local/share/applications/
   ```

### Icon Requirements

- Format: PNG (recommended), SVG also works
- Size: 512x512 or larger recommended
- Location: Can be anywhere, just update the desktop file path

## Pinning to Taskbar

### KDE Plasma:

1. Open application menu (Super key)
2. Search for "HLX Dev Studio"
3. Right-click the icon
4. Select "Add to Favorites" or "Pin to Task Manager"

### GNOME:

1. Open Activities (Super key)
2. Search for "HLX Dev Studio"
3. Right-click and select "Add to Favorites"

## Logs

If something goes wrong, check the logs:

```bash
# Backend logs
tail -f /tmp/hlx_backend.log

# Frontend logs
tail -f /tmp/hlx_dev_studio.log
```

## Stopping the Studio

- If launched from desktop: Close the terminal window or press Ctrl+C
- If instances are stuck: The launcher auto-kills old instances on next launch
- Manual cleanup:
  ```bash
  pkill -f "python.*hlx_backend"
  pkill -f "bun.*vite"
  ```

## URLs

Once running, access:

- Frontend UI: http://localhost:3001/
- Backend API: http://127.0.0.1:58300
- Brain API: http://127.0.0.1:58300/brain/status
- API Docs: http://127.0.0.1:58300/docs

## Troubleshooting

### Launcher not appearing in menu?

```bash
update-desktop-database ~/.local/share/applications/
```

### Icon not showing?

Make sure `/home/matt/hlx-dev-studio/icon.png` exists and is a valid PNG file:
```bash
file /home/matt/hlx-dev-studio/icon.png
```

### Services not starting?

Check dependencies:
```bash
which python3  # Should be /usr/bin/python3
which bun      # Should be /home/matt/.bun/bin/bun
```

### Port conflicts?

If port 3001 or 58300 are already in use, the launcher will fail. Kill conflicting processes:
```bash
lsof -i :3001
lsof -i :58300
```

## Files Created

```
/home/matt/hlx-dev-studio/launch-studio.sh          # Main launcher script
/home/matt/hlx-dev-studio/icon.png                   # Default icon (blue with "HLX")
~/.local/share/applications/hlx-dev-studio.desktop   # Desktop entry file
```

## Next Steps

- Customize the icon to your liking
- Pin to taskbar for easy access
- Share the launcher with your team (just copy the 3 files above)
