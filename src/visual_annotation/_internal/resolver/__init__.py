"""Private request resolver.

Why:
    Materializes the public iterable of elements once before handlers consume a
    trusted task snapshot.
"""

from __future__ import annotations

from visual_annotation._api.errors import AnnotatorError
from visual_annotation._api.types import AnnotationRequest
from visual_annotation._internal.contracts import AnnotationTask


class AnnotationTaskResolver:
    """Validates a public request into an internal annotation task."""

    def resolve(self, request: AnnotationRequest) -> AnnotationTask:
        """Return the trusted task consumed by the drawing runtime."""
        try:
            return AnnotationTask(
                image=request.image,
                elements=list(request.elements),
            )
        except (TypeError, ValueError) as exc:
            message = "Annotation request could not be resolved."
            raise AnnotatorError(message, cause=exc) from exc
