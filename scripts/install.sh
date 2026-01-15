#!/bin/bash
#
# Installation script for GPU Usage Menubar
# This script installs the menubar app and sets up auto-start via LaunchAgent
#

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MAMBA_ENV_DIR="$PROJECT_DIR/mamba-env"
PLIST_FILE="$HOME/Library/LaunchAgents/com.gpumonitor.menubar.plist"

echo "=================================================="
echo "GPU Usage Menubar - Installation"
echo "=================================================="
echo ""

# Check micromamba
echo "Checking micromamba installation..."
if ! command -v micromamba &> /dev/null; then
    echo "❌ Error: micromamba not found"
    echo "   Please install micromamba first: https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html"
    exit 1
fi
echo "✓ micromamba found"

# Check if SSH access to server works
echo ""
echo "Checking SSH access to GPU server..."
GPU_HOST="${GPU_SERVER_HOST:-ganesha}"
if ssh -o ConnectTimeout=5 -o BatchMode=yes "$GPU_HOST" "echo 'SSH test successful'" 2>/dev/null; then
    echo "✓ SSH access to $GPU_HOST confirmed"
else
    echo "⚠️  Warning: Cannot connect to $GPU_HOST via SSH"
    echo "   Make sure you have:"
    echo "   1. SSH key-based authentication set up"
    echo "   2. Host '$GPU_HOST' is reachable"
    echo "   3. nvidia-smi is installed on the remote server"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create micromamba environment
echo ""
echo "Setting up micromamba environment..."
if [ -d "$MAMBA_ENV_DIR" ]; then
    echo "  Environment already exists, updating..."
else
    echo "  Creating new environment..."
    micromamba create -p "$MAMBA_ENV_DIR" -f "$PROJECT_DIR/environment.yml" -y
fi

# Update/install dependencies
echo ""
echo "Installing dependencies..."
micromamba run -p "$MAMBA_ENV_DIR" pip install -e "$PROJECT_DIR"
echo "✓ Dependencies installed"

# Create run script
echo ""
echo "Creating run script..."
RUN_SCRIPT="$PROJECT_DIR/scripts/run_app.sh"
cat > "$RUN_SCRIPT" << 'EOF'
#!/bin/bash
# Run script for GPU Usage Menubar

# Get the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$PROJECT_DIR/venv"

# Load configuration if exists
if [ -f "$HOME/.gpu_monitor_config" ]; then
    export $(cat "$HOME/.gpu_monitor_config" | grep -v '^#' | xargs)
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Set environment for proper execution
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

# Run the application
# Use arch -x86_64 on Apple Silicon for compatibility
if [ "$(uname -m)" = "arm64" ]; then
    exec arch -x86_64 python3 -m gpu_usage_menubar.app
else
    exec python3 -m gpu_usage_menubar.app
fi
EOF

chmod +x "$RUN_SCRIPT"
echo "✓ Run script created"

# Create LaunchAgent plist
echo ""
echo "Creating LaunchAgent..."

cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.gpumonitor.menubar</string>
    <key>ProgramArguments</key>
    <array>
        <string>$RUN_SCRIPT</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>/tmp/gpu-usage-menubar.err</string>
    <key>StandardOutPath</key>
    <string>/tmp/gpu-usage-menubar.out</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
EOF

echo "✓ LaunchAgent plist created"

# Stop existing instance if running
echo ""
echo "Stopping any existing instances..."
pkill -f "gpu_usage_menubar.app" 2>/dev/null || true
launchctl unload "$PLIST_FILE" 2>/dev/null || true
sleep 2

# Load LaunchAgent
echo ""
echo "Loading LaunchAgent..."
launchctl load "$PLIST_FILE"
echo "✓ LaunchAgent loaded"

echo ""
echo "=================================================="
echo "Installation Complete!"
echo "=================================================="
echo ""
echo "The GPU monitor should now appear in your menu bar."
echo ""
echo "Configuration:"
echo "  - Edit ~/.gpu_monitor_config to customize settings"
echo "  - Default server: $GPU_HOST"
echo "  - Refresh interval: 30 seconds"
echo ""
echo "Logs:"
echo "  - stdout: /tmp/gpu-usage-menubar.out"
echo "  - stderr: /tmp/gpu-usage-menubar.err"
echo ""
echo "To uninstall, run: ./scripts/uninstall.sh"
echo ""
