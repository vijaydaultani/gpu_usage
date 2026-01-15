#!/bin/bash
#
# Update GPU Monitor app icon
# Usage: ./update_app_icon.sh <path_to_icon.png>
#

set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 <path_to_icon.png>"
    echo ""
    echo "Example:"
    echo "  $0 ~/Downloads/gpu_icon.png"
    exit 1
fi

ICON_PATH="$1"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ ! -f "$ICON_PATH" ]; then
    echo "❌ Error: Icon file not found: $ICON_PATH"
    exit 1
fi

echo "Updating GPU Monitor icon..."
echo ""

# Copy to icons directory
echo "Copying icon to project..."
cp "$ICON_PATH" "$PROJECT_DIR/icons/AppIcon.png"

# Create iconset for all sizes
ICONSET_DIR="$PROJECT_DIR/icons/AppIcon.iconset"
mkdir -p "$ICONSET_DIR"

echo "Generating icon sizes..."

# Use sips to resize the icon to different sizes
sips -z 16 16     "$ICON_PATH" --out "$ICONSET_DIR/icon_16x16.png" >/dev/null 2>&1
sips -z 32 32     "$ICON_PATH" --out "$ICONSET_DIR/icon_16x16@2x.png" >/dev/null 2>&1
sips -z 32 32     "$ICON_PATH" --out "$ICONSET_DIR/icon_32x32.png" >/dev/null 2>&1
sips -z 64 64     "$ICON_PATH" --out "$ICONSET_DIR/icon_32x32@2x.png" >/dev/null 2>&1
sips -z 128 128   "$ICON_PATH" --out "$ICONSET_DIR/icon_128x128.png" >/dev/null 2>&1
sips -z 256 256   "$ICON_PATH" --out "$ICONSET_DIR/icon_128x128@2x.png" >/dev/null 2>&1
sips -z 256 256   "$ICON_PATH" --out "$ICONSET_DIR/icon_256x256.png" >/dev/null 2>&1
sips -z 512 512   "$ICON_PATH" --out "$ICONSET_DIR/icon_256x256@2x.png" >/dev/null 2>&1
sips -z 512 512   "$ICON_PATH" --out "$ICONSET_DIR/icon_512x512.png" >/dev/null 2>&1
sips -z 1024 1024 "$ICON_PATH" --out "$ICONSET_DIR/icon_512x512@2x.png" >/dev/null 2>&1

# Convert to ICNS
echo "Creating ICNS file..."
iconutil -c icns "$ICONSET_DIR" -o "$PROJECT_DIR/icons/AppIcon.icns"

# Clean up iconset
rm -rf "$ICONSET_DIR"

# Update app bundle in Applications folder
echo "Updating app bundle..."

if [ -d "/Applications/GPU Monitor.app" ]; then
    cp "$PROJECT_DIR/icons/AppIcon.icns" "/Applications/GPU Monitor.app/Contents/Resources/"
    touch "/Applications/GPU Monitor.app"
    echo "  ✓ Updated /Applications/GPU Monitor.app"
else
    echo "  ⚠️  App not found in /Applications"
    echo "     Run: ./scripts/install_to_applications.sh"
fi

echo ""
echo "✓ Icon updated successfully!"
echo ""
echo "Note: You may need to:"
echo "  1. Restart the app to see the new icon"
echo "  2. Rebuild icon cache: sudo rm -rf /Library/Caches/com.apple.iconservices.store"
echo "  3. Restart Dock: killall Dock"
echo ""
