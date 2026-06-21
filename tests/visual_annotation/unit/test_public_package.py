"""Public package boundary unit tests.

Why:
    Protects supported top-level imports, config helpers, public errors, and
    package version metadata.
"""

from __future__ import annotations

import visual_annotation
from visual_annotation import (
    AnnotatorConfig,
    InvalidConfigValueError,
    VisualAnnotationError,
)

# =============================================================================
# Tests
# =============================================================================


def test_public_exports_resolve() -> None:
    """All supported public names are exported by the top-level package."""
    for name in visual_annotation.__all__:
        assert hasattr(visual_annotation, name)


def test_public_exception_is_package_specific() -> None:
    """The package exposes one public exception base."""
    assert issubclass(VisualAnnotationError, Exception)


def test_public_config_exports_resolve() -> None:
    """The package exposes the shared config lifecycle."""
    installed = visual_annotation.install_config(AnnotatorConfig())

    assert visual_annotation.get_config().__class__ is AnnotatorConfig
    assert installed.__class__ is AnnotatorConfig


def test_invalid_config_error_is_public() -> None:
    """The package exposes a config-specific public error."""
    error = InvalidConfigValueError(
        field="field",
        value={"secret": "redacted"},
        reason="bad",
    )

    assert isinstance(error, VisualAnnotationError)
    assert "Invalid value for config field" in str(error)


def test_version_is_available() -> None:
    """The package exposes distribution metadata."""
    assert visual_annotation.__version__
