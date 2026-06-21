"""Runtime configuration package.

Why:
    Owns validated immutable configuration snapshots for private annotation
    runtime instances.

What belongs here:
    Config dataclasses, default assembly, validation, and process-wide snapshot
    state.

What does not belong here:
    Public facade helpers, annotation handlers, or drawing orchestration.
"""

from visual_annotation._internal.config.assembly import (
    build_default_config as build_default_config,
)
from visual_annotation._internal.config.models import AnnotatorConfig as AnnotatorConfig
from visual_annotation._internal.config.state import (
    get_config as get_config,
    install_config as install_config,
)
from visual_annotation._internal.config.validation import (
    validate_config as validate_config,
)
