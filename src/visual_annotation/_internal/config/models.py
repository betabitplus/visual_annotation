"""Runtime configuration models.

Why:
    Defines immutable config snapshots consumed by the private annotation
    runtime.
"""

from __future__ import annotations

from dataclasses import dataclass

import supervision as sv
from py_lib_runtime import (
    validate_non_negative_int,
    validate_positive_float,
    validate_positive_int,
)

from visual_annotation._api import defaults as api_defaults
from visual_annotation._internal.config.validation import coerce_color


@dataclass(frozen=True, slots=True)
class AnnotatorConfig:
    """Owns visual appearance options for one annotation runtime snapshot.

    Invariant:
        Colors are normalized to `supervision.Color`; numeric fields are inside
        the ranges declared in `_api.defaults`.
    """

    annotation_color: str | sv.Color = api_defaults.DEFAULT_ANNOTATION_COLOR_NAME
    label_color: str | sv.Color = api_defaults.DEFAULT_LABEL_COLOR_NAME
    box_thickness: int = api_defaults.DEFAULT_BOX_THICKNESS
    point_radius: int = api_defaults.DEFAULT_POINT_RADIUS
    label_text_scale: float = api_defaults.DEFAULT_LABEL_TEXT_SCALE
    label_text_padding: int = api_defaults.DEFAULT_LABEL_TEXT_PADDING
    label_text_thickness: int = api_defaults.DEFAULT_LABEL_TEXT_THICKNESS

    def __post_init__(self) -> None:
        """Normalize and validate all public config values."""
        object.__setattr__(
            self,
            "annotation_color",
            coerce_color(field_name="annotation_color", value=self.annotation_color),
        )
        object.__setattr__(
            self,
            "label_color",
            coerce_color(field_name="label_color", value=self.label_color),
        )
        validate_positive_int(
            field_name="AnnotatorConfig.box_thickness",
            value=self.box_thickness,
        )
        validate_positive_int(
            field_name="AnnotatorConfig.point_radius",
            value=self.point_radius,
        )
        validate_positive_float(
            field_name="AnnotatorConfig.label_text_scale",
            value=self.label_text_scale,
        )
        validate_non_negative_int(
            field_name="AnnotatorConfig.label_text_padding",
            value=self.label_text_padding,
        )
        validate_positive_int(
            field_name="AnnotatorConfig.label_text_thickness",
            value=self.label_text_thickness,
        )
