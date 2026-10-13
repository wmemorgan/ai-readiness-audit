"""Generic OpenAI-compatible narration provider — BYO key, community/unverified calibration.

Works against any OpenAI-compatible chat-completions endpoint. Optional and disabled by
default; the SDK is imported lazily. Calibration against non-Claude providers is community
/ unverified. Like every narration provider, it consumes a finished report and never scores.
"""

from __future__ import annotations

from ...domain.models import ReadinessReport
from ._prompt import narration_prompt


class OpenAICompatibleNarrationProvider:
    """Narrate a finished report via an OpenAI-compatible endpoint (BYO key)."""

    def __init__(self, api_key: str, model: str, base_url: str | None = None) -> None:
        if not api_key:
            raise ValueError("an API key is required to enable narration")
        self._api_key = api_key
        self._model = model
        self._base_url = base_url

    def narrate(self, report: ReadinessReport) -> str:
        try:
            from openai import OpenAI  # imported lazily; optional dependency
        except ImportError as exc:  # pragma: no cover - optional path
            raise RuntimeError(
                "the 'openai' package is required for OpenAI-compatible narration"
            ) from exc

        client = OpenAI(api_key=self._api_key, base_url=self._base_url)
        completion = client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": narration_prompt(report)}],
        )
        return completion.choices[0].message.content or ""
