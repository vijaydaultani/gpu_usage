# GPU Usage Monitor

A native macOS menu bar application that displays real-time GPU utilization from remote servers with visual progress indicators and dual GPU monitoring.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)

## Features

### Visual Monitoring
- 🎨 **Dual GPU bar chart icon** in menu bar showing real-time utilization
- 📊 **Color-coded progress bars** (green/orange/red) for utilization levels
- 🖥️ **Detailed metrics** for each GPU including memory, temperature, and power
- 🌈 **Dynamic coloring** that adapts to utilization levels

### GPU Metrics Tracked
- **GPU utilization** (percentage)
- **Memory usage** (used/total MB and percentage)
- **Temperature** (Celsius)
- **Power draw** (Watts)
- **GPU model name**

### Remote Monitoring
- 🌐 **SSH-based** monitoring of remote GPU servers
- 🔒 **Secure** key-based authentication
- ⚡ **Auto-refresh** with configurable interval (default: 30 seconds)
- 🚀 **Auto-starts** on login via LaunchAgent

### Auto Management
- ⚡ **Configurable refresh rate** (default 30 seconds)
- 🚀 **Auto-starts** on login via LaunchAgent
- 🔄 **Manual refresh** option available
- 💤 **Sleep detection** - pauses during system sleep to save battery

## Screenshots

### Menu Bar Icon
The icon shows two vertical bars representing GPU 0 (left) and GPU 1 (right):
- **Green**: Low utilization (0-50%)
- **Orange**: Medium utilization (50-80%)
- **Red**: High utilization (80-100%)

### Dropdown Menu
```
GPU Monitor - ganesha
Updated: 18:00:45
────────────────────────────────
GPU 0: NVIDIA GeForce RTX 3090
Util: ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░ 45%
Mem:  ▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░ 52%
  12288MB/24576MB | 65°C | 280.5W

GPU 1: NVIDIA GeForce RTX 3090
Util: ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░ 73%
Mem:  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░ 81%
  19968MB/24576MB | 72°C | 320.8W
────────────────────────────────
Refresh Now
Quit
```

## Requirements

- **macOS**: 10.15 (Catalina) or later
- **Python**: 3.9 or higher
- **SSH Access**: Key-based authentication to remote GPU server
- **Remote Server**: nvidia-smi installed and accessible
- **Dependencies**: PyObjC (Cocoa framework), Pillow (auto-installed)

## Installation

### Prerequisites

1. **SSH Key Setup**: Ensure you have SSH key-based authentication set up for your GPU server:
   ```bash
   # Generate SSH key if you don't have one
   ssh-keygen -t ed25519

   # Copy key to remote server
   ssh-copy-id ganesha

   # Test connection (should not ask for password)
   ssh ganesha "nvidia-smi"
   ```

2. **Verify nvidia-smi**: Ensure the remote server has nvidia-smi installed:
   ```bash
   ssh ganesha "nvidia-smi --version"
   ```

### Automated Installation (Recommended)

```bash
git clone https://github.com/YOUR_USERNAME/gpu-usage-monitor.git
cd gpu-usage-monitor
./scripts/install.sh
```

The installer will:
1. Verify Python 3.9+ installation
2. Check SSH access to GPU server
3. Create a virtual environment
4. Install all dependencies
5. Configure LaunchAgent for auto-start
6. Launch the application

The app icon should appear in your menu bar within a few seconds!

### Manual Installation

If you prefer manual setup:

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate environment
source venv/bin/activate

# 3. Install package with dependencies
pip install -e .

# 4. Run the application
python -m gpu_usage_menubar.app
```

## Configuration

### Basic Configuration

Create a configuration file at `~/.gpu_monitor_config`:

```bash
# GPU server hostname or IP
GPU_SERVER_HOST=ganesha

# SSH username (optional - defaults to current user)
# GPU_SERVER_USER=your_username

# Refresh interval in seconds (default: 30)
GPU_REFRESH_INTERVAL=30

# Enable debug logging (optional)
DEBUG_LOGGING=0
```

### Multiple Servers

To monitor different servers, you can create different configurations and launch multiple instances:

```bash
# Monitor server 1
GPU_SERVER_HOST=ganesha python -m gpu_usage_menubar.app &

# Monitor server 2
GPU_SERVER_HOST=server2 python -m gpu_usage_menubar.app &
```

## Usage

### Understanding the Icon

The dual bar icon represents your GPU utilization:
- **Left bar**: GPU 0 utilization
- **Right bar**: GPU 1 utilization
- **Color coding**:
  - Green: 0-50% (low load)
  - Orange: 50-80% (medium load)
  - Red: 80-100% (high load)

### Reading the Dropdown

Click the icon to view detailed metrics:

1. **Server info**: Hostname and last update time
2. **Per-GPU metrics**:
   - GPU model name
   - Utilization percentage (with colored bar)
   - Memory usage (with colored bar)
   - Temperature and power draw
3. **Controls**: Manual refresh and quit options

### Manual Refresh

While the app auto-refreshes every 30 seconds (configurable), you can force an immediate update:
- Click the menu bar icon
- Select "Refresh Now"

## Auto-Start Configuration

The application is configured to **automatically start when you log in** to your Mac. This is managed by a macOS LaunchAgent.

### How It Works

- **LaunchAgent Location**: `~/Library/LaunchAgents/com.gpumonitor.menubar.plist`
- **RunAtLoad**: App starts automatically at login
- **Sleep Detection**: Automatically pauses during system sleep to save battery
- **No Manual Action Required**: Just restart your Mac and the app will appear in the menu bar

### Verify Auto-Start

After restarting your Mac, verify the app is running:

```bash
# Check if app is running
ps aux | grep gpu_usage_menubar

# Check LaunchAgent status
launchctl list | grep com.gpumonitor
```

### Disable Auto-Start

If you want to prevent the app from starting automatically:

```bash
# Temporarily disable
launchctl unload ~/Library/LaunchAgents/com.gpumonitor.menubar.plist

# Re-enable
launchctl load ~/Library/LaunchAgents/com.gpumonitor.menubar.plist

# Permanently remove (use uninstall script)
./scripts/uninstall.sh
```

## Uninstallation

```bash
./scripts/uninstall.sh
```

This will:
- Stop the running application
- Unload the LaunchAgent
- Remove auto-start configuration
- Clean up temporary files and logs
- Optionally remove the virtual environment and configuration

## Development

### Project Structure

```
gpu_usage/
├── src/gpu_usage_menubar/     # Main source code
│   ├── __init__.py            # Package initialization
│   ├── gpu_fetcher.py         # SSH-based GPU data fetcher
│   ├── icon_generator.py      # Generates dual GPU bar icons
│   └── app.py                 # Main PyObjC menubar application
│
├── tests/                     # Test suite
│   ├── test_gpu_fetcher.py    # GPU fetcher tests
│   ├── test_icon_generator.py # Icon generation tests
│   └── test_app.py            # Application tests
│
├── scripts/
│   ├── install.sh             # Automated installation
│   └── uninstall.sh           # Automated uninstallation
│
├── config/
│   └── settings.env.example   # Example configuration file
│
├── setup.py                   # Package configuration
├── pyproject.toml             # Build system configuration
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

### Testing the GPU Fetcher

You can test the GPU data fetcher independently:

```bash
source venv/bin/activate
python -m gpu_usage_menubar.gpu_fetcher ganesha
```

### Testing Icon Generation

Generate test icons at various utilization levels:

```bash
source venv/bin/activate
python -m gpu_usage_menubar.icon_generator
```

This will create test icons in the `test_icons/` directory.

### Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=src/gpu_usage_menubar --cov-report=term-missing
```

## Troubleshooting

### Icon Doesn't Appear

**Check if application is running:**
```bash
ps aux | grep gpu_usage_menubar
```

**Check LaunchAgent status:**
```bash
launchctl list | grep com.gpumonitor
```

**View logs:**
```bash
cat /tmp/gpu-usage-menubar.err
cat /tmp/gpu-usage-menubar.out
```

**Manually restart:**
```bash
launchctl unload ~/Library/LaunchAgents/com.gpumonitor.menubar.plist
launchctl load ~/Library/LaunchAgents/com.gpumonitor.menubar.plist
```

### Shows Error Icon (Red X)

**Verify SSH connection:**
```bash
ssh ganesha "echo 'Connection successful'"
```

**Test nvidia-smi on remote server:**
```bash
ssh ganesha "nvidia-smi --query-gpu=index,name,utilization.gpu --format=csv"
```

**Check SSH key authentication:**
- Ensure SSH key is added to ssh-agent: `ssh-add -l`
- Add key if needed: `ssh-add ~/.ssh/id_ed25519`
- Test passwordless login: `ssh -o BatchMode=yes ganesha`

### Connection Timeout

If the app shows connection errors:

1. **Increase timeout** in config:
   ```bash
   echo "GPU_FETCH_TIMEOUT=20" >> ~/.gpu_monitor_config
   ```

2. **Check network latency**:
   ```bash
   ping -c 5 ganesha
   ```

3. **Verify firewall** isn't blocking SSH

### Application Crashes

**Check Python version (must be 3.9+):**
```bash
python3 --version
```

**Reinstall dependencies:**
```bash
source venv/bin/activate
pip install -e . --force-reinstall
```

**Run manually to see error messages:**
```bash
source venv/bin/activate
python -m gpu_usage_menubar.app
```

### Architecture Issues (Apple Silicon)

On Apple Silicon Macs (M1/M2/M3), you may encounter architecture mismatches. The app automatically uses Rosetta for compatibility.

If you see architecture errors:
```bash
# Verify run script uses arch -x86_64
cat scripts/run_app.sh | grep arch
```

### Debug Logging

Enable debug logging to troubleshoot issues:

```bash
echo "DEBUG_LOGGING=1" >> ~/.gpu_monitor_config
launchctl unload ~/Library/LaunchAgents/com.gpumonitor.menubar.plist
launchctl load ~/Library/LaunchAgents/com.gpumonitor.menubar.plist

# View debug log
tail -f /tmp/gpu-usage-menubar-debug.log
```

## Technical Details

### How It Works

1. **Data Collection**: Connects via SSH to remote server
2. **nvidia-smi Query**: Executes nvidia-smi with CSV output format
3. **Parsing**: Extracts metrics (utilization, memory, temp, power)
4. **Icon Generation**: Creates dual-bar PNG icons with Pillow
5. **Display**: Uses PyObjC (native macOS Cocoa framework) for menu bar rendering
6. **Colored UI**: Uses NSAttributedString with NSColor for dynamic colored progress bars

### SSH Command Executed

```bash
ssh [user@]hostname "nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total,temperature.gpu,power.draw --format=csv,noheader,nounits"
```

### Icon Specifications

- **Format**: PNG with transparency
- **Size**: 36x36 pixels (18pt @ 2x retina)
- **Design**: Two vertical bars side by side
- **Colors**:
  - Background: Dark blue (#1e3a5f)
  - Low utilization: Green (#00ff00)
  - Medium utilization: Orange (#ffaa00)
  - High utilization: Red (#ff3333)
- **Template mode**: Disabled to preserve colors

### Progress Bar Display

- **Filled portion**: `▓` (U+2593 - Dark shade) in dynamic color
- **Empty portion**: `░` (U+2591 - Light shade) in light gray
- **Colors**: Green (0-50%), Orange (50-80%), Red (80-100%)
- **Width**: 25 characters
- **Implementation**: NSAttributedString with NSColor

### Refresh Mechanism

- **Auto-refresh**: NSTimer with configurable interval (default 30 seconds)
- **Thread-safe**: Uses threading.Lock() for data fetching
- **Manual refresh**: Immediate update via menu button
- **Sleep handling**: Timer stops during system sleep, restarts on wake

### Bundle Identifier

- **ID**: `com.gpumonitor.menubar`
- **Display Name**: GPU Usage Monitor
- **Process Type**: Interactive (shows in menu bar, not dock)
- **LSUIElement**: true (hides from Dock and Cmd+Tab app switcher)

## Security & Privacy

### Permissions Required

- **Network Access**: For SSH connections to remote server
- **Accessibility**: Not required
- **Screen Recording**: Not required
- **Full Disk Access**: Not required

### Data Handling

- **No data storage**: GPU data is only displayed, never stored
- **No external network**: Only SSH to specified server
- **SSH key security**: Uses system SSH agent for secure authentication

### Privacy Settings

The app will appear in:
- System Preferences → Security & Privacy → Privacy
- Under "Automation" (for running shell scripts)

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Add tests** for new functionality
4. **Ensure tests pass** (`pytest tests/ -v`)
5. **Commit** your changes (`git commit -m 'Add amazing feature'`)
6. **Push** to the branch (`git push origin feature/amazing-feature`)
7. **Open** a Pull Request

### Coding Standards

- Follow PEP 8 style guide
- Add docstrings for all functions
- Use type hints where appropriate
- Maintain test coverage

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

### Inspiration
- [Stats](https://github.com/exelban/stats) - macOS system monitor
- [Claude Usage Monitor](https://github.com/YOUR_USERNAME/claude-usage-monitor) - Template for menubar apps

### Libraries
- [PyObjC](https://pyobjc.readthedocs.io/) - Python bridge to macOS Cocoa frameworks
- [Pillow](https://python-pillow.org/) - Python Imaging Library for icon generation

### Development
- Tested on macOS Sonoma 14.x and Sequoia 15.x
- Supports both Intel and Apple Silicon Macs

## Changelog

### Version 1.0.0 (2026-01-15)

- Initial release
- Dual GPU monitoring with vertical bar icons
- Color-coded utilization indicators (green/orange/red)
- SSH-based remote GPU monitoring
- Detailed metrics: utilization, memory, temperature, power
- Auto-refresh with configurable interval
- LaunchAgent for auto-start on login
- Sleep detection for battery optimization
- Comprehensive error handling

## Roadmap

Future enhancements planned:

- [ ] Historical graphs of GPU utilization
- [ ] Alert notifications for high utilization/temperature
- [ ] Support for more than 2 GPUs
- [ ] GPU process listing (top GPU consumers)
- [ ] Multiple server monitoring in one app
- [ ] Export metrics to CSV/JSON
- [ ] Integration with monitoring systems (Prometheus, Grafana)

## Support

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/gpu-usage-monitor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/gpu-usage-monitor/discussions)

### Common Questions

**Q: Can I monitor more than 2 GPUs?**
A: Currently the icon supports 2 GPUs optimally. The dropdown menu will show all GPUs detected by nvidia-smi.

**Q: Does it work with AMD GPUs?**
A: No, currently only NVIDIA GPUs with nvidia-smi are supported.

**Q: Can I monitor local GPUs instead of remote?**
A: Yes! Just set `GPU_SERVER_HOST=localhost` in the config (requires nvidia-smi locally).

**Q: Why use SSH instead of a REST API?**
A: SSH is simpler, more secure, and doesn't require server-side setup. Most GPU servers already have SSH enabled.

**Q: Does it work with Docker containers?**
A: Yes, as long as nvidia-smi is accessible via SSH on the host.

**Q: Can I change the refresh rate?**
A: Yes, set `GPU_REFRESH_INTERVAL=X` (in seconds) in `~/.gpu_monitor_config`.

---

**Made with ❤️ for GPU monitoring**
