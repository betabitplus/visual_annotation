"""Public DTOs and vocabulary for visual annotation.

Why:
    Keeps caller-facing request, response, coordinate, image, and annotation
    element contracts stable at the public boundary.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from PIL import Image

from visual_annotation._api.defaults import (
    ALLOWED_IMAGE_MODES,
    BBOX_NUM_ELEMENTS,
    MAX_IMAGE_DIMENSION,
    MIN_IMAGE_DIMENSION,
    POINT_NUM_ELEMENTS,
)
from visual_annotation._api.errors import (
    BboxCoordinatesOutOfRangeError,
    BboxInvalidLengthError,
    BboxInvalidPointsOrderError,
    ImageDimensionError,
    ImageModeError,
    ImageTooLargeError,
    ImageTooSmallError,
    PointCoordinatesOutOfRangeError,
    PointInvalidLengthError,
    VideoFileNotFoundError,
    VideoUrlInvalidError,
)

# ================================================================================
# Public Vocabulary
# ================================================================================


class Pointer(StrEnum):
    """Pointer annotation variants consumed by visual annotators."""

    BBOX = "bbox"
    MASK = "mask"
    POINT = "point"


# ================================================================================
# Coordinate And Media Types
# ================================================================================

type BoundingBox = list[float]
type Point = list[float]
type ImageSchema = Image.Image


# ================================================================================
# Validation Helpers
# ================================================================================


class _Validation:
    """Local validators used by public DTO construction."""

    @staticmethod
    def coerce_float_list(value: object, *, field_name: str) -> list[float]:
        """Return a copied list of numeric coordinates."""
        if not isinstance(value, Sequence) or isinstance(value, str | bytes):
            msg = f"{field_name} must be a sequence of numeric coordinates."
            raise TypeError(msg)

        coords: list[float] = []
        for coord in value:
            if isinstance(coord, bool) or not isinstance(coord, int | float):
                msg = f"{field_name} must contain only numeric coordinates."
                raise TypeError(msg)
            coords.append(float(coord))
        return coords

    @staticmethod
    def check_bbox(bbox: object) -> BoundingBox:
        """Validate normalized bounding-box coordinates."""
        coords = _Validation.coerce_float_list(bbox, field_name="coord")
        if len(coords) != BBOX_NUM_ELEMENTS:
            raise BboxInvalidLengthError(len(coords), BBOX_NUM_ELEMENTS)
        if not all(0 <= coord <= 1 for coord in coords):
            raise BboxCoordinatesOutOfRangeError(coords)
        if not (coords[0] < coords[2] and coords[1] < coords[3]):
            raise BboxInvalidPointsOrderError(coords)
        return coords

    @staticmethod
    def check_point(point: object) -> Point:
        """Validate normalized point coordinates."""
        coords = _Validation.coerce_float_list(point, field_name="coord")
        if len(coords) != POINT_NUM_ELEMENTS:
            raise PointInvalidLengthError(len(coords), POINT_NUM_ELEMENTS)
        if not all(0 <= coord <= 1 for coord in coords):
            raise PointCoordinatesOutOfRangeError(coords)
        return coords

    @staticmethod
    def image(image: object) -> ImageSchema:
        """Validate image dimensions, mode, and size bounds."""
        if not isinstance(image, Image.Image):
            msg = "image must be a PIL Image."
            raise TypeError(msg)
        if image.width <= 0 or image.height <= 0:
            raise ImageDimensionError(image.width, image.height)
        if image.mode not in ALLOWED_IMAGE_MODES:
            raise ImageModeError(image.mode, ALLOWED_IMAGE_MODES)
        if image.width < MIN_IMAGE_DIMENSION or image.height < MIN_IMAGE_DIMENSION:
            raise ImageTooSmallError(image.width, image.height, MIN_IMAGE_DIMENSION)
        if image.width > MAX_IMAGE_DIMENSION or image.height > MAX_IMAGE_DIMENSION:
            raise ImageTooLargeError(image.width, image.height, MAX_IMAGE_DIMENSION)
        return image

    @staticmethod
    def video_path(path: object) -> str:
        """Validate that a local video path exists."""
        if not isinstance(path, str):
            msg = "path must be a string."
            raise TypeError(msg)
        if not Path(path).is_file():
            raise VideoFileNotFoundError(path)
        return path

    @staticmethod
    def video_url(url: object) -> str:
        """Validate that a video URL has a scheme and network location."""
        if not isinstance(url, str):
            msg = "url must be a string."
            raise TypeError(msg)
        try:
            result = urlparse(url)
        except ValueError as exc:
            raise VideoUrlInvalidError(url) from exc

        if not all([result.scheme, result.netloc]):
            raise VideoUrlInvalidError(url)
        return url

    @staticmethod
    def label(label: object) -> str:
        """Validate a visual element label."""
        if not isinstance(label, str):
            msg = "label must be a string."
            raise TypeError(msg)
        return label

    @staticmethod
    def text(value: object, *, field_name: str) -> str:
        """Validate a public text field."""
        if not isinstance(value, str):
            msg = f"{field_name} must be a string."
            raise TypeError(msg)
        return value

    @staticmethod
    def mask(mask: object) -> list[list[bool]]:
        """Validate a binary mask represented as nested boolean lists."""
        if not isinstance(mask, Sequence) or isinstance(mask, str | bytes):
            msg = "coord must be a sequence of boolean rows."
            raise TypeError(msg)

        rows: list[list[bool]] = []
        expected_width: int | None = None
        for row in mask:
            if not isinstance(row, Sequence) or isinstance(row, str | bytes):
                msg = "coord must contain only boolean rows."
                raise TypeError(msg)
            values = list(row)
            if not all(isinstance(value, bool) for value in values):
                msg = "coord mask values must be booleans."
                raise TypeError(msg)
            if expected_width is None:
                expected_width = len(values)
            elif len(values) != expected_width:
                msg = "coord mask rows must all have the same length."
                raise ValueError(msg)
            rows.append(values)
        return rows

    @staticmethod
    def elements(elements: object) -> Iterable[AnnotatableElement]:
        """Validate the public element iterable shape without consuming it."""
        if isinstance(elements, str | bytes) or not isinstance(elements, Iterable):
            msg = "elements must be an iterable of annotatable elements."
            raise TypeError(msg)
        return elements


# ================================================================================
# Media DTOs
# ================================================================================


@dataclass(frozen=True, slots=True)
class VideoSchema:
    """A validated path to a local video file."""

    path: str
    fps: int = 1
    start_offset: int | None = None
    end_offset: int | None = None

    def __post_init__(self) -> None:
        """Validate the video path after construction."""
        object.__setattr__(self, "path", _Validation.video_path(self.path))


@dataclass(frozen=True, slots=True)
class VideoUrlSchema:
    """A validated URL to a video file."""

    url: str
    fps: int = 1
    start_offset: int | None = None
    end_offset: int | None = None

    def __post_init__(self) -> None:
        """Validate the video URL after construction."""
        object.__setattr__(self, "url", _Validation.video_url(self.url))


# ================================================================================
# Annotation Element DTOs
# ================================================================================


@dataclass(frozen=True, slots=True)
class PageElement:
    """Describe a positioned element extracted from a document page."""

    coord: BoundingBox
    content: str

    def __post_init__(self) -> None:
        """Validate and copy the page element fields."""
        object.__setattr__(self, "coord", _Validation.check_bbox(self.coord))
        object.__setattr__(
            self,
            "content",
            _Validation.text(self.content, field_name="content"),
        )


@dataclass(frozen=True, slots=True)
class VisualElement:
    """Base model for a detected visual entity."""

    label: str

    def __post_init__(self) -> None:
        """Validate the shared visual element fields."""
        object.__setattr__(self, "label", _Validation.label(self.label))


@dataclass(frozen=True, slots=True)
class VisualBox(VisualElement):
    """Visual element defined by a rectangular bounding box."""

    coord: BoundingBox

    def __post_init__(self) -> None:
        """Validate and copy the box coordinates."""
        VisualElement.__post_init__(self)
        object.__setattr__(self, "coord", _Validation.check_bbox(self.coord))


@dataclass(frozen=True, slots=True)
class VisualPoint(VisualElement):
    """Visual element defined by a single reference point."""

    coord: Point

    def __post_init__(self) -> None:
        """Validate and copy the point coordinates."""
        VisualElement.__post_init__(self)
        object.__setattr__(self, "coord", _Validation.check_point(self.coord))


@dataclass(frozen=True, slots=True)
class VisualMask(VisualElement):
    """Visual element defined by a binary segmentation mask."""

    coord: list[list[bool]]

    def __post_init__(self) -> None:
        """Validate and copy the binary mask."""
        VisualElement.__post_init__(self)
        object.__setattr__(self, "coord", _Validation.mask(self.coord))


type AnnotatableElement = PageElement | VisualBox | VisualMask | VisualPoint


@dataclass(frozen=True, slots=True)
class AnnotationRequest:
    """A caller request to annotate an image with visual elements."""

    image: ImageSchema
    elements: Iterable[AnnotatableElement]

    def __post_init__(self) -> None:
        """Validate public request fields."""
        object.__setattr__(self, "image", _Validation.image(self.image))
        object.__setattr__(self, "elements", _Validation.elements(self.elements))


@dataclass(slots=True)
class AnnotationResponse:
    """Standardized response from the visual annotation pipeline."""

    response_data: ImageSchema
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate and copy public response fields."""
        self.response_data = _Validation.image(self.response_data)
        self.metadata = dict(self.metadata)

    @property
    def element_count(self) -> int:
        """Return the number of elements processed for this response."""
        value = self.metadata.get("element_count", 0)
        if isinstance(value, bool) or not isinstance(value, int):
            msg = "metadata element_count must be an integer."
            raise TypeError(msg)
        if value < 0:
            msg = "metadata element_count must be non-negative."
            raise ValueError(msg)
        return value
