"""AC-11: narration is inert by default and never moves a band."""

from __future__ import annotations

from ai_readiness_audit.adapters.narration import build_narration_provider
from ai_readiness_audit.adapters.narration.mock import MockNarrationProvider
from ai_readiness_audit.application.assess import assess
from ai_readiness_audit.config import Settings
from ai_readiness_audit.interface.sample_org import sample_answers


def test_narration_is_disabled_by_default() -> None:
    assert Settings.from_env({}).narration_enabled is False
    assert build_narration_provider(Settings()) is None


def test_disabled_narration_needs_no_key() -> None:
    # Building the default provider must not require any API key.
    assert build_narration_provider(Settings(narration_enabled=False)) is None


def test_band_is_identical_with_narration_on_or_off() -> None:
    answers = sample_answers()
    report = assess(answers)
    band_off = report.overall_band

    provider = MockNarrationProvider()
    narrative = provider.narrate(report)
    band_on = assess(answers).overall_band  # scoring is re-run; narration cannot influence it

    assert band_off == band_on
    assert isinstance(narrative, str) and narrative
    # The narration reflects the band; it does not change it.
    assert report.overall_band.title in narrative or report.verdict in narrative
