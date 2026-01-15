#!/usr/bin/env python3
"""
Create application icon for GPU Monitor.
Generates a 1024x1024 icon showing two GPU bars.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon(size=1024):
    """Create application icon."""
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    bg_color = (45, 55, 72, 255)      # Dark gray background
    border_color = (113, 128, 150, 255)  # Gray border
    gpu_green = (72, 187, 120, 255)   # Green
    gpu_orange = (237, 137, 54, 255)  # Orange
    gpu_red = (245, 101, 101, 255)    # Red

    # Calculate dimensions
    padding = size // 8
    center_x = size // 2

    # Draw background circle
    circle_bbox = [padding, padding, size - padding, size - padding]
    draw.ellipse(circle_bbox, fill=bg_color, outline=border_color, width=size//50)

    # Draw two GPU bars in the center
    bar_width = size // 6
    bar_height = size // 2
    gap = size // 20

    # GPU 0 bar (left) - showing ~60% utilization (orange)
    x1_left = center_x - bar_width - gap // 2
    x1_right = center_x - gap // 2
    y1_bottom = center_x + bar_height // 2
    y1_top_full = center_x - bar_height // 2
    y1_top_filled = y1_bottom - int(bar_height * 0.6)  # 60% filled

    # Empty portion
    draw.rectangle(
        [x1_left, y1_top_full, x1_right, y1_bottom],
        fill=(70, 80, 100, 255),
        outline=border_color,
        width=size//80
    )

    # Filled portion (orange - medium load)
    draw.rectangle(
        [x1_left + size//80, y1_top_filled, x1_right - size//80, y1_bottom - size//80],
        fill=gpu_orange,
        outline=None
    )

    # GPU 1 bar (right) - showing ~80% utilization (red)
    x2_left = center_x + gap // 2
    x2_right = center_x + bar_width + gap // 2
    y2_bottom = center_x + bar_height // 2
    y2_top_full = center_x - bar_height // 2
    y2_top_filled = y2_bottom - int(bar_height * 0.8)  # 80% filled

    # Empty portion
    draw.rectangle(
        [x2_left, y2_top_full, x2_right, y2_bottom],
        fill=(70, 80, 100, 255),
        outline=border_color,
        width=size//80
    )

    # Filled portion (red - high load)
    draw.rectangle(
        [x2_left + size//80, y2_top_filled, x2_right - size//80, y2_bottom - size//80],
        fill=gpu_red,
        outline=None
    )

    # Add small "GPU" text at bottom (optional)
    try:
        font_size = size // 12
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        text = "GPU"

        # Get text bbox for centering
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = (size - text_width) // 2
        text_y = y1_bottom + size // 15

        draw.text((text_x, text_y), text, fill=(200, 200, 200, 255), font=font)
    except:
        pass  # Skip text if font not available

    return img


if __name__ == "__main__":
    print("Creating GPU Monitor application icon...")

    # Create icons directory
    icons_dir = os.path.join(os.path.dirname(__file__), "..", "icons")
    os.makedirs(icons_dir, exist_ok=True)

    # Create icon at various sizes
    sizes = [1024, 512, 256, 128, 64, 32, 16]

    for size in sizes:
        icon = create_app_icon(size)
        output_path = os.path.join(icons_dir, f"icon_{size}x{size}.png")
        icon.save(output_path, "PNG")
        print(f"  Created: {output_path}")

    # Create the main icon (1024x1024 for macOS)
    icon = create_app_icon(1024)
    main_icon_path = os.path.join(icons_dir, "AppIcon.png")
    icon.save(main_icon_path, "PNG")
    print(f"  Created: {main_icon_path}")

    print("\n✓ Application icons created successfully!")
    print(f"  Location: {icons_dir}/")
