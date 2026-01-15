#!/bin/bash
#
# Create a macOS application bundle for GPU Monitor
# This creates a .app that can be launched from Finder, Spotlight, or Mission Control
#

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_NAME="GPU Monitor"
BUILD_DIR="$PROJECT_DIR/build"
APP_BUNDLE="$BUILD_DIR/GPU Monitor.app"
CONTENTS_DIR="$APP_BUNDLE/Contents"
MACOS_DIR="$CONTENTS_DIR/MacOS"
RESOURCES_DIR="$CONTENTS_DIR/Resources"

echo "=================================================="
echo "Creating macOS Application Bundle"
echo "=================================================="
echo ""

# Remove existing app if present
if [ -d "$APP_BUNDLE" ]; then
    echo "Removing existing app bundle..."
    rm -rf "$APP_BUNDLE"
fi

# Create directory structure
echo "Creating directory structure..."
mkdir -p "$MACOS_DIR"
mkdir -p "$RESOURCES_DIR"

# Create Info.plist
echo "Creating Info.plist..."
cat > "$CONTENTS_DIR/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleDisplayName</key>
    <string>GPU Monitor</string>
    <key>CFBundleExecutable</key>
    <string>gpu_monitor_launcher</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>CFBundleIdentifier</key>
    <string>com.gpumonitor.menubar</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>GPU Monitor</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>LSUIElement</key>
    <true/>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF

# Create launcher script
echo "Creating launcher script..."
cat > "$MACOS_DIR/gpu_monitor_launcher" << EOF
#!/bin/bash
#
# GPU Monitor Launcher
# This script is executed when the .app is launched
#

# Get the app bundle path
BUNDLE_PATH="\$(cd "\$(dirname "\${BASH_SOURCE[0]}")/../.." && pwd)"
# Project directory is fixed location
PROJECT_DIR="$PROJECT_DIR"
MAMBA_ENV_DIR="\$PROJECT_DIR/mamba-env"

# Load configuration if exists
if [ -f "$HOME/.gpu_monitor_config" ]; then
    export $(cat "$HOME/.gpu_monitor_config" | grep -v '^#' | xargs)
fi

# Set environment
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Find micromamba
MICROMAMBA_BIN="$HOME/.local/bin/micromamba"
if [ ! -f "$MICROMAMBA_BIN" ]; then
    if [ -f "/usr/local/bin/micromamba" ]; then
        MICROMAMBA_BIN="/usr/local/bin/micromamba"
    fi
fi

# Check if already running
if pgrep -f "gpu_usage_menubar.app" > /dev/null; then
    echo "GPU Monitor is already running"
    exit 0
fi

# Run the application
exec "$MICROMAMBA_BIN" run -p "$MAMBA_ENV_DIR" python -m gpu_usage_menubar.app
EOF

chmod +x "$MACOS_DIR/gpu_monitor_launcher"

# Copy icon if it exists, otherwise create it
echo "Setting up application icon..."
if [ -f "$PROJECT_DIR/icons/AppIcon.png" ]; then
    # Convert PNG to ICNS format (macOS app icon format)
    # First, create an iconset directory
    ICONSET_DIR="$RESOURCES_DIR/AppIcon.iconset"
    mkdir -p "$ICONSET_DIR"

    # Copy icons at different sizes (if we have the create_icon script)
    if [ -f "$PROJECT_DIR/icons/icon_16x16.png" ]; then
        cp "$PROJECT_DIR/icons/icon_16x16.png" "$ICONSET_DIR/icon_16x16.png"
        cp "$PROJECT_DIR/icons/icon_32x32.png" "$ICONSET_DIR/icon_16x16@2x.png"
        cp "$PROJECT_DIR/icons/icon_32x32.png" "$ICONSET_DIR/icon_32x32.png"
        cp "$PROJECT_DIR/icons/icon_64x64.png" "$ICONSET_DIR/icon_32x32@2x.png"
        cp "$PROJECT_DIR/icons/icon_128x128.png" "$ICONSET_DIR/icon_128x128.png"
        cp "$PROJECT_DIR/icons/icon_256x256.png" "$ICONSET_DIR/icon_128x128@2x.png"
        cp "$PROJECT_DIR/icons/icon_256x256.png" "$ICONSET_DIR/icon_256x256.png"
        cp "$PROJECT_DIR/icons/icon_512x512.png" "$ICONSET_DIR/icon_256x256@2x.png"
        cp "$PROJECT_DIR/icons/icon_512x512.png" "$ICONSET_DIR/icon_512x512.png"
        cp "$PROJECT_DIR/icons/icon_1024x1024.png" "$ICONSET_DIR/icon_512x512@2x.png"

        # Convert to ICNS
        iconutil -c icns "$ICONSET_DIR" -o "$RESOURCES_DIR/AppIcon.icns"
        rm -rf "$ICONSET_DIR"
    else
        # Just copy the PNG (will work but not ideal)
        cp "$PROJECT_DIR/icons/AppIcon.png" "$RESOURCES_DIR/AppIcon.png"
    fi
else
    echo "⚠️  Warning: Icon not found at $PROJECT_DIR/icons/AppIcon.png"
    echo "   Run: ./scripts/create_app_icon.py to generate icons"
fi

# Create PkgInfo file
echo "APPL????" > "$CONTENTS_DIR/PkgInfo"

echo ""
echo "=================================================="
echo "✓ Application bundle created successfully!"
echo "=================================================="
echo ""
echo "Build location: $APP_BUNDLE"
echo ""
echo "Next step: Install to Applications folder"
echo "  Run: ./scripts/install_to_applications.sh"
echo ""
