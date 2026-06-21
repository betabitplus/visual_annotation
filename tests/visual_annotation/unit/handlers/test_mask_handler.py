"""Unit tests for the private mask annotation handler."""

from __future__ import annotations

from unittest.mock import MagicMock

import numpy as np
import pytest
import supervision as sv

from tests.visual_annotation.support.builders import make_image, make_visual_masks
from visual_annotation._internal.handlers.mask import MaskAnnotationHandler

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def mock_mask_annotator() -> MagicMock:
    """Return a supervision mask annotator mock."""
    annotator = MagicMock(spec=sv.MaskAnnotator)
    annotator.annotate.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
    return annotator


# =============================================================================
# Tests
# =============================================================================


def test_handle_visual_masks_derives_scaled_boxes(
    mock_mask_annotator: MagicMock,
) -> None:
    """Verify masks derive bbox geometry before supervision annotation."""
    handler = MaskAnnotationHandler(sv_annotator=mock_mask_annotator)
    image = make_image()
    scene = np.zeros((100, 100, 3), dtype=np.uint8)

    handler.handle(scene, make_visual_masks(image))

    detections = mock_mask_annotator.annotate.call_args.kwargs["detections"]
    expected_xyxy = np.array(
        [
            [19.0, 65.0, 34.0, 81.0],
            [68.0, 43.0, 83.0, 68.0],
        ],
    )
    np.testing.assert_allclose(np.asarray(detections.xyxy, dtype=float), expected_xyxy)
    assert detections.data["class_name"] == ["car", "truck"]
