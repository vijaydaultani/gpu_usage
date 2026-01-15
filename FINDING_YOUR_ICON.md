# Finding Your GPU Monitor Icon

## What to Look For

Your GPU monitor appears in the **macOS menu bar** (top-right of screen) with:

### 🔍 **Look for: "GPU" text label**

The app now shows **" GPU"** text next to the icon to make it easy to identify!

### Icon Appearance

The icon shows **two vertical bars** side by side:
- **Left bar** = GPU 0
- **Right bar** = GPU 1

### Current State (0% Utilization)

Since both your GPUs are currently idle (0% utilization), the icon shows:
- Two **gray bars** with borders
- Empty bars (no colored fill)

### What Colors Mean

As GPU utilization increases, the bars fill from bottom to top:
- **Green** = Low load (0-50%)
- **Orange** = Medium load (50-80%)
- **Red** = High load (80-100%)

## Sample Icons

I've created visual samples in `./icon_samples/`:

```
icon_samples/
├── 0%_0%_idle.png      ← What you see now (gray empty bars)
├── 25%_30%_low.png     ← Light green fill
├── 60%_70%_medium.png  ← Orange fill
└── 85%_95%_high.png    ← Red fill
```

## Quick Test

To make the icon more visible temporarily, you can test it by running a GPU workload on ganesha, or I can show you how to temporarily display it with fake high utilization.

## If You Still Can't Find It

### Option 1: Click All Unknown Icons
Click on icons in your menubar you don't recognize - the GPU monitor will show:
```
GPU Monitor - ganesha
Updated: HH:MM:SS
────────────────
GPU 0: NVIDIA RTX PRO 6000...
```

### Option 2: Remove the Label (Icon Only)
If you prefer icon-only mode, create `~/.gpu_monitor_config`:
```bash
GPU_SHOW_LABEL=false
```
Then restart the app.

### Option 3: Check Running Apps
```bash
# The app is running (we verified this)
ps aux | grep gpu_usage_menubar | grep -v grep

# Should show the process
```

### Option 4: Force Refresh
Click the icon (once you find it) and select "Refresh Now" to see the timestamp update.

## Making It More Visible

### Add More Text to Label
Edit `src/gpu_usage_menubar/app.py` line 320:
```python
self.statusitem.setTitle_(" GPU: 0%/0%")  # Show utilization in label
```

### Use a Different Icon Style
We can create:
- A distinctive shape (circle, triangle, etc.)
- Add "G" letter overlay
- Use bright colors even at 0%
- Show numbers directly in the icon

## Current Configuration

Your app is running with:
- **Label:** "GPU" (enabled by default)
- **Icon:** Two vertical gray bars
- **Server:** ganesha
- **Refresh:** Every 30 seconds

## Position in Menu Bar

Menu bar icons appear **right-to-left** order:
1. System icons (WiFi, Battery, Clock) - far right
2. Third-party apps - middle
3. Your GPU monitor - **look in the middle section**

The icon should be somewhere between the system icons and your other apps!

---

**Pro tip:** Look for any icon with two small vertical rectangles and the text "GPU" next to it. That's yours! 🎯
