"""Supported public package entrypoint for visual annotation.

Why:
    Provides the one stable import boundary callers use to annotate images with
    visual boxes, points, masks, and page elements.

What belongs here:
    Re-exports of public facades, DTOs, config objects, public exceptions, and
    package version.

What does not belong here:
    Raw defaults, private runtime helpers, handlers, adapters, or implementation
    details.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from visual_annotation._api.annotation import annotate
from visual_annotation._api.config import AnnotatorConfig, get_config, install_config
from visual_annotation._api.errors import (
    AnnotatorConfigError,
    AnnotatorError,
    BboxCoordinatesOutOfRangeError,
    BboxInvalidLengthError,
    BboxInvalidPointsOrderError,
    BboxValidationError,
    HandlerMappingError,
    ImageDimensionError,
    ImageModeError,
    ImageTooLargeError,
    ImageTooSmallError,
    ImageValidationError,
    InvalidConfigValueError,
    PointCoordinatesOutOfRangeError,
    PointInvalidLengthError,
    PointValidationError,
    VideoFileNotFoundError,
    VideoUrlInvalidError,
    VideoValidationError,
    VisualAnnotationError,
)
from visual_annotation._api.media import format_video_offset
from visual_annotation._api.types import (
    AnnotatableElement,
    AnnotationRequest,
    AnnotationResponse,
    BoundingBox,
    ImageSchema,
    PageElement,
    Point,
    Pointer,
    VideoSchema,
    VideoUrlSchema,
    VisualBox,
    VisualMask,
    VisualPoint,
)

# ================================================================================
# Package Metadata
# ================================================================================

try:
    __version__ = version("visual-annotation")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0+local"

# ================================================================================
# Public API
# ================================================================================

__all__ = [
    "AnnotatableElement",
    "AnnotationRequest",
    "AnnotationResponse",
    "AnnotatorConfig",
    "AnnotatorConfigError",
    "AnnotatorError",
    "BboxCoordinatesOutOfRangeError",
    "BboxInvalidLengthError",
    "BboxInvalidPointsOrderError",
    "BboxValidationError",
    "BoundingBox",
    "HandlerMappingError",
    "ImageDimensionError",
    "ImageModeError",
    "ImageSchema",
    "ImageTooLargeError",
    "ImageTooSmallError",
    "ImageValidationError",
    "InvalidConfigValueError",
    "PageElement",
    "Point",
    "PointCoordinatesOutOfRangeError",
    "PointInvalidLengthError",
    "PointValidationError",
    "Pointer",
    "VideoFileNotFoundError",
    "VideoSchema",
    "VideoUrlInvalidError",
    "VideoUrlSchema",
    "VideoValidationError",
    "VisualAnnotationError",
    "VisualBox",
    "VisualMask",
    "VisualPoint",
    "__version__",
    "annotate",
    "format_video_offset",
    "get_config",
    "install_config",
]
