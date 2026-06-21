"""Private handler for mask annotation elements."""

from __future__ import annotations

from typing import ClassVar, override

import numpy as np
import supervision as sv

from visual_annotation._api.types import VisualMask
from visual_annotation._internal.handlers.base import BaseAnnotationHandler
from visual_annotation._internal.masks import mask2bbox


class MaskAnnotationHandler(BaseAnnotationHandler[VisualMask]):
    """Converts `VisualMask` objects into mask detections."""

    ANNOTATOR_KEY: ClassVar[str] = "mask"

    @override
    def _to_detections(self, elements: list[VisualMask]) -> sv.Detections:
        """Convert mask DTOs to supervision detections."""
        masks = np.array([element.coord for element in elements])
        bboxes = np.array([mask2bbox(mask) for mask in masks])
        labels = [element.label for element in elements]

        detections = sv.Detections(xyxy=bboxes, mask=masks)
        if any(labels):
            detections.data["class_name"] = labels
        return detections
