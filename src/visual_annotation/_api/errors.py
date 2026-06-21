"""Public exceptions for visual annotation.

Why:
    Keeps the caller-facing exception taxonomy stable while private runtime
    modules translate lower-level failures at explicit boundaries.

Notes:
    Direct caller-contract failures may still raise built-in `TypeError` or
    `ValueError`. The validation errors here inherit from `ValueError` so
    callers can catch package errors when they need domain-specific handling.
"""

from __future__ import annotations


class VisualAnnotationError(Exception):
    """Base class for package-specific public errors."""


class AnnotatorError(VisualAnnotationError):
    """Raised when visual annotation fails at runtime."""

    def __init__(
        self,
        message: str = "An error occurred during annotation.",
        *,
        cause: Exception | None = None,
        **context: object,
    ) -> None:
        """Store caller-safe runtime failure context."""
        self.context = context
        super().__init__(message)
        if cause is not None:
            self.__cause__ = cause


class AnnotatorConfigError(AnnotatorError):
    """Raised when annotator configuration cannot be used."""


class HandlerMappingError(AnnotatorError):
    """Raised when an annotation handler cannot be mapped correctly."""

    def __init__(self, *, handler_name: str, reason: str) -> None:
        """Store the failed handler name and mapping reason."""
        self.handler_name = handler_name
        self.reason = reason
        super().__init__(f"Failed to map handler '{handler_name}': {reason}")


class InvalidConfigValueError(AnnotatorConfigError, ValueError):
    """Raised when a config value is outside the supported domain."""

    def __init__(self, *, field: str, value: object, reason: str) -> None:
        """Store the invalid field, value, and caller-facing reason."""
        self.field = field
        self.value = value
        self.reason = reason
        super().__init__(
            f"Invalid value for config field '{field}': Received '{value}'. "
            f"Reason: {reason}"
        )


class PointValidationError(AnnotatorError, ValueError):
    """Base class for point validation errors."""


class PointInvalidLengthError(PointValidationError):
    """Raised when a point has the wrong number of coordinates."""

    def __init__(self, num_elements: int, expected: int) -> None:
        """Store the received and expected coordinate counts."""
        self.num_elements = num_elements
        self.expected_elements = expected
        super().__init__(
            f"Point must have {expected} elements [x, y], got {num_elements}.",
        )


class PointCoordinatesOutOfRangeError(PointValidationError):
    """Raised when point coordinates are outside the normalized range."""

    def __init__(self, point: list[float]) -> None:
        """Store the invalid point."""
        self.point = point
        super().__init__(
            f"Point coordinates must be between 0 and 1, got {point}.",
        )


class BboxValidationError(AnnotatorError, ValueError):
    """Base class for bounding-box validation errors."""


class BboxInvalidLengthError(BboxValidationError):
    """Raised when a bounding box has the wrong number of coordinates."""

    def __init__(self, num_elements: int, expected: int) -> None:
        """Store the received and expected coordinate counts."""
        self.num_elements = num_elements
        self.expected_elements = expected
        super().__init__(f"Bbox must have {expected} elements, got {num_elements}.")


class BboxCoordinatesOutOfRangeError(BboxValidationError):
    """Raised when bounding-box coordinates are outside the normalized range."""

    def __init__(self, bbox: list[float]) -> None:
        """Store the invalid bounding box."""
        self.bbox = bbox
        super().__init__(f"Bbox coords must be in [0,1], got {bbox}.")


class BboxInvalidPointsOrderError(BboxValidationError):
    """Raised when bounding-box points are not in top-left/bottom-right order."""

    def __init__(self, bbox: list[float]) -> None:
        """Store the invalid bounding box."""
        self.bbox = bbox
        super().__init__(
            f"x0 must be less than x1 and y0 must be less than y1, but got {bbox}.",
        )


class ImageValidationError(AnnotatorError, ValueError):
    """Base class for image validation errors."""


class ImageDimensionError(ImageValidationError):
    """Raised when image dimensions are zero or negative."""

    def __init__(self, width: int, height: int) -> None:
        """Store the invalid dimensions."""
        self.width = width
        self.height = height
        super().__init__(
            f"Image must have positive dimensions, but got {width}x{height}.",
        )


class ImageTooSmallError(ImageValidationError):
    """Raised when an image is below the supported minimum dimensions."""

    def __init__(self, width: int, height: int, min_dim: int) -> None:
        """Store the actual and minimum dimensions."""
        self.width = width
        self.height = height
        self.min_dim = min_dim
        super().__init__(
            f"Image dimensions {width}x{height} are too small. "
            f"Minimum is {min_dim}x{min_dim}.",
        )


class ImageTooLargeError(ImageValidationError):
    """Raised when an image exceeds the supported maximum dimensions."""

    def __init__(self, width: int, height: int, max_dim: int) -> None:
        """Store the actual and maximum dimensions."""
        self.width = width
        self.height = height
        self.max_dim = max_dim
        super().__init__(
            f"Image dimensions {width}x{height} exceed maximum of {max_dim}x{max_dim}.",
        )


class ImageModeError(ImageValidationError):
    """Raised when an image mode is not supported for annotation."""

    def __init__(self, mode: str, allowed_modes: frozenset[str]) -> None:
        """Store the unsupported mode and allowed mode set."""
        self.mode = mode
        self.allowed_modes = allowed_modes
        super().__init__(
            f"Image mode '{mode}' is not supported. "
            f"Allowed modes: {sorted(allowed_modes)}.",
        )


class VideoValidationError(AnnotatorError, ValueError):
    """Base class for video validation errors."""


class VideoFileNotFoundError(VideoValidationError):
    """Raised when a local video file path does not exist."""

    def __init__(self, path: str) -> None:
        """Store the missing video path."""
        self.path = path
        super().__init__(f"Video file not found at path: {path}")


class VideoUrlInvalidError(VideoValidationError):
    """Raised when a video URL is malformed."""

    def __init__(self, url: str) -> None:
        """Store the invalid URL."""
        self.url = url
        super().__init__(f"Invalid video URL: {url}")
