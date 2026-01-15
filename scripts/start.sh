#!/bin/bash
#
# Start GPU Usage Monitor
#

PLIST_FILE="$HOME/Library/LaunchAgents/com.gpumonitor.menubar.plist"

echo "Starting GPU Usage Monitor..."

# Check if already running
if launchctl list | grep -q "com.gpumonitor.menubar"; then
    echo "✓ GPU Monitor is already running"
    exit 0
fi

# Load the LaunchAgent
launchctl load "$PLIST_FILE"

# Wait a moment for it to start
sleep 2

# Verify it started
if ps aux | grep -v grep | grep -q "gpu_usage_menubar.app"; then
    echo "✓ GPU Monitor started successfully"
    echo "  Look for the icon in your menu bar"
else
    echo "✗ Failed to start GPU Monitor"
    echo "  Check logs: cat /tmp/gpu-usage-menubar.err"
    exit 1
fi
