"""Unit tests for the private box annotation handler."""

from __future__ import annotations

from unittest.mock import MagicMock

import numpy as np
import pytest
import supervision as sv

from tests.visual_annotation.support.builders import (
    make_page_elements,
    make_visual_boxes,
)
from visual_annotation._internal.handlers.box import (
    AnnotatableBox,
    BoxAnnotationHandler,
)

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def mock_box_annotator() -> MagicMock:
    """Return a supervision box annotator mock."""
    annotator = MagicMock(spec=sv.BoxAnnotator)
    annotator.annotate.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
    return annotator


# =============================================================================
# Tests
# =============================================================================


def test_handle_visual_boxes_scales_coordinates(mock_box_annotator: MagicMock) -> None:
    """Verify normalized boxes are scaled to image pixels."""
    handler = BoxAnnotationHandler(sv_annotator=mock_box_annotator)
    scene = np.zeros((100, 100, 3), dtype=np.uint8)

    handler.handle(scene, make_visual_boxes())

    detections = mock_box_annotator.annotate.call_args.kwargs["detections"]
    expected_xyxy = np.array(
        [
            [19.0, 65.0, 34.0, 83.0],
            [68.0, 43.0, 82.0, 69.0],
        ],
    )
    np.testing.assert_allclose(np.asarray(detections.xyxy, dtype=float), expected_xyxy)
    assert detections.data["class_name"] == ["car", "truck"]


def test_page_elements_do_not_create_labels(mock_box_annotator: MagicMock) -> None:
    """Verify page elements annotate boxes without label detections."""
    handler = BoxAnnotationHandler(sv_annotator=mock_box_annotator)
    scene = np.zeros((100, 100, 3), dtype=np.uint8)

    _, labeled_detections = handler.handle(scene, make_page_elements())

    detections = mock_box_annotator.annotate.call_args.kwargs["detections"]
    assert len(detections) == 2
    assert "class_name" not in detections.data
    assert labeled_detections is None


def test_empty_box_group_returns_unmodified_scene(
    mock_box_annotator: MagicMock,
) -> None:
    """Verify empty groups avoid annotator calls."""
    handler = BoxAnnotationHandler(sv_annotator=mock_box_annotator)
    scene = np.zeros((100, 100, 3), dtype=np.uint8)
    elements: list[AnnotatableBox] = []

    result_scene, labeled_detections = handler.handle(scene, elements)

    mock_box_annotator.annotate.assert_not_called()
    np.testing.assert_array_equal(result_scene, scene)
    assert labeled_detections is None
