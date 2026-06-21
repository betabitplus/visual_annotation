"""Package-specific pytest setup for visual annotation."""

from __future__ import annotations

from collections.abc import Generator

import pytest

from visual_annotation import AnnotatorConfig, install_config


@pytest.fixture(autouse=True)
def reset_installed_config_after_test() -> Generator[None]:
    """Restore default config after each test for process isolation."""
    yield
    install_config(AnnotatorConfig())
