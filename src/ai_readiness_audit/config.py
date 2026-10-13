"""Runtime configuration — policy-neutral by design.

The engine makes no retention or processing promises and pins no provider. Narration is
disabled by default; enabling it and supplying a key is a deployment choice, not an engine
constant. This keeps the open-source engine free of operational coupling.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Feature flags resolved from the environment, with safe defaults."""

    narration_enabled: bool = False

    @classmethod
    def from_env(cls, env: dict[str, str] | None = None) -> Settings:
        source = os.environ if env is None else env
        return cls(
            narration_enabled=_as_bool(source.get("ARA_NARRATION_ENABLED", "false")),
        )


def _as_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}
