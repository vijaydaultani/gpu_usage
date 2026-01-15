#!/bin/bash
#
# Test script to verify GPU server connection
# Run this before installing to ensure everything is set up correctly
#

set -e

echo "=================================================="
echo "GPU Monitor - Connection Test"
echo "=================================================="
echo ""

# Get server hostname from env or use default
GPU_HOST="${GPU_SERVER_HOST:-ganesha}"
GPU_USER="${GPU_SERVER_USER:-}"

if [ -n "$GPU_USER" ]; then
    SSH_TARGET="${GPU_USER}@${GPU_HOST}"
else
    SSH_TARGET="${GPU_HOST}"
fi

echo "Testing connection to: $SSH_TARGET"
echo ""

# Test 1: Basic SSH connection
echo "Test 1: SSH Connection"
echo "----------------------"
if ssh -o ConnectTimeout=5 -o BatchMode=yes "$SSH_TARGET" "echo 'SSH connection successful'" 2>/dev/null; then
    echo "✅ SSH connection works"
else
    echo "❌ SSH connection failed"
    echo ""
    echo "Troubleshooting steps:"
    echo "1. Check if server is reachable: ping $GPU_HOST"
    echo "2. Set up SSH key: ssh-copy-id $SSH_TARGET"
    echo "3. Test manual connection: ssh $SSH_TARGET"
    exit 1
fi

echo ""

# Test 2: nvidia-smi availability
echo "Test 2: nvidia-smi Command"
echo "-------------------------"
if ssh -o ConnectTimeout=5 "$SSH_TARGET" "which nvidia-smi" > /dev/null 2>&1; then
    echo "✅ nvidia-smi is available"
else
    echo "❌ nvidia-smi not found on remote server"
    echo ""
    echo "nvidia-smi must be installed on $GPU_HOST"
    exit 1
fi

echo ""

# Test 3: GPU detection
echo "Test 3: GPU Detection"
echo "--------------------"
GPU_OUTPUT=$(ssh -o ConnectTimeout=10 "$SSH_TARGET" "nvidia-smi --query-gpu=index,name --format=csv,noheader" 2>&1)

if [ $? -eq 0 ]; then
    GPU_COUNT=$(echo "$GPU_OUTPUT" | wc -l | tr -d ' ')
    echo "✅ Found $GPU_COUNT GPU(s):"
    echo ""
    echo "$GPU_OUTPUT" | while IFS=',' read -r index name; do
        echo "  GPU $index: $name"
    done
else
    echo "❌ Failed to query GPUs"
    echo ""
    echo "Error: $GPU_OUTPUT"
    exit 1
fi

echo ""

# Test 4: Full GPU query
echo "Test 4: Full GPU Metrics Query"
echo "------------------------------"
FULL_OUTPUT=$(ssh -o ConnectTimeout=10 "$SSH_TARGET" \
    "nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total,temperature.gpu,power.draw --format=csv,noheader,nounits" 2>&1)

if [ $? -eq 0 ]; then
    echo "✅ Successfully retrieved GPU metrics:"
    echo ""
    echo "GPU | Name | Util% | Memory | Temp | Power"
    echo "----+------+-------+--------+------+------"
    echo "$FULL_OUTPUT" | while IFS=',' read -r idx name util mem_used mem_total temp power; do
        idx=$(echo $idx | xargs)
        name=$(echo $name | xargs)
        util=$(echo $util | xargs)
        mem_used=$(echo $mem_used | xargs)
        mem_total=$(echo $mem_total | xargs)
        temp=$(echo $temp | xargs)
        power=$(echo $power | xargs)
        printf "%3s | %-20s | %5s%% | %5s/%5sMB | %3s°C | %6sW\n" \
            "$idx" "$name" "$util" "$mem_used" "$mem_total" "$temp" "$power"
    done
else
    echo "❌ Failed to retrieve GPU metrics"
    echo ""
    echo "Error: $FULL_OUTPUT"
    exit 1
fi

echo ""
echo "=================================================="
echo "✅ All tests passed!"
echo "=================================================="
echo ""
echo "Your system is ready for GPU monitoring."
echo "Run ./scripts/install.sh to install the menubar app."
echo ""
