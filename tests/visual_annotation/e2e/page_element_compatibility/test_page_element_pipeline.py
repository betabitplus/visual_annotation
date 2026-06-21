# %%
"""Visual annotation page element compatibility scenario.

Why:
    Verifies that page elements from screenshot/quote-capture workflows still
    route through public annotation without requiring private imports.

Covers:
    Area: page element compatibility
    Behavior: page element boxes without labels
    Interface: top-level `visual_annotation.annotate`

Checks:
    If page elements are annotated, then the response reports the element count.
    If page elements are annotated, then the output image keeps the input size.
    If page elements are annotated, then the output image differs from the input.

Examples:
    Run manually:
        uv run python -m \
            tests.visual_annotation.e2e.page_element_compatibility.test_page_element_pipeline

    Run as test:
        pytest \
            tests/visual_annotation/e2e/page_element_compatibility/test_page_element_pipeline.py
"""

from __future__ import annotations

import pytest
from py_lib_tooling import console, image_changed, save_test_output_image

from tests.visual_annotation.support.builders import (
    load_test_image,
    make_page_elements,
    response_evidence,
    test_image_path as fixture_image_path,
)
from visual_annotation import AnnotationResponse, annotate

pytestmark = [
    pytest.mark.e2e_contract,
    pytest.mark.hermetic,
]


# =============================================================================
# Scenario
# =============================================================================

_EXPECTED_ELEMENT_COUNT = 2


# =============================================================================
# Helpers
# =============================================================================


def format_result_for_demo(response: AnnotationResponse) -> dict[str, object]:
    """Return readable public evidence for manual runs."""
    return response_evidence(response)


# =============================================================================
# Pipeline
# =============================================================================


def run_pipeline() -> tuple[AnnotationResponse, bool]:
    """Run the public page element compatibility flow."""
    image = load_test_image()
    response = annotate(image, make_page_elements())
    return response, image_changed(image, response.response_data)


# =============================================================================
# Assertions
# =============================================================================


def assert_pipeline_response(response: AnnotationResponse, changed: bool) -> None:
    """Assert the public page element annotation response."""
    assert response.metadata["element_count"] == _EXPECTED_ELEMENT_COUNT
    assert response.response_data.size == load_test_image().size
    assert changed


# =============================================================================
# Tests
# =============================================================================


def test_page_element_compatibility_pipeline() -> None:
    """Verify page elements remain annotatable through the public API."""
    response, changed = run_pipeline()
    assert_pipeline_response(response, changed)


# =============================================================================
# Demo (Manual Execution)
# =============================================================================


def main() -> None:
    """Run the page element compatibility scenario as a manual demo."""
    console.demo_intro(__doc__)
    console.demo_step(
        "Scenario",
        "Annotating the shared image fixture with page-element boxes.",
        details=(f"image: {fixture_image_path().name}",),
    )

    response, changed = run_pipeline()
    assert_pipeline_response(response, changed)
    console.demo_step("Observed Response", "The public response matched the contract.")
    console.print(format_result_for_demo(response))
    output_path = save_test_output_image(
        response.response_data,
        "page_element_compatibility.png",
        module_name="visual_annotation",
    )
    console.demo_step(
        "Annotated Result",
        "Saved the annotated image for visual review.",
        details=(f"output: {output_path}",),
    )
    console.display_image_if_available(output_path)
    console.demo_outcome("The annotated image changed while preserving size.")


if __name__ == "__main__":
    main()

# %%
