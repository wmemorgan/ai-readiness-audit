"""Delivery adapters. The engine ships a no-op channel — no operational coupling.

A hosted deployment plugs a real email/pipeline channel in behind the DeliveryChannel port.
"""

from __future__ import annotations


class NoopDeliveryChannel:
    """A delivery channel that intentionally does nothing (the policy-neutral default)."""

    def deliver(self, recipient: str, rendered: str) -> None:
        return None
