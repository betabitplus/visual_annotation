"""Private base class for annotation handlers.

Why:
    Centralizes coordinate scaling and supervision annotator invocation so each
    concrete handler only owns DTO-to-detections translation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

import numpy as np
import supervision as sv
from supervision.annotators.base import BaseAnnotator


class BaseAnnotationHandler[T](ABC):
    """Owns the template method for one annotation element family."""

    ANNOTATOR_KEY: ClassVar[str]

    def __init__(self, sv_annotator: BaseAnnotator) -> None:
        """Store the configured supervision annotator for this handler."""
        self.sv_annotator = sv_annotator

    @abstractmethod
    def _to_detections(self, elements: list[T]) -> sv.Detections:
        """Convert public DTOs into supervision detections."""
        raise NotImplementedError

    def _scale_detections(
        self,
        detections: sv.Detections,
        scene_shape: tuple[int, int, int],
    ) -> sv.Detections:
        """Scale normalized coordinates to absolute image pixels."""
        height, width, _ = scene_shape
        if len(detections.xyxy) > 0:
            detections.xyxy = detections.xyxy * np.array([width, height, width, height])

        xy = getattr(detections, "xy", None)
        if xy is not None and len(xy) > 0:
            detections.xy = xy * np.array([width, height])
        return detections

    def handle(
        self,
        scene: np.ndarray,
        elements: list[T],
    ) -> tuple[np.ndarray, sv.Detections | None]:
        """Annotate one homogeneous element group."""
        if not elements:
            return scene, None

        detections = self._to_detections(elements)
        if len(detections) == 0:
            return scene, None

        detections = self._scale_detections(detections, scene.shape)
        annotated_scene = self.sv_annotator.annotate(
            scene=scene.copy(),
            detections=detections,
        )
        labeled_detections = detections if "class_name" in detections.data else None
        return annotated_scene, labeled_detections
