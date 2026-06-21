"""Unit tests for the private point annotation handler."""

from __future__ import annotations

from unittest.mock import MagicMock

import numpy as np
import pytest
import supervision as sv

from tests.visual_annotation.support.builders import make_visual_points
from visual_annotation._internal.handlers.point import PointAnnotationHandler

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def mock_dot_annotator() -> MagicMock:
    """Return a supervision dot annotator mock."""
    annotator = MagicMock(spec=sv.DotAnnotator)
    annotator.annotate.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
    return annotator


# =============================================================================
# Tests
# =============================================================================


def test_handle_visual_points_scales_xy_anchor(mock_dot_annotator: MagicMock) -> None:
    """Verify point handler scales the dynamic `xy` anchor used by supervision."""
    handler = PointAnnotationHandler(sv_annotator=mock_dot_annotator)
    scene = np.zeros((100, 100, 3), dtype=np.uint8)

    handler.handle(scene, make_visual_points())

    detections = mock_dot_annotator.annotate.call_args.kwargs["detections"]
    expected_xy = np.array([[26.0, 74.0], [75.0, 56.0]])
    np.testing.assert_allclose(np.asarray(detections.xy, dtype=float), expected_xy)
    assert detections.data["class_name"] == ["car", "truck"]
