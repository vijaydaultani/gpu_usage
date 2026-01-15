# How to Update the GPU Monitor Icon

You've provided a beautiful GPU monitoring icon! Here's how to use it:

## Step 1: Save the Icon

Save the icon image you provided as a PNG file. For example:
- Save to: `~/Downloads/gpu_icon.png`
- Or save to: `~/Desktop/gpu_icon.png`

## Step 2: Update the App Icon

Run the update script with the path to your icon:

```bash
cd ~/work/github/gpu_usage
./scripts/update_app_icon.sh ~/Downloads/gpu_icon.png
```

This will:
1. Copy the icon to the project
2. Generate all required sizes (16x16 to 1024x1024)
3. Create an ICNS file (macOS icon format)
4. Update both app bundles (local and /Applications)

## Step 3: Refresh the Icon Cache

To make macOS recognize the new icon immediately:

```bash
# Clear icon cache
sudo rm -rf /Library/Caches/com.apple.iconservices.store

# Restart Dock
killall Dock
```

## Step 4: Restart the App

```bash
./scripts/restart.sh
```

## Result

Your new icon will appear in:
- ✅ Applications folder
- ✅ Spotlight search
- ✅ Mission Control
- ✅ Launchpad
- ✅ Dock (if kept there)

---

## Configure Cmd+Tab Visibility

By default, GPU Monitor is **hidden** from Cmd+Tab and Dock (menubar only).

### To Show in Cmd+Tab (Make it a Normal App)

```bash
./scripts/configure_app_visibility.sh show
./scripts/restart.sh
```

Now the app will:
- ✅ Appear in Cmd+Tab switcher
- ✅ Show in Dock when running
- ✅ Behave like a normal app

### To Hide from Cmd+Tab (Menubar Only)

```bash
./scripts/configure_app_visibility.sh hide
./scripts/restart.sh
```

Now the app will:
- ✅ Only show in menubar
- ✅ Hidden from Cmd+Tab
- ✅ Hidden from Dock
- ✅ Minimal presence (recommended)

### Check Current Setting

```bash
./scripts/configure_app_visibility.sh
```

---

## About the Icon

The icon you provided features:
- 🎨 Beautiful blue gradient background
- 🔲 GPU chip design with pins
- 📊 Monitoring gauge with metrics
- 💎 Professional, modern look
- ✨ Perfect for a GPU monitoring app!

This icon is much better than the simple bars we generated. It clearly represents GPU hardware and monitoring functionality.

## Quick Commands

```bash
# Update icon
./scripts/update_app_icon.sh ~/Downloads/gpu_icon.png

# Show in Cmd+Tab
./scripts/configure_app_visibility.sh show
./scripts/restart.sh

# Hide from Cmd+Tab (default)
./scripts/configure_app_visibility.sh hide
./scripts/restart.sh
```

---

**Ready to use your icon!** Just save it and run the update script. 🎨
