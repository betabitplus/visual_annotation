"""Private handler for point annotation elements."""

from __future__ import annotations

from typing import ClassVar, override

import numpy as np
import supervision as sv

from visual_annotation._api.types import VisualPoint
from visual_annotation._internal.handlers.base import BaseAnnotationHandler


class PointAnnotationHandler(BaseAnnotationHandler[VisualPoint]):
    """Converts `VisualPoint` objects into dot detections."""

    ANNOTATOR_KEY: ClassVar[str] = "point"

    @override
    def _to_detections(self, elements: list[VisualPoint]) -> sv.Detections:
        """Convert point DTOs to supervision detections."""
        coords_xy = np.array([element.coord for element in elements])
        labels = [element.label for element in elements]

        coords_xyxy = np.hstack([coords_xy, coords_xy])
        detections = sv.Detections(xyxy=coords_xyxy)
        detections.xy = coords_xy

        if any(labels):
            detections.data["class_name"] = labels
        return detections
