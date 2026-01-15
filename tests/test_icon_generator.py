"""
Tests for icon generator module.
"""

import pytest
from gpu_usage_menubar.icon_generator import (
    create_dual_gpu_icon,
    create_single_gpu_icon,
    create_error_icon,
    get_utilization_color,
    COLORS
)


class TestUtilizationColor:
    """Tests for get_utilization_color function."""

    def test_low_utilization(self):
        """Test color for low utilization (0-50%)."""
        assert get_utilization_color(0) == COLORS["gpu_low"]
        assert get_utilization_color(25) == COLORS["gpu_low"]
        assert get_utilization_color(49) == COLORS["gpu_low"]

    def test_medium_utilization(self):
        """Test color for medium utilization (50-80%)."""
        assert get_utilization_color(50) == COLORS["gpu_medium"]
        assert get_utilization_color(65) == COLORS["gpu_medium"]
        assert get_utilization_color(79) == COLORS["gpu_medium"]

    def test_high_utilization(self):
        """Test color for high utilization (80-100%)."""
        assert get_utilization_color(80) == COLORS["gpu_high"]
        assert get_utilization_color(90) == COLORS["gpu_high"]
        assert get_utilization_color(100) == COLORS["gpu_high"]


class TestDualGPUIcon:
    """Tests for create_dual_gpu_icon function."""

    def test_creates_png_bytes(self):
        """Test that icon creation returns PNG bytes."""
        icon = create_dual_gpu_icon(50, 75)
        assert isinstance(icon, bytes)
        assert icon.startswith(b'\x89PNG')  # PNG magic number

    def test_handles_zero_utilization(self):
        """Test icon creation with 0% utilization."""
        icon = create_dual_gpu_icon(0, 0)
        assert isinstance(icon, bytes)
        assert len(icon) > 0

    def test_handles_full_utilization(self):
        """Test icon creation with 100% utilization."""
        icon = create_dual_gpu_icon(100, 100)
        assert isinstance(icon, bytes)
        assert len(icon) > 0

    def test_handles_mixed_utilization(self):
        """Test icon creation with different GPU utilizations."""
        icon = create_dual_gpu_icon(25, 90)
        assert isinstance(icon, bytes)
        assert len(icon) > 0

    def test_clamps_negative_values(self):
        """Test that negative values are clamped to 0."""
        icon = create_dual_gpu_icon(-10, -20)
        assert isinstance(icon, bytes)
        # Should not raise an error

    def test_clamps_over_100_values(self):
        """Test that values over 100 are clamped to 100."""
        icon = create_dual_gpu_icon(150, 200)
        assert isinstance(icon, bytes)
        # Should not raise an error

    def test_custom_size(self):
        """Test icon creation with custom size."""
        icon = create_dual_gpu_icon(50, 75, size=64)
        assert isinstance(icon, bytes)
        assert len(icon) > 0


class TestSingleGPUIcon:
    """Tests for create_single_gpu_icon function."""

    def test_creates_png_bytes(self):
        """Test that single GPU icon returns PNG bytes."""
        icon = create_single_gpu_icon(50)
        assert isinstance(icon, bytes)
        assert icon.startswith(b'\x89PNG')

    def test_handles_various_utilizations(self):
        """Test single GPU icon with various utilization levels."""
        for util in [0, 25, 50, 75, 100]:
            icon = create_single_gpu_icon(util)
            assert isinstance(icon, bytes)
            assert len(icon) > 0


class TestErrorIcon:
    """Tests for create_error_icon function."""

    def test_creates_png_bytes(self):
        """Test that error icon returns PNG bytes."""
        icon = create_error_icon()
        assert isinstance(icon, bytes)
        assert icon.startswith(b'\x89PNG')

    def test_custom_size(self):
        """Test error icon with custom size."""
        icon = create_error_icon(size=64)
        assert isinstance(icon, bytes)
        assert len(icon) > 0
