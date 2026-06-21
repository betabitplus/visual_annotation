"""Private mask geometry helpers.

Why:
    Keeps mask-to-box conversion close to the mask handler that consumes it.
"""

from __future__ import annotations

import numpy as np


def mask2bbox(mask: np.ndarray) -> np.ndarray:
    """Convert a boolean mask to a normalized bounding box in `xyxy` order."""
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    if not np.any(rows) or not np.any(cols):
        return np.zeros(4, dtype=np.float32)

    ymin, ymax = np.where(rows)[0][[0, -1]]
    xmin, xmax = np.where(cols)[0][[0, -1]]

    bbox = np.array([xmin, ymin, xmax + 1, ymax + 1], dtype=np.float32)
    return bbox / np.tile(mask.shape[::-1], 2)
