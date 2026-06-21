"""Integration tests for private visual annotation service orchestration."""

from __future__ import annotations

from typing import Any

import pytest

from tests.visual_annotation.support.builders import (
    make_annotation_request,
    make_annotator_config,
    make_image,
    make_visual_boxes,
)
from visual_annotation import AnnotationResponse, AnnotatorError
from visual_annotation._internal.contracts import AnnotationTask
from visual_annotation._internal.service import VisualAnnotationService

# =============================================================================
# Helpers
# =============================================================================


class MockAnnotator:
    """Mock drawing runtime used to isolate service orchestration."""

    def __init__(
        self,
        *,
        mock_result: Any | None = None,
        should_fail: bool = False,
        fail_exception: Exception | None = None,
    ) -> None:
        """Store mock behavior and call evidence."""
        self.mock_result = mock_result or make_image()
        self.should_fail = should_fail
        self.fail_exception = fail_exception
        self.call_count = 0
        self.last_image: Any | None = None
        self.last_elements: list[Any] | None = None

    def annotate(self, image: Any, elements: Any) -> Any:
        """Record the annotation call and return configured behavior."""
        self.call_count += 1
        self.last_image = image
        self.last_elements = list(elements)
        if self.should_fail:
            raise self.fail_exception or RuntimeError("Mock failure")
        return self.mock_result


class MockResolver:
    """Mock request resolver used to isolate service orchestration."""

    def __init__(
        self,
        *,
        should_fail: bool = False,
        fail_exception: Exception | None = None,
    ) -> None:
        """Store mock behavior and call evidence."""
        self.should_fail = should_fail
        self.fail_exception = fail_exception
        self.call_count = 0

    def resolve(self, request: Any) -> AnnotationTask:
        """Record the resolve call and return configured behavior."""
        self.call_count += 1
        if self.should_fail:
            raise self.fail_exception or RuntimeError("Mock resolver failure")
        return AnnotationTask(image=request.image, elements=list(request.elements))


# =============================================================================
# Tests
# =============================================================================


def test_service_uses_injected_resolver() -> None:
    """Verify service delegates request resolution through the resolver seam."""
    resolver = MockResolver()
    service = VisualAnnotationService(config=make_annotator_config(), resolver=resolver)
    service._annotator = MockAnnotator()

    service.annotate(make_annotation_request())

    assert resolver.call_count == 1


def test_service_delegates_to_annotator() -> None:
    """Verify service passes resolved task data to the drawing runtime."""
    expected_image = make_image(width=200, height=200)
    mock_annotator = MockAnnotator(mock_result=expected_image)
    service = VisualAnnotationService(config=make_annotator_config())
    service._annotator = mock_annotator

    image = make_image()
    elements = make_visual_boxes()
    response = service.annotate(make_annotation_request(image=image, elements=elements))

    assert isinstance(response, AnnotationResponse)
    assert mock_annotator.call_count == 1
    assert response.response_data == expected_image
    assert response.metadata["element_count"] == 2
    assert mock_annotator.last_image == image
    assert mock_annotator.last_elements == elements


def test_service_wraps_annotator_failures() -> None:
    """Verify lower-level drawing failures cross the service as `AnnotatorError`."""
    service = VisualAnnotationService(config=make_annotator_config())
    service._annotator = MockAnnotator(
        should_fail=True,
        fail_exception=RuntimeError("Internal failure"),
    )

    with pytest.raises(AnnotatorError) as exc_info:
        service.annotate(make_annotation_request(elements=make_visual_boxes()))

    assert isinstance(exc_info.value.__cause__, RuntimeError)
    assert exc_info.value.context["element_count"] == 2


def test_service_wraps_unexpected_resolver_failures() -> None:
    """Verify unexpected resolver failures are translated at the service boundary."""
    service = VisualAnnotationService(
        config=make_annotator_config(),
        resolver=MockResolver(should_fail=True, fail_exception=ValueError("bad data")),
    )

    with pytest.raises(AnnotatorError) as exc_info:
        service.annotate(make_annotation_request())

    assert isinstance(exc_info.value.__cause__, ValueError)
