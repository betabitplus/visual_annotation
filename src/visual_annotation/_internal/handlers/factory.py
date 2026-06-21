"""Private factory for configured annotation handlers."""

from __future__ import annotations

from typing import Any

import supervision as sv
from supervision.annotators.base import BaseAnnotator

from visual_annotation._api.errors import HandlerMappingError
from visual_annotation._api.types import (
    PageElement,
    VisualBox,
    VisualMask,
    VisualPoint,
)
from visual_annotation._internal.config import AnnotatorConfig
from visual_annotation._internal.handlers.base import BaseAnnotationHandler
from visual_annotation._internal.handlers.box import BoxAnnotationHandler
from visual_annotation._internal.handlers.mask import MaskAnnotationHandler
from visual_annotation._internal.handlers.point import PointAnnotationHandler

HANDLER_CLASS_REGISTRY: dict[type[object], type[BaseAnnotationHandler[Any]]] = {
    VisualBox: BoxAnnotationHandler,
    PageElement: BoxAnnotationHandler,
    VisualPoint: PointAnnotationHandler,
    VisualMask: MaskAnnotationHandler,
}


class AnnotationHandlerFactory:
    """Owns supervision annotator setup for one config snapshot."""

    def __init__(self, config: AnnotatorConfig) -> None:
        """Create all supervision annotators from a validated config."""
        self.config = config
        self._sv_annotators = self._initialize_sv_annotators()
        self.label_annotator = self._sv_annotators["label"]

    def get_handlers(self) -> dict[type[object], BaseAnnotationHandler[Any]]:
        """Build the complete element-type handler registry."""
        handler_registry: dict[type[object], BaseAnnotationHandler[Any]] = {}
        for dto_type, handler_class in HANDLER_CLASS_REGISTRY.items():
            annotator_key = getattr(handler_class, "ANNOTATOR_KEY", None)
            if not annotator_key:
                raise HandlerMappingError(
                    handler_name=handler_class.__name__,
                    reason="ANNOTATOR_KEY class attribute is not defined.",
                )

            sv_annotator = self._sv_annotators.get(annotator_key)
            if sv_annotator is None:
                raise HandlerMappingError(
                    handler_name=handler_class.__name__,
                    reason=f"No supervision annotator found for key '{annotator_key}'.",
                )
            handler_registry[dto_type] = handler_class(sv_annotator=sv_annotator)
        return handler_registry

    def _initialize_sv_annotators(self) -> dict[str, BaseAnnotator]:
        """Initialize all supervision annotators for this config."""
        return {
            "mask": sv.MaskAnnotator(
                color=self.config.annotation_color,
                color_lookup=sv.ColorLookup.INDEX,
            ),
            "box": sv.BoxAnnotator(
                color=self.config.annotation_color,
                thickness=self.config.box_thickness,
                color_lookup=sv.ColorLookup.INDEX,
            ),
            "point": sv.DotAnnotator(
                color=self.config.annotation_color,
                radius=self.config.point_radius,
                color_lookup=sv.ColorLookup.INDEX,
            ),
            "label": sv.LabelAnnotator(
                color_lookup=sv.ColorLookup.INDEX,
                color=self.config.annotation_color,
                text_color=self.config.label_color,
                text_scale=self.config.label_text_scale,
                text_padding=self.config.label_text_padding,
                text_thickness=self.config.label_text_thickness,
                smart_position=True,
            ),
        }
