#!/bin/bash
#
# Configure GPU Monitor visibility in Cmd+Tab and Dock
#
# LSUIElement=true  - Hidden from Cmd+Tab and Dock (menubar only)
# LSUIElement=false - Visible in Cmd+Tab and Dock (normal app)
#

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

show_usage() {
    echo "GPU Monitor - Configure App Visibility"
    echo ""
    echo "Usage: $0 [show]"
    echo ""
    echo "Options:"
    echo "  show - Show in Cmd+Tab, Dock, and Launchpad (normal app)"
    echo ""
    echo "Note: To show icon in Launchpad, the app must also appear in Cmd+Tab."
    echo "This is a macOS limitation with LSUIElement setting."
    echo ""
    echo "Current setting:"
    if [ -f "/Applications/GPU Monitor.app/Contents/Info.plist" ]; then
        if grep -q "<key>LSUIElement</key>" "/Applications/GPU Monitor.app/Contents/Info.plist"; then
            if grep -A1 "LSUIElement" "/Applications/GPU Monitor.app/Contents/Info.plist" | grep -q "<true/>"; then
                echo "  Status: HIDDEN from Cmd+Tab/Dock/Launchpad (menubar only)"
            else
                echo "  Status: VISIBLE in Cmd+Tab/Dock/Launchpad"
            fi
        fi
    else
        echo "  App not found in /Applications. Run: ./scripts/install_to_applications.sh"
    fi
    echo ""
}

if [ $# -eq 0 ]; then
    show_usage
    exit 0
fi

MODE="$1"

if [ "$MODE" != "show" ]; then
    echo "❌ Error: Invalid option '$MODE'"
    echo ""
    show_usage
    exit 1
fi

# Set LSUIElement to false to show in Launchpad
LSUI_VALUE="false"
STATUS_MSG="VISIBLE in Cmd+Tab, Dock, and Launchpad"

echo "Configuring GPU Monitor visibility..."
echo ""

# Function to update plist
update_plist() {
    local plist_path="$1"

    if [ ! -f "$plist_path" ]; then
        echo "  ⚠️  Skipping: $plist_path not found"
        return
    fi

    # Use PlistBuddy to update the value
    /usr/libexec/PlistBuddy -c "Set :LSUIElement $LSUI_VALUE" "$plist_path" 2>/dev/null || \
    /usr/libexec/PlistBuddy -c "Add :LSUIElement bool $LSUI_VALUE" "$plist_path"

    # Touch the app to update modification time
    touch "$(dirname "$(dirname "$plist_path")")"

    echo "  ✓ Updated: $plist_path"
}

# Update Applications folder (the only location that matters)
update_plist "/Applications/GPU Monitor.app/Contents/Info.plist"

echo ""
echo "✓ Configuration updated!"
echo ""
echo "New setting: $STATUS_MSG"
echo ""
echo "To apply changes:"
echo "  1. Quit GPU Monitor (click icon → Quit)"
echo "  2. Restart the app"
echo "  3. Or run: ./scripts/restart.sh"
echo ""
