# Installation Complete! 🎉

Your GPU Usage Monitor is now successfully installed and running!

## Installation Summary

✅ **Micromamba environment created** at `./mamba-env`
✅ **Python 3.14** with all dependencies installed
✅ **PyObjC and Pillow** installed for native macOS integration
✅ **LaunchAgent configured** for auto-start on login
✅ **Application running** in the background

## What's Running

Check your **menu bar** (top-right corner of your screen) for the GPU monitor icon:
- Two vertical bars showing GPU 0 (left) and GPU 1 (right)
- Colors indicate load: **Green** (low) → **Orange** (medium) → **Red** (high)

## Your Configuration

- **Server:** ganesha
- **GPUs:** 2x NVIDIA RTX PRO 6000 Blackwell Max-Q
- **Refresh interval:** 30 seconds (default)
- **Environment:** Micromamba at `./mamba-env`

## Quick Commands

### Check if running
```bash
ps aux | grep gpu_usage_menubar | grep -v grep
```

### View logs
```bash
# Errors
cat /tmp/gpu-usage-menubar.err

# Output
cat /tmp/gpu-usage-menubar.out
```

### Restart the app
```bash
launchctl unload ~/Library/LaunchAgents/com.gpumonitor.menubar.plist
launchctl load ~/Library/LaunchAgents/com.gpumonitor.menubar.plist
```

### Stop the app
```bash
launchctl unload ~/Library/LaunchAgents/com.gpumonitor.menubar.plist
```

### Uninstall completely
```bash
./scripts/uninstall.sh
```

## Customization

To customize settings, create `~/.gpu_monitor_config`:

```bash
# Server settings
GPU_SERVER_HOST=ganesha
GPU_SERVER_USER=your_username  # Optional

# Refresh rate (in seconds)
GPU_REFRESH_INTERVAL=15  # Faster updates

# Debug logging
DEBUG_LOGGING=1
```

After changing config, restart the app.

## What's in the Menu

Click the icon to see:
- **Server name** and last update time
- **GPU 0 metrics:**
  - Utilization bar (%)
  - Memory bar (% with MB used/total)
  - Temperature (°C) and Power (W)
- **GPU 1 metrics:** (same as above)
- **Refresh Now** button
- **Quit** button

## Troubleshooting

### Icon doesn't appear?
Wait 5-10 seconds for initial connection to server.

### Red X icon showing?
Check SSH connection: `ssh ganesha "nvidia-smi"`

### Want to monitor a different server?
```bash
echo "GPU_SERVER_HOST=other_server" > ~/.gpu_monitor_config
launchctl unload ~/Library/LaunchAgents/com.gpumonitor.menubar.plist
launchctl load ~/Library/LaunchAgents/com.gpumonitor.menubar.plist
```

## Next Steps

1. **Check your menu bar** - The icon should be visible now!
2. **Click the icon** - See detailed GPU metrics
3. **Test manual refresh** - Click "Refresh Now"
4. **Customize if needed** - Edit `~/.gpu_monitor_config`

## Files Created

```
gpu_usage/
├── mamba-env/                          # Micromamba environment
├── src/gpu_usage_menubar/              # Source code
├── scripts/                            # Installation scripts
├── config/settings.env.example         # Config template
├── environment.yml                     # Conda environment spec
└── ~/Library/LaunchAgents/
    └── com.gpumonitor.menubar.plist   # Auto-start config
```

## Support

- Full documentation: [README.md](README.md)
- Quick start guide: [QUICKSTART.md](QUICKSTART.md)
- Test connection: `./scripts/test_connection.sh`

---

**Enjoy monitoring your GPUs!** 🖥️✨

The app will automatically start when you log in to your Mac.
