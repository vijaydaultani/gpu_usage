#!/bin/bash
#
# Restart GPU Usage Monitor
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Restarting GPU Usage Monitor..."
echo ""

# Stop
"$SCRIPT_DIR/stop.sh"

echo ""

# Wait a moment
sleep 2

# Start
"$SCRIPT_DIR/start.sh"
