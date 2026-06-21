"""Property tests for public coordinate contracts."""

from __future__ import annotations

from hypothesis import given, strategies as st

from visual_annotation import VisualBox, VisualPoint

# =============================================================================
# Strategies
# =============================================================================

_NORMALIZED_START = st.floats(
    min_value=0.0,
    max_value=0.9,
    allow_nan=False,
    allow_infinity=False,
)
_NORMALIZED_SIZE = st.floats(
    min_value=0.001,
    max_value=0.1,
    allow_nan=False,
    allow_infinity=False,
)
_NORMALIZED_POINT = st.floats(
    min_value=0.0,
    max_value=1.0,
    allow_nan=False,
    allow_infinity=False,
)


# =============================================================================
# Properties
# =============================================================================


@given(
    x0=_NORMALIZED_START,
    y0=_NORMALIZED_START,
    width=_NORMALIZED_SIZE,
    height=_NORMALIZED_SIZE,
)
def test_valid_public_boxes_round_trip(
    x0: float,
    y0: float,
    width: float,
    height: float,
) -> None:
    """Verify valid normalized boxes preserve caller coordinates."""
    x1 = min(1.0, x0 + width)
    y1 = min(1.0, y0 + height)

    box = VisualBox(label="target", coord=[x0, y0, x1, y1])

    assert box.coord == [x0, y0, x1, y1]


@given(
    x=_NORMALIZED_POINT,
    y=_NORMALIZED_POINT,
)
def test_valid_public_points_round_trip(x: float, y: float) -> None:
    """Verify valid normalized points preserve caller coordinates."""
    point = VisualPoint(label="target", coord=[x, y])

    assert point.coord == [x, y]
