"""
Icon generator for dual GPU monitoring.
Creates menubar icons showing utilization for two GPUs side by side.
"""

from PIL import Image, ImageDraw, ImageFont
import io
from typing import Optional, Tuple


# Color scheme
COLORS = {
    "bg_dark": "#2d3748",      # Darker gray background (more visible)
    "bg_empty": "#4a5568",     # Gray for empty portion (more visible)
    "gpu_low": "#48bb78",      # Green for low utilization (0-50%)
    "gpu_medium": "#ed8936",   # Orange for medium utilization (50-80%)
    "gpu_high": "#f56565",     # Red for high utilization (80-100%)
    "text": "#ffffff",         # White text
    "border": "#718096",       # Lighter border for visibility
}


def get_utilization_color(percent: float) -> str:
    """
    Get color based on GPU utilization percentage.

    Args:
        percent: GPU utilization (0-100)

    Returns:
        Hex color string
    """
    if percent < 50:
        return COLORS["gpu_low"]
    elif percent < 80:
        return COLORS["gpu_medium"]
    else:
        return COLORS["gpu_high"]


def create_dual_gpu_icon(gpu1_percent: float, gpu2_percent: float, size: int = 36) -> bytes:
    """
    Create a menu bar icon showing two GPU utilization levels side by side.

    Creates a compact icon with two vertical bars representing GPU0 and GPU1.
    Each bar is color-coded: green (low), orange (medium), red (high).

    Args:
        gpu1_percent: GPU 0 utilization (0-100)
        gpu2_percent: GPU 1 utilization (0-100)
        size: Icon size in pixels (default 36 for retina 18x18pt)

    Returns:
        PNG image bytes
    """
    # Clamp percentages
    gpu1_percent = max(0, min(100, gpu1_percent))
    gpu2_percent = max(0, min(100, gpu2_percent))

    # Create image with transparency
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Calculate dimensions
    padding = 3
    bar_width = (size - 3 * padding) // 2  # Space for 2 bars + gaps
    bar_height = size - 2 * padding

    # GPU 0 bar (left)
    gpu1_filled_height = int(bar_height * gpu1_percent / 100)
    x1_left = padding
    x1_right = padding + bar_width
    y1_top = padding + (bar_height - gpu1_filled_height)
    y1_bottom = padding + bar_height

    # Empty/background portion for GPU 0
    draw.rectangle(
        [x1_left, padding, x1_right, padding + bar_height],
        fill=COLORS["bg_empty"],
        outline=COLORS["border"],
        width=1
    )

    # Filled portion for GPU 0 (only if > 0%)
    if gpu1_filled_height > 0:
        draw.rectangle(
            [x1_left + 1, y1_top, x1_right - 1, y1_bottom - 1],
            fill=get_utilization_color(gpu1_percent),
            outline=None
        )

    # GPU 1 bar (right)
    gpu2_filled_height = int(bar_height * gpu2_percent / 100)
    x2_left = x1_right + padding
    x2_right = x2_left + bar_width
    y2_top = padding + (bar_height - gpu2_filled_height)
    y2_bottom = padding + bar_height

    # Empty/background portion for GPU 1
    draw.rectangle(
        [x2_left, padding, x2_right, padding + bar_height],
        fill=COLORS["bg_empty"],
        outline=COLORS["border"],
        width=1
    )

    # Filled portion for GPU 1 (only if > 0%)
    if gpu2_filled_height > 0:
        draw.rectangle(
            [x2_left + 1, y2_top, x2_right - 1, y2_bottom - 1],
            fill=get_utilization_color(gpu2_percent),
            outline=None
        )

    # Convert to bytes
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()


def create_single_gpu_icon(gpu_percent: float, size: int = 36) -> bytes:
    """
    Create a menu bar icon for a single GPU (fallback).

    Args:
        gpu_percent: GPU utilization (0-100)
        size: Icon size in pixels

    Returns:
        PNG image bytes
    """
    gpu_percent = max(0, min(100, gpu_percent))

    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    padding = 4
    bar_width = size - 2 * padding
    bar_height = size - 2 * padding

    filled_height = int(bar_height * gpu_percent / 100)

    # Background
    draw.rectangle(
        [padding, padding, padding + bar_width, padding + bar_height],
        fill=COLORS["bg_dark"],
        outline=COLORS["border"],
        width=2
    )

    # Filled portion
    if filled_height > 0:
        y_top = padding + (bar_height - filled_height)
        draw.rectangle(
            [padding + 2, y_top, padding + bar_width - 2, padding + bar_height - 2],
            fill=get_utilization_color(gpu_percent),
            outline=None
        )

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()


def create_error_icon(size: int = 36) -> bytes:
    """
    Create an error icon when GPU data cannot be fetched.

    Args:
        size: Icon size in pixels

    Returns:
        PNG image bytes
    """
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw a red X
    padding = 6
    draw.line([padding, padding, size - padding, size - padding], fill='#ff3333', width=3)
    draw.line([padding, size - padding, size - padding, padding], fill='#ff3333', width=3)

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()


if __name__ == "__main__":
    # Test: Create icons at different utilization levels
    import os

    test_dir = "test_icons"
    os.makedirs(test_dir, exist_ok=True)

    # Test various GPU utilization combinations
    test_cases = [
        (0, 0, "idle"),
        (25, 30, "low"),
        (55, 65, "medium"),
        (85, 90, "high"),
        (100, 100, "full"),
        (20, 95, "mixed"),
    ]

    for gpu1, gpu2, label in test_cases:
        icon_bytes = create_dual_gpu_icon(gpu1, gpu2, size=36)
        with open(f"{test_dir}/dual_gpu_{label}_{gpu1}_{gpu2}.png", "wb") as f:
            f.write(icon_bytes)
        print(f"Created icon: GPU0={gpu1}%, GPU1={gpu2}% ({label})")

    # Create error icon
    error_icon = create_error_icon(size=36)
    with open(f"{test_dir}/error_icon.png", "wb") as f:
        f.write(error_icon)
    print("Created error icon")

    # Create larger previews
    for gpu1, gpu2, label in [(25, 75, "preview")]:
        icon_bytes = create_dual_gpu_icon(gpu1, gpu2, size=128)
        with open(f"{test_dir}/dual_gpu_large_{label}.png", "wb") as f:
            f.write(icon_bytes)

    print(f"\nTest icons saved to {test_dir}/")
