#!/bin/bash
#
# Uninstallation script for GPU Usage Menubar
#

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLIST_FILE="$HOME/Library/LaunchAgents/com.gpumonitor.menubar.plist"

echo "=================================================="
echo "GPU Usage Menubar - Uninstallation"
echo "=================================================="
echo ""

# Stop the application
echo "Stopping application..."
pkill -f "gpu_usage_menubar.app" 2>/dev/null || true
echo "✓ Application stopped"

# Unload LaunchAgent
if [ -f "$PLIST_FILE" ]; then
    echo ""
    echo "Unloading LaunchAgent..."
    launchctl unload "$PLIST_FILE" 2>/dev/null || true
    rm -f "$PLIST_FILE"
    echo "✓ LaunchAgent removed"
fi

# Clean up temporary files
echo ""
echo "Cleaning up temporary files..."
rm -f /tmp/gpu-usage-menubar.out
rm -f /tmp/gpu-usage-menubar.err
rm -f /tmp/gpu-usage-menubar-debug.log
echo "✓ Temporary files cleaned"

# Ask about micromamba environment
echo ""
read -p "Remove micromamba environment? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf "$PROJECT_DIR/mamba-env"
    echo "✓ Micromamba environment removed"
fi

# Ask about configuration
echo ""
read -p "Remove configuration file (~/.gpu_monitor_config)? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f "$HOME/.gpu_monitor_config"
    echo "✓ Configuration removed"
fi

echo ""
echo "=================================================="
echo "Uninstallation Complete!"
echo "=================================================="
echo ""
