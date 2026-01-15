#!/bin/bash
#
# Refresh icon cache and restart Dock
# This requires sudo password to clear system icon cache
#

echo "Refreshing icon cache..."
echo ""
echo "This will:"
echo "  1. Clear macOS icon cache (requires password)"
echo "  2. Restart Dock"
echo "  3. Refresh Launchpad"
echo ""

# Clear system icon cache (requires sudo)
sudo rm -rf /Library/Caches/com.apple.iconservices.store

# Restart Dock (updates menubar and Launchpad)
killall Dock

# Refresh Launchpad database
defaults write com.apple.dock ResetLaunchPad -bool true

# Wait for Dock to restart
sleep 2

echo ""
echo "✓ Icon cache refreshed!"
echo ""
echo "Your new GPU icon should now appear in:"
echo "  • Applications folder"
echo "  • Launchpad"
echo "  • Spotlight"
echo "  • Mission Control"
echo ""
