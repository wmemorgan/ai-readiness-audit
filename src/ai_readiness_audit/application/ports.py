"""Ports: the interfaces the outside world implements to plug into the core.

Adapters (report renderers, PDF writers, narration providers, delivery channels) depend on
these abstractions; the core never depends on a concrete adapter. This is the dependency
inversion that keeps the domain pure and the engine free of operational coupling.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable

from ..domain.models import Band, ReadinessReport


@runtime_checkable
class QuestionnaireInput(Protocol):
    """Source of a completed assessment: question id -> selected band."""

    def answers(self) -> Mapping[str, Band]: ...


@runtime_checkable
class ReportRenderer(Protocol):
    """Render a readiness report to a presentation string (e.g. HTML)."""

    def render(self, report: ReadinessReport) -> str: ...


@runtime_checkable
class PdfRenderer(Protocol):
    """Render a readiness report to PDF bytes."""

    def render(self, report: ReadinessReport) -> bytes: ...


@runtime_checkable
class NarrationProvider(Protocol):
    """Produce optional plain-language narration for a finished report.

    A narration provider *consumes* a completed report and returns prose. It cannot and must
    not influence scoring — it never receives raw answers, only the finished report.
    """

    def narrate(self, report: ReadinessReport) -> str: ...


@runtime_checkable
class DeliveryChannel(Protocol):
    """Deliver a rendered report to a recipient (e.g. email)."""

    def deliver(self, recipient: str, rendered: str) -> None: ...
