# %%
"""Workbench scenario: page element compatibility dependency seam.

Why:
    Confirms that screenshot-style page boxes can be rendered as unlabeled boxes
    without importing the shipped package.

Covers:
    Area: page element compatibility
    Behavior: page element boxes without label detections
    Interface: supervision BoxAnnotator

Checks:
    If page boxes are scaled to pixels, then supervision receives concrete
    `xyxy` coordinates.
    If the annotator runs, then no label payload is required.

Examples:
    Run manually:
        uv run python -m workbench.visual_annotation.page_element_compatibility
        uv run py-lib-reproduce-running-loop \
            workbench.visual_annotation.page_element_compatibility
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
    "page_element_compatibility.png",
    module_name="visual_annotation",
)
_PAGE_BOXES = np.array([[0.19, 0.65, 0.34, 0.83], [0.68, 0.43, 0.82, 0.69]])


# =============================================================================
# Helpers
# =============================================================================

# No local helpers for this scenario.


# =============================================================================
# Pipeline
# =============================================================================


def run_pipeline() -> dict[str, object]:
    """Run the real page box drawing dependency flow."""
    image = Image.open(_INPUT_IMAGE).convert("RGB")
    scene_rgb = np.array(image)
    scene_bgr = cv2.cvtColor(scene_rgb, cv2.COLOR_RGB2BGR)
    scale = np.array([image.width, image.height, image.width, image.height])
    detections = sv.Detections(xyxy=_PAGE_BOXES * scale)

    box_annotator = sv.BoxAnnotator(
        color=sv.Color.RED,
        thickness=2,
        color_lookup=sv.ColorLookup.INDEX,
    )
    annotated = box_annotator.annotate(scene=scene_bgr.copy(), detections=detections)
    output = Image.fromarray(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
    _OUTPUT_IMAGE.parent.mkdir(parents=True, exist_ok=True)
    output.save(_OUTPUT_IMAGE)

    return {
        "input_size": list(image.size),
        "label_payload": "class_name" in detections.data,
        "output_image": str(_OUTPUT_IMAGE.relative_to(get_repo_root())),
        "output_size": list(output.size),
        "page_box_count": len(detections),
    }


# =============================================================================
# Demo (Manual Execution)
# =============================================================================


def main() -> None:
    """Run the workbench script as a narrative manual demo."""
    console.demo_intro(__doc__)
    console.demo_step("Scenario", "Drawing two unlabeled page boxes with supervision.")
    evidence = run_pipeline()
    console.demo_step(
        "Observed Drawing", "The dependency seam returned image evidence."
    )
    console.print(evidence)
    console.display_image_if_available(_OUTPUT_IMAGE)
    console.demo_outcome("Page element drawing works without label payloads.")


if __name__ == "__main__":
    main()


# =============================================================================
# Expected Output
# =============================================================================
EXPECTED_OUTPUT = """
Real run:
{
  "input_size": [515, 333],
  "label_payload": false,
  "output_image": "workbench/.outputs/visual_annotation/page_element_compatibility.png",
  "output_size": [515, 333],
  "page_box_count": 2
}
""".strip()
