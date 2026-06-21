"""Public config re-exports.

Why:
    Keeps config names behind the `_api` facade while `_internal` owns config
    models, validation, runtime default assembly, and snapshot state.
"""

from __future__ import annotations

# pyright: reportUnusedImport=false
from visual_annotation._internal import (  # noqa: F401
    AnnotatorConfig,
    get_config,
    install_config,
)
