"""Private image annotation runtime.

Why:
    Owns OpenCV/supervision adaptation and element dispatch while the public
    facade stays focused on caller-facing inputs and outputs.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from typing import Any

import cv2
import numpy as np
import supervision as sv
from PIL import Image
from py_lib_runtime import get_logger
from supervision.annotators.base import BaseAnnotator

from visual_annotation._api.types import AnnotatableElement, ImageSchema
from visual_annotation._internal.handlers.base import BaseAnnotationHandler

_LOGGER = get_logger(__name__)


class Annotator:
    """Owns dispatch from public visual elements to configured handlers."""

    def __init__(
        self,
        *,
        handlers: dict[type[object], BaseAnnotationHandler[Any]],
        label_annotator: BaseAnnotator,
    ) -> None:
        """Store runtime handler dependencies."""
        self.handler_registry = handlers
        self.label_annotator = label_annotator

    def annotate(
        self,
        image: ImageSchema,
        elements: Iterable[AnnotatableElement],
    ) -> ImageSchema:
        """Annotate an image with a list of visual elements."""
        scene_rgb = np.array(image.copy())
        scene_bgr = cv2.cvtColor(scene_rgb, cv2.COLOR_RGB2BGR)

        all_labeled_detections: list[sv.Detections] = []
        for element_type, group in self._group_elements_by_type(elements).items():
            handler = self.handler_registry.get(element_type)
            if handler is None:
                type_name = element_type.__name__
                _LOGGER.warning(
                    "No annotation handler found for element type",
                    event_type="visual_annotation.annotation.handler.not_found",
                    type_name=type_name,
                )
                continue

            scene_bgr, labeled_detections = handler.handle(scene_bgr, group)
            if labeled_detections is not None:
                all_labeled_detections.append(labeled_detections)

        if all_labeled_detections:
            combined_detections = sv.Detections.merge(all_labeled_detections)
            scene_bgr = self.label_annotator.annotate(
                scene=scene_bgr,
                detections=combined_detections,
            )

        final_scene_rgb = cv2.cvtColor(scene_bgr, cv2.COLOR_BGR2RGB)
        return Image.fromarray(final_scene_rgb)

    def _group_elements_by_type(
        self,
        elements: Iterable[AnnotatableElement],
    ) -> dict[type[object], list[Any]]:
        """Group annotation elements by concrete runtime type."""
        grouped_elements: dict[type[object], list[Any]] = defaultdict(list)
        for element in elements:
            grouped_elements[type(element)].append(element)
        return dict(grouped_elements)
