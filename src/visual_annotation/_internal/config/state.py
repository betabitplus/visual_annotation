"""Runtime config snapshot state.

Why:
    Keeps process-wide config construction and install/read helpers inside the
    private config implementation.
"""

from __future__ import annotations

from threading import RLock

from py_lib_runtime import get_logger

from visual_annotation._internal.config.assembly import build_default_config
from visual_annotation._internal.config.models import AnnotatorConfig
from visual_annotation._internal.config.validation import validate_config

_installed_config: AnnotatorConfig = build_default_config()
_config_lock = RLock()
logger = get_logger(__name__)


def get_config(config: AnnotatorConfig | None = None) -> AnnotatorConfig:
    """Return a validated runtime configuration snapshot."""
    if config is not None:
        return config
    with _config_lock:
        return _installed_config


def install_config(config: object) -> AnnotatorConfig:
    """Install a validated runtime configuration snapshot."""
    if not isinstance(config, AnnotatorConfig):
        msg = "install_config() expects an AnnotatorConfig instance."
        raise TypeError(msg)

    validate_config(config)
    global _installed_config  # noqa: PLW0603
    with _config_lock:
        _installed_config = config

    _clear_runtime_config_caches()
    logger.info(
        "Configuration installed",
        event_type="visual_annotation.config.runtime.installed",
        box_thickness=config.box_thickness,
        point_radius=config.point_radius,
    )
    return config


def _clear_runtime_config_caches() -> None:
    """Clear runtime objects that captured the previous config snapshot."""
    from visual_annotation._internal.service import clear_runtime_caches

    clear_runtime_caches()
