"""Private service orchestration for visual annotation.

Why:
    Keeps resolver, handler factory, and drawing runtime collaboration out of
    the public facade layer.
"""

from __future__ import annotations

from functools import cache

from py_lib_runtime import get_logger, log_operation_duration, preview_exception_message

from visual_annotation._api.errors import AnnotatorError
from visual_annotation._api.types import AnnotationRequest, AnnotationResponse
from visual_annotation._internal.annotator import Annotator
from visual_annotation._internal.config import AnnotatorConfig, get_config
from visual_annotation._internal.handlers.factory import AnnotationHandlerFactory
from visual_annotation._internal.resolver import AnnotationTaskResolver

_LOGGER = get_logger(__name__)


class VisualAnnotationService:
    """Owns one configured visual annotation runtime snapshot."""

    def __init__(
        self,
        config: AnnotatorConfig,
        *,
        resolver: AnnotationTaskResolver | None = None,
    ) -> None:
        """Build service collaborators for the supplied config snapshot."""
        self.config = config
        self.resolver = resolver or AnnotationTaskResolver()
        self._factory = AnnotationHandlerFactory(config)
        self._annotator = Annotator(
            handlers=self._factory.get_handlers(),
            label_annotator=self._factory.label_annotator,
        )

    def annotate(
        self,
        request: AnnotationRequest,
        *,
        correlation_id: str | None = None,
    ) -> AnnotationResponse:
        """Resolve and execute one annotation request."""
        element_count = 0
        log = _LOGGER.bind(
            operation="visual_annotation.annotate",
            correlation_id=correlation_id,
        )
        try:
            with log_operation_duration(
                log,
                event_type="visual_annotation.annotation.lifecycle.completed",
                message="Annotation completed",
            ):
                log.info(
                    "Annotation started",
                    event_type="visual_annotation.annotation.lifecycle.started",
                )
                task = self.resolver.resolve(request)
                element_count = len(task.elements)
                annotated_image = self._annotator.annotate(task.image, task.elements)
                return AnnotationResponse(
                    response_data=annotated_image,
                    metadata={"element_count": element_count},
                )
        except AnnotatorError:
            raise
        except Exception as exc:
            log.warning(
                "Annotation failed",
                event_type="visual_annotation.annotation.lifecycle.failed",
                error_type=type(exc).__name__,
                error_message=preview_exception_message(exc),
            )
            raise AnnotatorError(
                cause=exc,
                element_count=element_count,
            ) from exc


def annotate_request(
    request: AnnotationRequest,
    *,
    config: AnnotatorConfig | None = None,
    correlation_id: str | None = None,
) -> AnnotationResponse:
    """Run one public request through a configured service."""
    service = (
        get_default_visual_annotation_service()
        if config is None
        else VisualAnnotationService(config=config)
    )
    return service.annotate(request, correlation_id=correlation_id)


@cache
def get_default_visual_annotation_service() -> VisualAnnotationService:
    """Return the cached service for the installed config snapshot."""
    return VisualAnnotationService(config=get_config())


def clear_runtime_caches() -> None:
    """Clear runtime caches after config changes or tests."""
    get_default_visual_annotation_service.cache_clear()
