"""Built-in default declarations for visual annotation.

Why:
    Keeps appearance, coordinate, and media validation defaults in one
    declarative layer so runtime modules do not scatter literals.

How:
    Treat these values as source declarations. Public config construction and
    private runtime setup derive validated snapshots from them.
"""

from __future__ import annotations

# ================================================================================
# Annotation Appearance Defaults
# ================================================================================

# Options: RED | GREEN | BLUE | YELLOW | WHITE | BLACK | etc.
# Must be a valid `supervision.Color` enum member.
DEFAULT_ANNOTATION_COLOR_NAME: str = "RED"
DEFAULT_LABEL_COLOR_NAME: str = "WHITE"

# Range: >0, thickness of bounding box lines in pixels.
DEFAULT_BOX_THICKNESS: int = 2

# Range: >0, radius of point markers in pixels.
DEFAULT_POINT_RADIUS: int = 4

# Range: >0.0, scale factor for label text size.
DEFAULT_LABEL_TEXT_SCALE: float = 0.7

# Range: 0+, padding around label text in pixels.
DEFAULT_LABEL_TEXT_PADDING: int = 2

# Range: >0, thickness of label text in pixels.
DEFAULT_LABEL_TEXT_THICKNESS: int = 2

# ================================================================================
# Coordinate And Image Validation Defaults
# ================================================================================

BBOX_NUM_ELEMENTS: int = 4
POINT_NUM_ELEMENTS: int = 2

# Minimum 10x10 pixels.
MIN_IMAGE_DIMENSION: int = 10

# Maximum 16384x16384 pixels, matching the feature-branch GPU-oriented limit.
MAX_IMAGE_DIMENSION: int = 16_384

# Supported downstream modes for PIL, OpenCV conversion, annotation, and LLM usage.
ALLOWED_IMAGE_MODES: frozenset[str] = frozenset({"RGB", "RGBA", "L", "LA", "P", "PA"})
