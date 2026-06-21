"""Private handler for box-like annotation elements."""

from __future__ import annotations

from typing import ClassVar, override

import numpy as np
import supervision as sv

from visual_annotation._api.types import PageElement, VisualBox
from visual_annotation._internal.handlers.base import BaseAnnotationHandler

AnnotatableBox = VisualBox | PageElement


class BoxAnnotationHandler(BaseAnnotationHandler[AnnotatableBox]):
    """Converts `VisualBox` and `PageElement` objects into box detections."""

    ANNOTATOR_KEY: ClassVar[str] = "box"

    @override
    def _to_detections(self, elements: list[AnnotatableBox]) -> sv.Detections:
        """Convert box-like DTOs to supervision detections."""
        if not elements:
            return sv.Detections.empty()

        coords = np.array([element.coord for element in elements])
        detections = sv.Detections(xyxy=coords)

        labels = [
            element.label
            for element in elements
            if isinstance(element, VisualBox) and element.label
        ]
        if labels:
            detections.data["class_name"] = [
                element.label for element in elements if isinstance(element, VisualBox)
            ]
        return detections
