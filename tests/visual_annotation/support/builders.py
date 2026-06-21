"""Reusable visual annotation test builders.

Why:
    Keeps shared public DTO and image setup in one package-specific test helper
    instead of duplicating it across e2e, unit, and integration tests.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import supervision as sv
from PIL import Image, ImageDraw
from py_lib_tooling import get_test_data_path

from visual_annotation import (
    AnnotationRequest,
    AnnotationResponse,
    AnnotatorConfig,
    PageElement,
    VisualBox,
    VisualMask,
    VisualPoint,
)


def test_image_path() -> Path:
    """Return the shared visual annotation image fixture path."""
    return get_test_data_path("visual_annotation") / "test_image.png"


def load_test_image() -> Image.Image:
    """Load the shared RGB image fixture."""
    path = test_image_path()
    if not path.exists():
        msg = f"Test image not found: {path}"
        raise FileNotFoundError(msg)
    return Image.open(path).convert("RGB")


def make_image(width: int = 100, height: int = 100) -> Image.Image:
    """Return a plain RGB test image."""
    return Image.new("RGB", (width, height), color="white")


def make_annotator_config(
    *,
    annotation_color: str | sv.Color = sv.Color.RED,
    label_color: str | sv.Color = sv.Color.WHITE,
    box_thickness: int = 2,
    point_radius: int = 5,
    label_text_scale: float = 0.5,
    label_text_padding: int = 5,
    label_text_thickness: int = 1,
) -> AnnotatorConfig:
    """Return a validated test config."""
    return AnnotatorConfig(
        annotation_color=annotation_color,
        label_color=label_color,
        box_thickness=box_thickness,
        point_radius=point_radius,
        label_text_scale=label_text_scale,
        label_text_padding=label_text_padding,
        label_text_thickness=label_text_thickness,
    )


def make_visual_boxes() -> list[VisualBox]:
    """Return deterministic box elements for public scenarios."""
    return [
        VisualBox(label="car", coord=[0.19, 0.65, 0.34, 0.83]),
        VisualBox(label="truck", coord=[0.68, 0.43, 0.82, 0.69]),
    ]


def make_visual_points() -> list[VisualPoint]:
    """Return deterministic point elements for public scenarios."""
    return [
        VisualPoint(label="car", coord=[0.26, 0.74]),
        VisualPoint(label="truck", coord=[0.75, 0.56]),
    ]


def make_page_elements() -> list[PageElement]:
    """Return deterministic page elements for compatibility scenarios."""
    return [
        PageElement(coord=[0.19, 0.65, 0.34, 0.83], content="left lane vehicle"),
        PageElement(coord=[0.68, 0.43, 0.82, 0.69], content="right lane vehicle"),
    ]


def make_visual_masks(image: Image.Image | None = None) -> list[VisualMask]:
    """Return deterministic vehicle-shaped mask elements."""
    source_image = image or make_image()
    boxes = make_visual_boxes()
    polygons = [
        [
            (0.19, 0.77),
            (0.19, 0.69),
            (0.22, 0.65),
            (0.30, 0.65),
            (0.33, 0.70),
            (0.33, 0.80),
            (0.25, 0.80),
        ],
        [
            (0.68, 0.64),
            (0.68, 0.48),
            (0.72, 0.43),
            (0.79, 0.44),
            (0.82, 0.52),
            (0.82, 0.67),
            (0.72, 0.67),
        ],
    ]

    return [
        VisualMask(
            label=box.label,
            coord=_normalized_polygon_mask(
                source_image,
                polygons[index],
            ).tolist(),
        )
        for index, box in enumerate(boxes)
    ]


def _normalized_polygon_mask(
    image: Image.Image,
    points: list[tuple[float, float]],
) -> np.ndarray:
    """Return a boolean mask from normalized polygon points."""
    mask = Image.new("1", image.size, 0)
    pixel_points = [
        (round(x * image.width), round(y * image.height)) for x, y in points
    ]
    ImageDraw.Draw(mask).polygon(pixel_points, fill=1)
    return np.asarray(mask, dtype=bool)


def make_annotation_request(
    *,
    image: Image.Image | None = None,
    elements: list[PageElement | VisualBox | VisualMask | VisualPoint] | None = None,
) -> AnnotationRequest:
    """Return a public annotation request for integration tests."""
    return AnnotationRequest(
        image=image or make_image(),
        elements=elements if elements is not None else make_page_elements(),
    )


def response_evidence(response: AnnotationResponse) -> dict[str, object]:
    """Return public response evidence shared by e2e assertions and demos."""
    return {
        "element_count": response.metadata["element_count"],
        "output_image_size": list(response.response_data.size),
        "output_image_mode": response.response_data.mode,
    }
