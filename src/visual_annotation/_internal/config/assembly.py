"""Built-in config assembly.

Why:
    Converts public default declarations into validated private config
    snapshots before runtime work begins.
"""

from __future__ import annotations

from py_lib_runtime import get_logger

from visual_annotation._api import defaults as api_defaults
from visual_annotation._internal.config.models import AnnotatorConfig
from visual_annotation._internal.config.validation import validate_config

logger = get_logger(__name__)


def build_default_config() -> AnnotatorConfig:
    """Assemble and validate the built-in runtime config snapshot."""
    config = AnnotatorConfig(
        annotation_color=api_defaults.DEFAULT_ANNOTATION_COLOR_NAME,
        label_color=api_defaults.DEFAULT_LABEL_COLOR_NAME,
        box_thickness=api_defaults.DEFAULT_BOX_THICKNESS,
        point_radius=api_defaults.DEFAULT_POINT_RADIUS,
        label_text_scale=api_defaults.DEFAULT_LABEL_TEXT_SCALE,
        label_text_padding=api_defaults.DEFAULT_LABEL_TEXT_PADDING,
        label_text_thickness=api_defaults.DEFAULT_LABEL_TEXT_THICKNESS,
    )
    validate_config(config)
    logger.info(
        "Runtime config resolved",
        event_type="visual_annotation.config.runtime.resolved",
        box_thickness=config.box_thickness,
        point_radius=config.point_radius,
    )
    return config
