"""
GPU data fetcher for remote servers.
Connects via SSH to fetch GPU utilization metrics using nvidia-smi.
Uses SSH ControlMaster for connection multiplexing (single persistent connection).
"""

import subprocess
import os
import tempfile
import atexit
from typing import Optional, List, NamedTuple
from dataclasses import dataclass


class SSHConnectionManager:
    """
    Manages a persistent SSH connection using ControlMaster.

    This ensures only ONE SSH connection is maintained to the remote server,
    and all subsequent SSH commands reuse this connection through the control socket.
    """

    _instance = None
    _control_dir = None
    _active_connections = {}  # hostname -> control_path

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._control_dir = tempfile.mkdtemp(prefix='gpu_monitor_ssh_')
            atexit.register(cls._instance.cleanup_all)
        return cls._instance

    def _get_control_path(self, hostname: str, ssh_user: Optional[str] = None) -> str:
        """Get the control socket path for a given host."""
        key = f"{ssh_user}@{hostname}" if ssh_user else hostname
        return os.path.join(self._control_dir, f"ctrl-{key.replace('@', '_at_')}.sock")

    def _get_host_string(self, hostname: str, ssh_user: Optional[str] = None) -> str:
        """Get the SSH host string (user@host or just host)."""
        return f"{ssh_user}@{hostname}" if ssh_user else hostname

    def ensure_connection(self, hostname: str, ssh_user: Optional[str] = None, timeout: int = 10) -> bool:
        """
        Ensure a master SSH connection exists for the given host.

        If no master connection exists, creates one. If one exists, verifies it's alive.

        Returns:
            True if connection is ready, False if failed
        """
        control_path = self._get_control_path(hostname, ssh_user)
        host_string = self._get_host_string(hostname, ssh_user)

        # Check if master connection already exists and is alive
        if os.path.exists(control_path):
            check_cmd = [
                "ssh", "-O", "check",
                "-o", f"ControlPath={control_path}",
                host_string
            ]
            try:
                subprocess.run(check_cmd, capture_output=True, timeout=5)
                return True  # Connection is alive
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                # Connection dead, remove stale socket
                try:
                    os.remove(control_path)
                except OSError:
                    pass

        # Start a new master connection
        master_cmd = [
            "ssh",
            "-o", f"ControlPath={control_path}",
            "-o", "ControlMaster=yes",
            "-o", "ControlPersist=600",  # Keep connection alive for 10 minutes
            "-o", "ServerAliveInterval=30",  # Send keepalive every 30 seconds
            "-o", "ServerAliveCountMax=3",
            "-o", "BatchMode=yes",  # Never prompt for password
            "-o", "ConnectTimeout=10",
            "-N",  # Don't execute remote command, just connect
            "-f",  # Go to background after connection
            host_string
        ]

        try:
            result = subprocess.run(master_cmd, capture_output=True, text=True, timeout=timeout)
            if result.returncode == 0:
                self._active_connections[host_string] = control_path
                print(f"SSH master connection established to {host_string}")
                return True
            else:
                print(f"Failed to establish SSH master connection: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print(f"SSH master connection timed out for {host_string}")
            return False
        except Exception as e:
            print(f"Error establishing SSH master connection: {e}")
            return False

    def get_ssh_command(self, hostname: str, ssh_user: Optional[str] = None) -> List[str]:
        """
        Get SSH command arguments that use the multiplexed connection.

        Returns:
            List of SSH command arguments including ControlPath options
        """
        control_path = self._get_control_path(hostname, ssh_user)
        host_string = self._get_host_string(hostname, ssh_user)

        return [
            "ssh",
            "-o", f"ControlPath={control_path}",
            "-o", "ControlMaster=auto",  # Use existing master or create new one
            "-o", "BatchMode=yes",
            host_string
        ]

    def close_connection(self, hostname: str, ssh_user: Optional[str] = None):
        """Close the master connection for a specific host."""
        control_path = self._get_control_path(hostname, ssh_user)
        host_string = self._get_host_string(hostname, ssh_user)

        if os.path.exists(control_path):
            close_cmd = [
                "ssh", "-O", "exit",
                "-o", f"ControlPath={control_path}",
                host_string
            ]
            try:
                subprocess.run(close_cmd, capture_output=True, timeout=5)
                print(f"SSH connection closed for {host_string}")
            except Exception as e:
                print(f"Error closing SSH connection: {e}")

            # Clean up socket file
            try:
                os.remove(control_path)
            except OSError:
                pass

        if host_string in self._active_connections:
            del self._active_connections[host_string]

    def cleanup_all(self):
        """Close all active SSH connections and clean up."""
        print("Cleaning up SSH connections...")
        for host_string, control_path in list(self._active_connections.items()):
            if os.path.exists(control_path):
                close_cmd = [
                    "ssh", "-O", "exit",
                    "-o", f"ControlPath={control_path}",
                    host_string
                ]
                try:
                    subprocess.run(close_cmd, capture_output=True, timeout=5)
                except Exception:
                    pass

        # Clean up control directory
        if self._control_dir and os.path.exists(self._control_dir):
            try:
                import shutil
                shutil.rmtree(self._control_dir, ignore_errors=True)
            except Exception:
                pass

        self._active_connections.clear()


# Global connection manager instance
_ssh_manager = None

def get_ssh_manager() -> SSHConnectionManager:
    """Get the singleton SSH connection manager."""
    global _ssh_manager
    if _ssh_manager is None:
        _ssh_manager = SSHConnectionManager()
    return _ssh_manager


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

    This function uses SSH ControlMaster to maintain a single persistent
    connection, avoiding the overhead of establishing a new SSH session
    for each query.

    Args:
        hostname: Remote server hostname or IP
        ssh_user: SSH username (defaults to current user if None)
        timeout: Command timeout in seconds

    Returns:
        GPUData object with all GPU information, or None if failed
    """
    try:
        # Get the SSH connection manager and ensure connection is ready
        ssh_manager = get_ssh_manager()
        ssh_manager.ensure_connection(hostname, ssh_user, timeout)

        # Build SSH command using multiplexed connection
        ssh_cmd = ssh_manager.get_ssh_command(hostname, ssh_user)

        # nvidia-smi command to get GPU info in CSV format
        # Query: index, name, utilization.gpu, memory.used, memory.total, temperature.gpu, power.draw
        nvidia_cmd = (
            "nvidia-smi "
            "--query-gpu=index,name,utilization.gpu,memory.used,memory.total,temperature.gpu,power.draw "
            "--format=csv,noheader,nounits"
        )

        ssh_cmd.append(nvidia_cmd)

        # Execute command with timeout (uses existing multiplexed connection)
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
