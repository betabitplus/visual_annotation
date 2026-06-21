# %%
"""Workbench scenario: mask annotation dependency seam.

Why:
    Confirms that the local supervision/OpenCV drawing stack can render masks
    on the shared image fixture without importing the shipped package.

Covers:
    Area: mask annotation
    Behavior: deterministic boolean masks converted to supervision detections
    Interface: supervision MaskAnnotator and LabelAnnotator

Checks:
    If deterministic masks are supplied, then supervision receives mask data.
    If the annotators run, then the returned image keeps the fixture size.

Examples:
    Run manually:
        uv run python -m workbench.visual_annotation.mask_annotation
        uv run py-lib-reproduce-running-loop \
            workbench.visual_annotation.mask_annotation
"""

from __future__ import annotations

import cv2
import numpy as np
import supervision as sv
from PIL import Image, ImageDraw
from py_lib_tooling import console, get_repo_root, get_workbench_output_path

# =============================================================================
# Scenario
# =============================================================================

_INPUT_IMAGE = (
    get_repo_root() / "tests" / "visual_annotation" / "data" / "test_image.png"
)
_OUTPUT_IMAGE = get_workbench_output_path(
    "mask_annotation.png",
    module_name="visual_annotation",
)
_BOXES = np.array([[0.19, 0.65, 0.34, 0.83], [0.68, 0.43, 0.82, 0.69]])
_LABELS = ["car", "truck"]


# =============================================================================
# Helpers
# =============================================================================


def _boxes_to_masks(*, image: Image.Image) -> np.ndarray:
    """Build deterministic vehicle-shaped boolean masks."""
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
    masks = [_normalized_polygon_mask(image, points) for points in polygons]
    return np.stack(masks, axis=0)


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


# =============================================================================
# Pipeline
# =============================================================================


def run_pipeline() -> dict[str, object]:
    """Run the real mask drawing dependency flow."""
    image = Image.open(_INPUT_IMAGE).convert("RGB")
    scene_rgb = np.array(image)
    scene_bgr = cv2.cvtColor(scene_rgb, cv2.COLOR_RGB2BGR)
    masks = _boxes_to_masks(image=image)
    bboxes = _BOXES * np.tile(image.size, 2)
    detections = sv.Detections(xyxy=bboxes, mask=masks)
    detections.data["class_name"] = _LABELS

    mask_annotator = sv.MaskAnnotator(
        color=sv.Color.RED,
        color_lookup=sv.ColorLookup.INDEX,
    )
    label_annotator = sv.LabelAnnotator(
        color=sv.Color.RED,
        text_color=sv.Color.WHITE,
        color_lookup=sv.ColorLookup.INDEX,
    )
    annotated = mask_annotator.annotate(scene=scene_bgr.copy(), detections=detections)
    annotated = label_annotator.annotate(scene=annotated, detections=detections)
    annotated_array = np.asarray(annotated, dtype=np.uint8)
    output = Image.fromarray(cv2.cvtColor(annotated_array, cv2.COLOR_BGR2RGB))
    _OUTPUT_IMAGE.parent.mkdir(parents=True, exist_ok=True)
    output.save(_OUTPUT_IMAGE)

    return {
        "input_size": list(image.size),
        "output_size": list(output.size),
        "output_image": str(_OUTPUT_IMAGE.relative_to(get_repo_root())),
        "mask_count": len(detections),
    }


# =============================================================================
# Demo (Manual Execution)
# =============================================================================


def main() -> None:
    """Run the workbench script as a narrative manual demo."""
    console.demo_intro(__doc__)
    console.demo_step("Scenario", "Drawing two labeled masks with supervision.")
    evidence = run_pipeline()
    console.demo_step(
        "Observed Drawing", "The dependency seam returned image evidence."
    )
    console.print(evidence)
    console.display_image_if_available(_OUTPUT_IMAGE)
    console.demo_outcome("Mask annotation dependencies can render the slice.")


if __name__ == "__main__":
    main()


# =============================================================================
# Expected Output
# =============================================================================
EXPECTED_OUTPUT = """
Real run:
{
  "input_size": [515, 333],
  "mask_count": 2,
  "output_image": "workbench/.outputs/visual_annotation/mask_annotation.png",
  "output_size": [515, 333]
}
""".strip()
