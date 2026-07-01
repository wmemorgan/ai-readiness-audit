"""Optional LLM narration — a documented, BYO-key product feature that never scores.

Narration is disabled by default. When enabled, a provider consumes the *finished* report
and returns prose; it receives no answers and cannot influence a band. The modules here
import only the report model — never the scoring core — so the boundary is structural, not
merely a convention.
"""

from __future__ import annotations

from ...application.ports import NarrationProvider
from ...config import Settings
from .mock import MockNarrationProvider


def build_narration_provider(settings: Settings) -> NarrationProvider | None:
    """Return a narration provider when enabled, else ``None`` (the default).

    The default build wires the deterministic mock provider, which needs no API key. A hosted
    deployment may substitute a Claude or OpenAI-compatible provider (see the sibling modules).
    """
    if not settings.narration_enabled:
        return None
    return MockNarrationProvider()
