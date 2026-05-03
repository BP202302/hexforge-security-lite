from __future__ import annotations

from typing import Iterable

from ..models import Finding


class FindingFormatter:
    def sort(self, findings: Iterable[Finding]) -> list[Finding]:
        order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        confidence = {"high": 0, "medium": 1, "low": 2}
        return sorted(findings, key=lambda f: (order.get(f.severity, 9), confidence.get(f.confidence, 9), f.module, f.id))
