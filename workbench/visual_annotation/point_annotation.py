# %%
"""Workbench scenario: point annotation dependency seam.

Why:
    Confirms that the local supervision/OpenCV drawing stack can render points
    on the shared image fixture without importing the shipped package.

Covers:
    Area: point annotation
    Behavior: normalized point coordinates scaled into image pixels
    Interface: supervision DotAnnotator and LabelAnnotator

Checks:
    If normalized points are scaled to pixels, then supervision receives
    concrete `xy` coordinates.
    If the annotators run, then the returned image keeps the fixture size.

Examples:
    Run manually:
        uv run python -m workbench.visual_annotation.point_annotation
        uv run py-lib-reproduce-running-loop \
            workbench.visual_annotation.point_annotation
"""

from __future__ import annotations

import cv2
import numpy as np
import supervision as sv
from PIL import Image
from py_lib_tooling import console, get_repo_root, get_workbench_output_path

# =============================================================================
# Scenario
# =============================================================================

_INPUT_IMAGE = (
    get_repo_root() / "tests" / "visual_annotation" / "data" / "test_image.png"
)
_OUTPUT_IMAGE = get_workbench_output_path(
    "point_annotation.png",
    module_name="visual_annotation",
)
_POINTS = np.array([[0.26, 0.74], [0.75, 0.56]])
_LABELS = ["car", "truck"]


# =============================================================================
# Helpers
# =============================================================================

# No local helpers for this scenario.


# =============================================================================
# Pipeline
# =============================================================================


def run_pipeline() -> dict[str, object]:
    """Run the real point drawing dependency flow."""
    image = Image.open(_INPUT_IMAGE).convert("RGB")
    scene_rgb = np.array(image)
    scene_bgr = cv2.cvtColor(scene_rgb, cv2.COLOR_RGB2BGR)
    xy = _POINTS * np.array([image.width, image.height])
    detections = sv.Detections(xyxy=np.hstack([xy, xy]))
    detections.xy = xy
    detections.data["class_name"] = _LABELS

    dot_annotator = sv.DotAnnotator(
        color=sv.Color.RED,
        radius=4,
        color_lookup=sv.ColorLookup.INDEX,
    )
    label_annotator = sv.LabelAnnotator(
        color=sv.Color.RED,
        text_color=sv.Color.WHITE,
        color_lookup=sv.ColorLookup.INDEX,
    )
    annotated = dot_annotator.annotate(scene=scene_bgr.copy(), detections=detections)
    annotated = label_annotator.annotate(scene=annotated, detections=detections)
    annotated_array = np.asarray(annotated, dtype=np.uint8)
    output = Image.fromarray(cv2.cvtColor(annotated_array, cv2.COLOR_BGR2RGB))
    _OUTPUT_IMAGE.parent.mkdir(parents=True, exist_ok=True)
    output.save(_OUTPUT_IMAGE)

    return {
        "input_size": list(image.size),
        "output_image": str(_OUTPUT_IMAGE.relative_to(get_repo_root())),
        "output_size": list(output.size),
        "point_count": len(detections),
    }


# =============================================================================
# Demo (Manual Execution)
# =============================================================================


def main() -> None:
    """Run the workbench script as a narrative manual demo."""
    console.demo_intro(__doc__)
    console.demo_step("Scenario", "Drawing two labeled points with supervision.")
    evidence = run_pipeline()
    console.demo_step(
        "Observed Drawing", "The dependency seam returned image evidence."
    )
    console.print(evidence)
    console.display_image_if_available(_OUTPUT_IMAGE)
    console.demo_outcome("Point annotation dependencies can render the slice.")


if __name__ == "__main__":
    main()


# =============================================================================
# Expected Output
# =============================================================================
EXPECTED_OUTPUT = """
Real run:
{
  "input_size": [515, 333],
  "output_image": "workbench/.outputs/visual_annotation/point_annotation.png",
  "output_size": [515, 333],
  "point_count": 2
}
""".strip()
