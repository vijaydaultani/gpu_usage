# Quick Start Guide - GPU Usage Monitor

Get your GPU monitor running in 5 minutes!

## Prerequisites Checklist

Before installing, ensure you have:

- [ ] macOS 10.15 or later
- [ ] Python 3.9+ (`python3 --version`)
- [ ] SSH key-based access to your GPU server
- [ ] nvidia-smi installed on the remote server

## Step 1: Test SSH Connection

First, verify you can connect to your GPU server without a password:

```bash
# Test SSH connection (should NOT ask for password)
ssh ganesha "nvidia-smi"
```

If this asks for a password, set up SSH keys first:

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519

# Copy key to server
ssh-copy-id ganesha

# Test again
ssh ganesha "nvidia-smi"
```

## Step 2: Clone and Install

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/gpu-usage-monitor.git
cd gpu-usage-monitor

# Run the installer
./scripts/install.sh
```

The installer will:
- ✅ Check Python version
- ✅ Verify SSH access to GPU server
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Set up auto-start
- ✅ Launch the app

## Step 3: Verify It's Running

Look for the GPU monitor icon in your menu bar (top right corner):
- You should see two vertical bars representing your GPUs
- Click on it to see detailed metrics

If you don't see it:

```bash
# Check if it's running
ps aux | grep gpu_usage_menubar

# Check logs for errors
cat /tmp/gpu-usage-menubar.err
```

## Step 4: Configure (Optional)

To customize the settings, create a config file:

```bash
# Copy the example configuration
cp config/settings.env.example ~/.gpu_monitor_config

# Edit with your preferences
nano ~/.gpu_monitor_config
```

Example configuration:

```bash
# GPU server hostname
GPU_SERVER_HOST=ganesha

# SSH username (optional)
GPU_SERVER_USER=your_username

# Refresh every 15 seconds (instead of default 30)
GPU_REFRESH_INTERVAL=15
```

After changing config, restart the app:

```bash
launchctl unload ~/Library/LaunchAgents/com.gpumonitor.menubar.plist
launchctl load ~/Library/LaunchAgents/com.gpumonitor.menubar.plist
```

## Troubleshooting

### Problem: Icon doesn't appear

**Solution:**
```bash
# Manually start the app to see errors
cd gpu-usage-monitor
source venv/bin/activate
python -m gpu_usage_menubar.app
```

### Problem: Shows red X (error icon)

**Solution:** Check SSH connection
```bash
# Test SSH
ssh ganesha "nvidia-smi"

# Check SSH key is loaded
ssh-add -l

# Add key if needed
ssh-add ~/.ssh/id_ed25519
```

### Problem: "Connection timeout"

**Solution:** Increase timeout in config
```bash
echo "GPU_FETCH_TIMEOUT=20" >> ~/.gpu_monitor_config
```

Then restart the app.

## Common Tasks

### Manual Refresh
Click the menubar icon → "Refresh Now"

### Stop the App
Click the menubar icon → "Quit"

### Restart the App
```bash
launchctl unload ~/Library/LaunchAgents/com.gpumonitor.menubar.plist
launchctl load ~/Library/LaunchAgents/com.gpumonitor.menubar.plist
```

### Uninstall
```bash
cd gpu-usage-monitor
./scripts/uninstall.sh
```

## What You'll See

**Menu Bar Icon:**
- Two vertical bars (left = GPU 0, right = GPU 1)
- Green = low load (0-50%)
- Orange = medium load (50-80%)
- Red = high load (80-100%)

**Dropdown Menu:**
```
GPU Monitor - ganesha
Updated: 18:00:45
────────────────────────────────
GPU 0: NVIDIA GeForce RTX 3090
Util: ▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░ 20%
Mem:  ▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░ 32%
  7864MB/24576MB | 45°C | 180.5W
...
```

## Next Steps

- Read the full [README.md](README.md) for detailed information
- Customize your configuration
- Set up monitoring for multiple servers
- Enable debug logging if needed

## Getting Help

- **Issues:** Report bugs on GitHub Issues
- **Documentation:** See README.md
- **Logs:** Check `/tmp/gpu-usage-menubar.err`

---

Enjoy monitoring your GPUs! 🚀
