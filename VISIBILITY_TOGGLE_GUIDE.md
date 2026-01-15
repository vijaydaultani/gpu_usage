# GPU Monitor - Visibility Toggle Guide

## ✅ New Feature: Toggle Cmd+Tab Visibility from Menu

You can now control whether GPU Monitor appears in Cmd+Tab and Launchpad **directly from the menubar**!

## How to Use

### Step 1: Click the GPU Monitor Icon
Click on the GPU monitor icon in your menubar (the two vertical bars).

### Step 2: Look for the Visibility Option
In the menu, you'll see one of these options:
- **"Hide from Cmd+Tab"** - If the app is currently visible
- **"Show in Cmd+Tab"** - If the app is currently hidden

### Step 3: Click to Toggle
Click the visibility option to toggle the setting.

### Step 4: Restart Dialog
A dialog will appear asking you to restart:
- **Click "OK"** - App will automatically restart with new setting
- **Click "Cancel"** - Keep current setting, no restart

## What the Options Mean

### "Hide from Cmd+Tab"
When you select this:
- ✅ App only appears in **menubar** (minimal presence)
- ❌ Hidden from **Cmd+Tab** app switcher
- ❌ Hidden from **Dock**
- ❌ Hidden from **Launchpad**
- ✅ Still launchable from **Applications folder**
- ✅ Still launchable from **Spotlight**

**Best for:** Users who want the app to stay out of the way

### "Show in Cmd+Tab"
When you select this:
- ✅ Appears in **Cmd+Tab** app switcher
- ✅ Shows in **Dock** when running
- ✅ Visible in **Launchpad**
- ✅ Full application visibility
- ✅ Shows in **Mission Control**

**Best for:** Users who want to manage the app like a normal application

## Current Menu Structure

When you click the GPU icon, you'll see:

```
GPU Monitor - ganesha
Updated: 22:30:15
────────────────────────────────
GPU 0: NVIDIA RTX PRO 6000...
Util: ░░░░░░░░░░░░░░░░░░░░░ 0%
Mem:  ▓▓▓░░░░░░░░░░░░░░░░░░ 24%
  ...
────────────────────────────────
GPU 1: NVIDIA RTX PRO 6000...
Util: ░░░░░░░░░░░░░░░░░░░░░ 0%
Mem:  ░░░░░░░░░░░░░░░░░░░░░ 0%
  ...
────────────────────────────────
Refresh Now
Hide from Cmd+Tab          ← NEW!
────────────────────────────────
Quit GPU Monitor
```

## The Restart Process

When you toggle visibility:

1. **Dialog appears** - "Restart Required"
2. **Click OK** - App quits and restarts automatically
3. **New setting applied** - Takes effect immediately
4. **Launchpad refreshes** - If needed

The restart is automatic - you don't need to manually relaunch!

## Technical Details

The visibility is controlled by the `LSUIElement` setting in Info.plist:
- `LSUIElement = false` → Visible everywhere
- `LSUIElement = true` → Hidden from Cmd+Tab/Dock/Launchpad

This is a macOS system setting that determines app visibility.

## Note About Launchpad

**Important:** macOS links Launchpad visibility to Cmd+Tab visibility.

- If you **hide from Cmd+Tab** → Also hidden from Launchpad
- If you **show in Cmd+Tab** → Also visible in Launchpad

You cannot show in Launchpad while hiding from Cmd+Tab. This is a macOS limitation.

## Troubleshooting

### Menu option doesn't appear
Restart the app:
```bash
./scripts/restart.sh
```

### Toggle doesn't work
Check permissions and update manually:
```bash
./scripts/configure_app_visibility.sh show  # or hide
./scripts/restart.sh
```

### Launchpad doesn't update after toggle
Refresh Launchpad:
```bash
defaults write com.apple.dock ResetLaunchPad -bool true
killall Dock
```

## Quick Reference

| Action | Steps |
|--------|-------|
| Hide from Cmd+Tab | Click icon → "Hide from Cmd+Tab" → OK |
| Show in Cmd+Tab | Click icon → "Show in Cmd+Tab" → OK |
| Check current setting | Look at the menu option text |

## Recommendations

**For most users:** Keep it visible (show in Cmd+Tab)
- Easier to find and manage
- Can launch from Launchpad
- Shows in app switcher

**For minimal setup:** Hide from Cmd+Tab
- Only appears in menubar
- Less clutter in app switcher
- Still accessible from Spotlight

---

**The toggle is now in your menubar menu!** Just right-click (or left-click) the GPU icon to access it. 🎯
