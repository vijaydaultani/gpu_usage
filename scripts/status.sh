#!/bin/bash
#
# Check GPU Usage Monitor status
#

PLIST_FILE="$HOME/Library/LaunchAgents/com.gpumonitor.menubar.plist"

echo "GPU Usage Monitor Status"
echo "========================"
echo ""

# Check LaunchAgent
if launchctl list | grep -q "com.gpumonitor.menubar"; then
    echo "LaunchAgent: ✓ Loaded"
else
    echo "LaunchAgent: ✗ Not loaded"
fi

# Check process
if ps aux | grep -v grep | grep -q "gpu_usage_menubar.app"; then
    echo "Process:     ✓ Running"
    echo ""
    echo "Process details:"
    ps aux | grep -v grep | grep "gpu_usage_menubar.app" | head -1
else
    echo "Process:     ✗ Not running"
fi

echo ""
echo "Configuration:"
echo "  Server: ${GPU_SERVER_HOST:-ganesha}"
echo "  Refresh: ${GPU_REFRESH_INTERVAL:-300} seconds"

# Check for errors
if [ -f /tmp/gpu-usage-menubar.err ] && [ -s /tmp/gpu-usage-menubar.err ]; then
    echo ""
    echo "Recent errors (last 5 lines):"
    tail -5 /tmp/gpu-usage-menubar.err
fi
