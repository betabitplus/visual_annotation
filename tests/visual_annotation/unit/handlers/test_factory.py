"""Unit tests for private annotation handler factory setup."""

from __future__ import annotations

import supervision as sv

from tests.visual_annotation.support.builders import make_annotator_config
from visual_annotation import PageElement, VisualBox, VisualMask, VisualPoint
from visual_annotation._internal.handlers.box import BoxAnnotationHandler
from visual_annotation._internal.handlers.factory import AnnotationHandlerFactory
from visual_annotation._internal.handlers.mask import MaskAnnotationHandler
from visual_annotation._internal.handlers.point import PointAnnotationHandler

# =============================================================================
# Tests
# =============================================================================


def test_factory_initializes_all_handler_types() -> None:
    """Verify the runtime factory covers every public element type."""
    factory = AnnotationHandlerFactory(make_annotator_config())

    registry = factory.get_handlers()

    assert isinstance(registry[VisualBox], BoxAnnotationHandler)
    assert isinstance(registry[PageElement], BoxAnnotationHandler)
    assert isinstance(registry[VisualPoint], PointAnnotationHandler)
    assert isinstance(registry[VisualMask], MaskAnnotationHandler)
    assert isinstance(factory.label_annotator, sv.LabelAnnotator)
