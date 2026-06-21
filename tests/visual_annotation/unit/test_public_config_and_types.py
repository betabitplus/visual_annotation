"""Public config and DTO contract tests."""

from __future__ import annotations

from pathlib import Path

import pytest
import supervision as sv
from PIL import Image

from tests.visual_annotation.support.builders import make_image
from visual_annotation import (
    AnnotationRequest,
    AnnotationResponse,
    AnnotatorConfig,
    BboxCoordinatesOutOfRangeError,
    BboxInvalidLengthError,
    BboxInvalidPointsOrderError,
    ImageModeError,
    ImageTooLargeError,
    ImageTooSmallError,
    InvalidConfigValueError,
    PageElement,
    PointCoordinatesOutOfRangeError,
    PointInvalidLengthError,
    VideoFileNotFoundError,
    VideoSchema,
    VideoUrlInvalidError,
    VideoUrlSchema,
    VisualBox,
    VisualPoint,
    get_config,
    install_config,
)
from visual_annotation._internal.service import (
    get_default_visual_annotation_service,
)

# =============================================================================
# Tests
# =============================================================================


def test_config_normalizes_color_names() -> None:
    """Verify public config converts string color names to supervision colors."""
    config = AnnotatorConfig(annotation_color="red", label_color="white")

    assert config.annotation_color == sv.Color.RED
    assert config.label_color == sv.Color.WHITE


def test_config_rejects_invalid_color_name() -> None:
    """Verify config color validation preserves a package-specific error."""
    with pytest.raises(InvalidConfigValueError) as exc_info:
        AnnotatorConfig(annotation_color="not-a-color")

    assert exc_info.value.field == "annotation_color"


def test_config_rejects_invalid_numeric_ranges() -> None:
    """Verify public config checks numeric ranges at construction."""
    with pytest.raises(ValueError, match="box_thickness"):
        AnnotatorConfig(box_thickness=0)
    with pytest.raises(ValueError, match="label_text_scale"):
        AnnotatorConfig(label_text_scale=0.0)
    with pytest.raises(ValueError, match="label_text_padding"):
        AnnotatorConfig(label_text_padding=-1)


def test_config_rejects_boolean_numeric_values() -> None:
    """Verify bools do not pass as numeric config values."""
    with pytest.raises(TypeError, match="box_thickness"):
        AnnotatorConfig(box_thickness=True)
    with pytest.raises(TypeError, match="label_text_scale"):
        AnnotatorConfig(label_text_scale=True)
    with pytest.raises(TypeError, match="label_text_padding"):
        AnnotatorConfig(label_text_padding=False)


def test_install_config_replaces_public_snapshot() -> None:
    """Installed config snapshots are returned by the public config reader."""
    config = AnnotatorConfig(box_thickness=5)

    installed = install_config(config)

    assert installed is config
    assert get_config() is config


def test_install_config_rejects_unknown_snapshot_type() -> None:
    """Only validated visual annotation configs can be installed."""
    with pytest.raises(TypeError, match="AnnotatorConfig"):
        install_config(object())


def test_install_config_invalidates_default_service_cache() -> None:
    """Installing config refreshes runtime objects built from old snapshots."""
    old_service = get_default_visual_annotation_service()
    config = AnnotatorConfig(box_thickness=7)

    install_config(config)
    new_service = get_default_visual_annotation_service()

    assert new_service is not old_service
    assert new_service.config is config


def test_bbox_contract_rejects_invalid_shapes_and_ranges() -> None:
    """Verify public box DTOs preserve coordinate validation."""
    with pytest.raises(BboxInvalidLengthError):
        VisualBox(label="bad", coord=[0.1, 0.2, 0.3])

    with pytest.raises(BboxCoordinatesOutOfRangeError):
        VisualBox(label="bad", coord=[-0.1, 0.2, 0.3, 0.4])

    with pytest.raises(BboxInvalidPointsOrderError):
        VisualBox(label="bad", coord=[0.5, 0.2, 0.5, 0.4])


def test_point_contract_rejects_invalid_shapes_and_ranges() -> None:
    """Verify public point DTOs preserve coordinate validation."""
    with pytest.raises(PointInvalidLengthError):
        VisualPoint(label="bad", coord=[0.1])

    with pytest.raises(PointCoordinatesOutOfRangeError):
        VisualPoint(label="bad", coord=[0.2, 1.2])


def test_page_element_uses_bbox_contract() -> None:
    """Verify page elements reuse the public bounding-box contract."""
    element = PageElement(coord=[0.1, 0.2, 0.4, 0.6], content="quote")

    assert element.coord == [0.1, 0.2, 0.4, 0.6]
    assert element.content == "quote"


def test_image_contract_rejects_unsupported_modes_and_sizes() -> None:
    """Verify public image validation preserves feature-branch limits."""
    with pytest.raises(ImageModeError):
        AnnotationRequest(image=Image.new("1", (100, 100)), elements=[])

    with pytest.raises(ImageTooSmallError):
        AnnotationRequest(image=make_image(width=9, height=100), elements=[])

    too_large = make_image()
    too_large._size = (16_385, 100)
    with pytest.raises(ImageTooLargeError):
        AnnotationRequest(image=too_large, elements=[])


def test_video_contracts_validate_path_and_url(tmp_path: Path) -> None:
    """Verify public video helper DTOs preserve validation behavior."""
    video_path = tmp_path / "sample.mp4"
    video_path.write_bytes(b"not a real video")

    assert VideoSchema(path=str(video_path)).path == str(video_path)
    assert VideoUrlSchema(url="https://example.com/video.mp4").url.endswith(".mp4")

    with pytest.raises(VideoFileNotFoundError):
        VideoSchema(path=str(tmp_path / "missing.mp4"))

    with pytest.raises(VideoUrlInvalidError):
        VideoUrlSchema(url="not-a-url")


def test_annotation_response_exposes_element_count() -> None:
    """Response helper exposes processed element count without metadata access."""
    response = AnnotationResponse(
        response_data=make_image(),
        metadata={"element_count": 2},
    )

    assert response.element_count == 2


def test_annotation_response_defaults_element_count_to_zero() -> None:
    """Responses without service metadata report zero processed elements."""
    response = AnnotationResponse(response_data=make_image())

    assert response.element_count == 0


def test_annotation_response_rejects_invalid_element_count() -> None:
    """Response helper rejects invalid service metadata."""
    response = AnnotationResponse(
        response_data=make_image(),
        metadata={"element_count": "two"},
    )

    with pytest.raises(TypeError, match="element_count"):
        _ = response.element_count


def test_annotation_response_rejects_negative_element_count() -> None:
    """Response helper rejects impossible negative element counts."""
    response = AnnotationResponse(
        response_data=make_image(),
        metadata={"element_count": -1},
    )

    with pytest.raises(ValueError, match="non-negative"):
        _ = response.element_count
