"""Claude narration provider — a documented, bring-your-own-key product feature.

The provider is optional and disabled by default. The SDK is imported lazily so the engine
has no hard dependency on it. The provider consumes a finished report and returns prose; it
never receives answers and cannot influence a band.
"""

from __future__ import annotations

from ...domain.models import ReadinessReport
from ._prompt import narration_prompt

DEFAULT_MODEL = "claude-opus-4-8"


class ClaudeNarrationProvider:
    """Narrate a finished report via the Claude API (BYO key)."""

    def __init__(self, api_key: str, model: str = DEFAULT_MODEL) -> None:
        if not api_key:
            raise ValueError("an API key is required to enable Claude narration")
        self._api_key = api_key
        self._model = model

    def narrate(self, report: ReadinessReport) -> str:
        try:
            import anthropic  # imported lazily; optional dependency
        except ImportError as exc:  # pragma: no cover - optional path
            raise RuntimeError(
                "the 'anthropic' package is required for Claude narration"
            ) from exc

        client = anthropic.Anthropic(api_key=self._api_key)
        message = client.messages.create(
            model=self._model,
            max_tokens=600,
            messages=[{"role": "user", "content": narration_prompt(report)}],
        )
        return "".join(block.text for block in message.content if block.type == "text")
