"""Private implementation root for visual annotation.

Why:
    Provides narrow private-root entrypoints used by `_api` facades so facade
    modules do not import deep implementation modules.
"""

from __future__ import annotations

from visual_annotation._internal.config import (
    AnnotatorConfig as AnnotatorConfig,
    get_config as get_config,
    install_config as install_config,
)
from visual_annotation._internal.service import (
    annotate_request as annotate_request,
    clear_runtime_caches as clear_runtime_caches,
)
