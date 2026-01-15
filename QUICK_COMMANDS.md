# Quick Commands - GPU Monitor

Easy commands to start, stop, and manage your GPU monitor.

## 🚀 Start / Stop Commands

### Start the monitor
```bash
./scripts/start.sh
```

### Stop the monitor
```bash
./scripts/stop.sh
```

### Restart the monitor
```bash
./scripts/restart.sh
```

### Check status
```bash
./scripts/status.sh
```

## 🖱️ Using the Menu Bar Icon

### Regular Click (Left Click)
Shows the full GPU details menu:
- Server name and update time
- GPU 0 metrics (utilization, memory, temp, power)
- GPU 1 metrics
- **Refresh Now** - Force immediate update
- **Quit GPU Monitor** - Stop the application

### Right Click (Control + Click)
Same menu as left click - all options available

### To Quit from Menu Bar
1. Click the GPU icon (two vertical bars)
2. Select **"Quit GPU Monitor"** at the bottom
3. The app will cleanly shut down

## 📁 Application Icons

Visual icons have been created in `./icons/`:
- `AppIcon.png` - Main 1024x1024 icon
- Various sizes: 512, 256, 128, 64, 32, 16

The icon shows two GPU bars:
- Left bar (orange): 60% utilization
- Right bar (red): 80% utilization

## 🔧 Other Useful Commands

### View logs
```bash
# Error log
cat /tmp/gpu-usage-menubar.err

# Output log
cat /tmp/gpu-usage-menubar.out

# Follow errors in real-time
tail -f /tmp/gpu-usage-menubar.err
```

### Check if running
```bash
ps aux | grep gpu_usage_menubar | grep -v grep
```

### Force kill (if quit doesn't work)
```bash
pkill -9 -f gpu_usage_menubar
```

### Test GPU connection
```bash
./scripts/test_connection.sh
```

## ⚙️ Configuration

Edit `~/.gpu_monitor_config`:
```bash
# Server to monitor
GPU_SERVER_HOST=ganesha

# Refresh interval (default: 300 = 5 minutes)
GPU_REFRESH_INTERVAL=300

# Show percentages in menubar (default: false)
GPU_SHOW_PERCENTAGES=false
```

After changing config:
```bash
./scripts/restart.sh
```

## 📍 File Locations

- **Scripts:** `./scripts/`
- **Icons:** `./icons/`
- **Config:** `~/.gpu_monitor_config`
- **Logs:** `/tmp/gpu-usage-menubar.{out,err}`
- **LaunchAgent:** `~/Library/LaunchAgents/com.gpumonitor.menubar.plist`

## 💡 Tips

1. **Can't find the icon?** Enable percentages temporarily:
   ```bash
   echo "GPU_SHOW_PERCENTAGES=true" > ~/.gpu_monitor_config
   ./scripts/restart.sh
   ```

2. **Want faster updates?** Change refresh interval:
   ```bash
   echo "GPU_REFRESH_INTERVAL=60" > ~/.gpu_monitor_config
   ./scripts/restart.sh
   ```

3. **Troubleshooting:** Run status check:
   ```bash
   ./scripts/status.sh
   ```

---

**Quick Start:** `./scripts/start.sh`
**Quick Stop:** `./scripts/stop.sh` OR click icon → "Quit GPU Monitor"
