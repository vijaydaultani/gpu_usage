#!/bin/bash
# Run script for GPU Usage Menubar using micromamba

# Get the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MAMBA_ENV_DIR="$PROJECT_DIR/mamba-env"

# Load configuration if exists
if [ -f "$HOME/.gpu_monitor_config" ]; then
    export $(cat "$HOME/.gpu_monitor_config" | grep -v '^#' | xargs)
fi

# Set environment for proper execution
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Find micromamba executable
MICROMAMBA_BIN="$HOME/.local/bin/micromamba"

if [ ! -f "$MICROMAMBA_BIN" ]; then
    # Try alternate locations
    if [ -f "/usr/local/bin/micromamba" ]; then
        MICROMAMBA_BIN="/usr/local/bin/micromamba"
    elif command -v micromamba &> /dev/null; then
        MICROMAMBA_BIN="$(command -v micromamba)"
    else
        echo "Error: micromamba not found"
        exit 1
    fi
fi

# Create symlink to python with proper name if it doesn't exist
GPU_MONITOR_BIN="$MAMBA_ENV_DIR/bin/GPUMonitor"
if [ ! -f "$GPU_MONITOR_BIN" ]; then
    ln -sf "$MAMBA_ENV_DIR/bin/python" "$GPU_MONITOR_BIN"
fi

# Run using the renamed executable so Bartender shows correct name
exec "$MICROMAMBA_BIN" run -p "$MAMBA_ENV_DIR" "$GPU_MONITOR_BIN" -m gpu_usage_menubar.app
