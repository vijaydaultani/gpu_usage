# Feature Comparison: GPU Monitor vs Claude Usage Monitor

Both apps now share the same battery-saving and user experience features.

## ✅ Identical Features

### 1. **Refresh Interval**
- **Default:** 5 minutes (300 seconds)
- **Configurable:** Set `GPU_REFRESH_INTERVAL` in config file
- **Battery friendly:** Less frequent checks = better battery life

### 2. **App Icon Behavior**
- ✅ **Hidden from Dock** - Won't show in the Dock
- ✅ **Hidden from Cmd+Tab** - Won't appear in app switcher
- ✅ **Menu bar only** - Uses `NSApplicationActivationPolicyAccessory`

### 3. **Sleep Mode Detection**
- ✅ **Stops timer during sleep** - `timer.invalidate()` when system sleeps
- ✅ **No background activity** - Timer is completely stopped, not paused
- ✅ **Automatic resume** - Restarts immediately on wake
- ✅ **Immediate refresh** - Updates data right after wake
- ✅ **Battery optimized** - No CPU/network usage during sleep

### 4. **Implementation Details**

Both apps use:
- `NSWorkspace` notifications for sleep/wake detection
- `NSWorkspaceWillSleepNotification` - triggers before sleep
- `NSWorkspaceDidWakeNotification` - triggers after wake
- `NSTimer.invalidate()` - completely stops the timer
- Thread-safe locking for data fetching

## Configuration Comparison

### Claude Usage Monitor
```bash
# Hard-coded 5 minute refresh
Timer: 300 seconds (5 minutes)
```

### GPU Monitor
```bash
# Configurable refresh interval (default: 5 minutes)
GPU_REFRESH_INTERVAL=300  # 5 minutes (default)
GPU_REFRESH_INTERVAL=600  # 10 minutes (even more battery friendly)
GPU_REFRESH_INTERVAL=60   # 1 minute (more responsive)
```

## Battery Impact

With 5-minute refresh interval:
- **12 checks per hour** (vs 120 with 30-second interval)
- **~288 checks per day** (vs 2,880 with 30-second interval)
- **90% reduction** in network requests
- **90% reduction** in SSH connections
- **Minimal battery impact** - comparable to system status items

## Summary

✅ Your GPU Monitor now has **all the same features** as Claude Usage Monitor:
- 5-minute refresh interval
- Hidden from app switcher
- Full sleep detection
- Battery optimized
- Clean menubar-only presence

The only difference is GPU Monitor gives you **more control** through the config file! 🎯
