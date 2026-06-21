"""Internal contracts for annotation runtime seams.

Why:
    Keeps trusted runtime DTOs out of the public request models while preserving
    a typed boundary between resolution and drawing.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from visual_annotation._api.types import (
    AnnotatableElement,
    ImageSchema,
    PageElement,
    VisualBox,
    VisualMask,
    VisualPoint,
)

_ANNOTATABLE_TYPES = (PageElement, VisualBox, VisualMask, VisualPoint)


def _validate_elements(elements: object) -> list[AnnotatableElement]:
    """Validate a materialized runtime element list."""
    if not isinstance(elements, list):
        msg = "elements must be materialized as a list."
        raise TypeError(msg)
    if not all(isinstance(element, _ANNOTATABLE_TYPES) for element in elements):
        msg = "elements must contain only annotatable visual elements."
        raise TypeError(msg)
    return cast("list[AnnotatableElement]", elements)


@dataclass(frozen=True, slots=True)
class AnnotationTask:
    """Trusted annotation task created after public request validation."""

    image: ImageSchema
    elements: list[AnnotatableElement]

    def __post_init__(self) -> None:
        """Validate the materialized runtime element list."""
        object.__setattr__(
            self, "elements", _validate_elements(cast("object", self.elements))
        )
