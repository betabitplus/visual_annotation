"""Public annotation facade.

Why:
    Keeps the caller-facing `annotate(...)` signature small while private
    implementation code owns runtime orchestration and drawing.
"""

from __future__ import annotations

from collections.abc import Iterable

from visual_annotation._api.config import AnnotatorConfig
from visual_annotation._api.types import (
    AnnotatableElement,
    AnnotationRequest,
    AnnotationResponse,
    ImageSchema,
)
from visual_annotation._internal import annotate_request

# ================================================================================
# Public API
# ================================================================================


def annotate(
    image: ImageSchema,
    elements: Iterable[AnnotatableElement],
    *,
    config: AnnotatorConfig | None = None,
    correlation_id: str | None = None,
) -> AnnotationResponse:
    """Annotate an image with visual elements."""
    request = AnnotationRequest(image=image, elements=elements)
    return annotate_request(request, config=config, correlation_id=correlation_id)
