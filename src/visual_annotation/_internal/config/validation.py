"""Runtime config validation helpers.

Why:
    Centralizes color normalization and numeric invariants before config
    snapshots are constructed or installed.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import supervision as sv
from py_lib_runtime import (
    validate_non_negative_int,
    validate_positive_float,
    validate_positive_int,
)

from visual_annotation._api.errors import InvalidConfigValueError

if TYPE_CHECKING:
    from visual_annotation._internal.config.models import AnnotatorConfig


def coerce_color(*, field_name: str, value: object) -> sv.Color:
    """Return a `supervision.Color` from a public color input."""
    if isinstance(value, sv.Color):
        return value
    if not isinstance(value, str):
        msg = f"AnnotatorConfig.{field_name} must be a color name or sv.Color."
        raise TypeError(msg)

    candidate = getattr(sv.Color, value.upper(), None)
    if isinstance(candidate, sv.Color):
        return candidate
    raise InvalidConfigValueError(
        field=field_name,
        value=value,
        reason="it is not a valid sv.Color member",
    )


def validate_config(config: AnnotatorConfig) -> None:
    """Validate one visual annotation config snapshot."""
    coerce_color(field_name="annotation_color", value=config.annotation_color)
    coerce_color(field_name="label_color", value=config.label_color)
    validate_positive_int(
        field_name="AnnotatorConfig.box_thickness",
        value=config.box_thickness,
    )
    validate_positive_int(
        field_name="AnnotatorConfig.point_radius",
        value=config.point_radius,
    )
    validate_positive_float(
        field_name="AnnotatorConfig.label_text_scale",
        value=config.label_text_scale,
    )
    validate_non_negative_int(
        field_name="AnnotatorConfig.label_text_padding",
        value=config.label_text_padding,
    )
    validate_positive_int(
        field_name="AnnotatorConfig.label_text_thickness",
        value=config.label_text_thickness,
    )
