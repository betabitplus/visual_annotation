"""Public media helper facades.

Why:
    Keeps caller-facing media helper functions out of declaration-only public
    type modules.
"""

from __future__ import annotations

# ================================================================================
# Public API
# ================================================================================


def format_video_offset(seconds: int) -> str:
    """Format seconds into the Gemini-compatible offset string."""
    return f"{seconds}s"
