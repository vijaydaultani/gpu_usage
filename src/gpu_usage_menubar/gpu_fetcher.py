"""
GPU data fetcher for remote servers.
Connects via SSH to fetch GPU utilization metrics using nvidia-smi.
"""

import subprocess
import re
from typing import Optional, List, NamedTuple
from dataclasses import dataclass


@dataclass
class GPUInfo:
    """Container for GPU information."""
    gpu_id: int
    name: str
    utilization: float  # Percentage (0-100)
    memory_used: int    # MB
    memory_total: int   # MB
    memory_percent: float  # Percentage (0-100)
    temperature: int    # Celsius
    power_draw: float   # Watts


class GPUData(NamedTuple):
    """Container for all GPU data from remote server."""
    gpus: List[GPUInfo]
    hostname: str
    timestamp: str


def fetch_gpu_data(hostname: str, ssh_user: Optional[str] = None, timeout: int = 10) -> Optional[GPUData]:
    """
    Fetch GPU utilization data from a remote server via SSH.

    Uses nvidia-smi to query GPU metrics. Requires:
    - SSH access to the remote server
    - nvidia-smi installed on the remote server
    - SSH key-based authentication (no password prompt)

    Args:
        hostname: Remote server hostname or IP
        ssh_user: SSH username (defaults to current user if None)
        timeout: Command timeout in seconds

    Returns:
        GPUData object with all GPU information, or None if failed
    """
    try:
        # Build SSH command
        ssh_cmd = ["ssh"]
        if ssh_user:
            ssh_cmd.extend([f"{ssh_user}@{hostname}"])
        else:
            ssh_cmd.append(hostname)

        # nvidia-smi command to get GPU info in CSV format
        # Query: index, name, utilization.gpu, memory.used, memory.total, temperature.gpu, power.draw
        nvidia_cmd = (
            "nvidia-smi "
            "--query-gpu=index,name,utilization.gpu,memory.used,memory.total,temperature.gpu,power.draw "
            "--format=csv,noheader,nounits"
        )

        ssh_cmd.append(nvidia_cmd)

        # Execute command with timeout
        result = subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True
        )

        # Parse output
        gpus = []
        for line in result.stdout.strip().split('\n'):
            if not line.strip():
                continue

            parts = [p.strip() for p in line.split(',')]
            if len(parts) < 7:
                continue

            try:
                gpu_id = int(parts[0])
                name = parts[1]
                utilization = float(parts[2])
                memory_used = int(parts[3])
                memory_total = int(parts[4])
                memory_percent = (memory_used / memory_total * 100) if memory_total > 0 else 0
                temperature = int(parts[5])
                power_draw = float(parts[6])

                gpus.append(GPUInfo(
                    gpu_id=gpu_id,
                    name=name,
                    utilization=utilization,
                    memory_used=memory_used,
                    memory_total=memory_total,
                    memory_percent=memory_percent,
                    temperature=temperature,
                    power_draw=power_draw
                ))
            except (ValueError, IndexError) as e:
                print(f"Warning: Failed to parse line: {line} - {e}")
                continue

        if not gpus:
            return None

        # Get timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        return GPUData(gpus=gpus, hostname=hostname, timestamp=timestamp)

    except subprocess.TimeoutExpired:
        print(f"Error: SSH command timed out after {timeout} seconds")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error: SSH command failed: {e.stderr}")
        return None
    except Exception as e:
        print(f"Error fetching GPU data: {e}")
        return None


def format_gpu_summary(gpu_data: GPUData) -> str:
    """
    Format GPU data into a human-readable summary.

    Args:
        gpu_data: GPUData object

    Returns:
        Formatted string with GPU information
    """
    if not gpu_data or not gpu_data.gpus:
        return "No GPU data available"

    lines = [f"Server: {gpu_data.hostname} (Updated: {gpu_data.timestamp})"]
    lines.append("")

    for gpu in gpu_data.gpus:
        lines.append(f"GPU {gpu.gpu_id}: {gpu.name}")
        lines.append(f"  Utilization: {gpu.utilization:.0f}%")
        lines.append(f"  Memory: {gpu.memory_used} MB / {gpu.memory_total} MB ({gpu.memory_percent:.0f}%)")
        lines.append(f"  Temperature: {gpu.temperature}°C")
        lines.append(f"  Power: {gpu.power_draw:.1f}W")
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    # Test the fetcher
    import sys

    hostname = sys.argv[1] if len(sys.argv) > 1 else "ganesha"
    ssh_user = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"Fetching GPU data from {hostname}...")
    data = fetch_gpu_data(hostname, ssh_user)

    if data:
        print(format_gpu_summary(data))
    else:
        print("Failed to fetch GPU data")
