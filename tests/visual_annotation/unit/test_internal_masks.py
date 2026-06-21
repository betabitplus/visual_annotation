"""Unit tests for private mask geometry."""

from __future__ import annotations

import numpy as np

from visual_annotation._internal.masks import mask2bbox

# =============================================================================
# Tests
# =============================================================================


def test_simple_rectangular_mask() -> None:
    """Convert a simple rectangular mask to a normalized bbox."""
    mask = np.zeros((100, 100), dtype=bool)
    mask[20:80, 30:70] = True

    bbox = mask2bbox(mask)

    np.testing.assert_array_almost_equal(
        bbox,
        np.array([0.3, 0.2, 0.7, 0.8], dtype=np.float32),
    )


def test_empty_mask_returns_zero_bbox() -> None:
    """Preserve the empty-mask zero bbox contract."""
    mask = np.zeros((100, 100), dtype=bool)

    np.testing.assert_array_equal(mask2bbox(mask), np.zeros(4, dtype=np.float32))


def test_non_square_mask_uses_width_height_order() -> None:
    """Verify normalization divides x by width and y by height."""
    mask = np.zeros((50, 100), dtype=bool)
    mask[10:40, 20:80] = True

    bbox = mask2bbox(mask)

    np.testing.assert_array_almost_equal(
        bbox,
        np.array([0.2, 0.2, 0.8, 0.8], dtype=np.float32),
    )
