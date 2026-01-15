# GPU Monitor - App Usage Guide

You now have a **full macOS application** that can be launched from anywhere!

## 🚀 Ways to Launch

### 1. **From Applications Folder**
- Open Finder
- Go to Applications
- Double-click **"GPU Monitor.app"**

### 2. **From Spotlight** (⭐ Easiest)
- Press `Cmd + Space`
- Type "GPU Monitor"
- Press Enter

### 3. **From Mission Control**
- Press `F3` or swipe up with 3-4 fingers
- All your open apps appear
- Click on GPU Monitor icon

### 4. **From Dock** (Optional)
- Open Applications → GPU Monitor.app
- Right-click the menubar icon
- Select "Options" → "Keep in Dock"
- Now you can launch it from the Dock anytime

### 5. **From Launchpad**
- Press `F4` or pinch with thumb and three fingers
- Find "GPU Monitor" icon
- Click to launch

## 📍 What Happens When You Launch

1. **App starts** - Process begins in background
2. **Icon appears** in menubar (top-right corner)
3. **Two vertical bars** show GPU 0 and GPU 1 utilization
4. **First refresh** happens immediately
5. **Auto-refresh** every 5 minutes after that

## 🖱️ Using the Menubar Icon

### Click the Icon
Shows full menu:
```
GPU Monitor - ganesha
Updated: 22:15:30
────────────────────────────
GPU 0: NVIDIA RTX PRO 6000...
Util: ░░░░░░░░░░░░░░░░░░░░░ 0%
Mem:  ▓▓▓▓▓░░░░░░░░░░░░░░░░ 24%
  23718MB/97887MB | 43°C | 27.8W
────────────────────────────
GPU 1: NVIDIA RTX PRO 6000...
Util: ░░░░░░░░░░░░░░░░░░░░░ 0%
Mem:  ░░░░░░░░░░░░░░░░░░░░░ 0%
  4MB/97887MB | 38°C | 14.3W
────────────────────────────
Refresh Now
Quit GPU Monitor
```

### Menu Options

**Refresh Now**
- Forces immediate update from server
- Useful if you just started a GPU job

**Quit GPU Monitor**
- Cleanly stops the application
- Removes menubar icon
- Terminates all processes

## 🎨 The App Icon

The application icon shows:
- Two vertical GPU bars
- Left bar (orange): Represents moderate load
- Right bar (red): Represents high load
- Dark circular background

This icon appears in:
- Applications folder
- Spotlight search
- Mission Control
- Launchpad
- Dock (if you keep it there)

## 🔄 Auto-Start vs Manual Launch

### Current Setup
The app is configured to **auto-start on login** via LaunchAgent.

### If You Want Manual Launch Only

**Disable auto-start:**
```bash
launchctl unload ~/Library/LaunchAgents/com.gpumonitor.menubar.plist
```

**Now launch manually:**
- Double-click app from Applications
- Or use Spotlight (Cmd+Space → "GPU Monitor")

**Re-enable auto-start:**
```bash
launchctl load ~/Library/LaunchAgents/com.gpumonitor.menubar.plist
```

## 💡 Common Scenarios

### Scenario 1: Start GPU Monitor
**Option A:** Press `Cmd+Space`, type "GPU", press Enter ⭐
**Option B:** Open Applications → GPU Monitor.app
**Option C:** Click from Dock (if added)

### Scenario 2: Check GPU Status
- Click the menubar icon (two bars)
- View current utilization, memory, temp, power

### Scenario 3: Force Refresh
- Click menubar icon
- Select "Refresh Now"

### Scenario 4: Stop GPU Monitor
- Click menubar icon
- Select "Quit GPU Monitor"

### Scenario 5: Keep in Dock
- Launch the app (from Applications or Spotlight)
- Right-click the Dock icon
- Options → Keep in Dock

## 🛠️ Advanced: Command Line Control

Even with the .app, you can still use scripts:

```bash
# Start (loads LaunchAgent)
./scripts/start.sh

# Stop (unloads LaunchAgent + kills process)
./scripts/stop.sh

# Restart
./scripts/restart.sh

# Check status
./scripts/status.sh
```

## 📊 What You See in Menubar

### Icon Appearance
- **Two vertical bars** side by side
- **Colors change** based on GPU load:
  - Gray = Idle (0%)
  - Green = Low (1-50%)
  - Orange = Medium (50-80%)
  - Red = High (80-100%)

### Optional: Show Percentages
Edit `~/.gpu_monitor_config`:
```bash
GPU_SHOW_PERCENTAGES=true
```
Then restart. Now menubar shows: `[icon] 0%/0%`

## 🔍 Troubleshooting

### App doesn't appear in menubar after launch
Wait 5-10 seconds for initial connection to ganesha

### Can't find app in Spotlight
Run:
```bash
sudo mdutil -E /Applications
```
This rebuilds Spotlight index

### App icon is generic
The custom icon should appear. If not:
```bash
./scripts/create_app_bundle.sh
./scripts/install_to_applications.sh
```

### Check if running
```bash
ps aux | grep gpu_usage_menubar | grep -v grep
```

## 📁 File Locations

- **Application:** `/Applications/GPU Monitor.app`
- **Project:** `~/work/github/gpu_usage/`
- **Config:** `~/.gpu_monitor_config`
- **Logs:** `/tmp/gpu-usage-menubar.{out,err}`

## 🎯 Quick Reference

| Action | Method |
|--------|--------|
| Launch app | `Cmd+Space` → "GPU Monitor" |
| View stats | Click menubar icon |
| Refresh | Click icon → "Refresh Now" |
| Quit | Click icon → "Quit GPU Monitor" |
| Add to Dock | Launch → Right-click dock icon → Keep in Dock |

---

**You're all set!** 🎉

Press `Cmd+Space`, type "GPU Monitor", and press Enter to launch the app!
