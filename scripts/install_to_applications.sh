#!/bin/bash
#
# Install GPU Monitor.app to Applications folder
#

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_APP="$PROJECT_DIR/build/GPU Monitor.app"
DEST_APP="/Applications/GPU Monitor.app"

echo "Installing GPU Monitor to Applications folder..."
echo ""

# Check if source app exists
if [ ! -d "$SOURCE_APP" ]; then
    echo "❌ Error: GPU Monitor.app not found"
    echo "   Run: ./scripts/create_app_bundle.sh first"
    exit 1
fi

# Remove existing app if present
if [ -d "$DEST_APP" ]; then
    echo "Removing existing GPU Monitor.app from Applications..."
    rm -rf "$DEST_APP"
fi

# Copy to Applications
echo "Copying to /Applications..."
cp -R "$SOURCE_APP" "/Applications/"

echo ""
echo "✓ GPU Monitor installed successfully!"
echo ""
echo "You can now:"
echo "  • Launch from Applications folder"
echo "  • Launch from Spotlight (Cmd+Space, type 'GPU Monitor')"
echo "  • Launch from Mission Control"
echo "  • Add to Dock for quick access"
echo ""
echo "The app will appear in your menubar when launched."
echo ""
