#!/bin/bash
#
# Stop GPU Usage Monitor
#

PLIST_FILE="$HOME/Library/LaunchAgents/com.gpumonitor.menubar.plist"

echo "Stopping GPU Usage Monitor..."

# Check if running
if ! launchctl list | grep -q "com.gpumonitor.menubar"; then
    echo "✓ GPU Monitor is not running"
    exit 0
fi

# Unload the LaunchAgent
launchctl unload "$PLIST_FILE"

# Also kill any running processes
pkill -f "gpu_usage_menubar.app" 2>/dev/null

# Wait a moment
sleep 1

# Verify it stopped
if ps aux | grep -v grep | grep -q "gpu_usage_menubar.app"; then
    echo "⚠️  Warning: Process may still be running"
    echo "  Force kill with: pkill -9 -f gpu_usage_menubar.app"
else
    echo "✓ GPU Monitor stopped successfully"
fi
