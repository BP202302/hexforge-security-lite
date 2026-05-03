from __future__ import annotations

from typing import Iterable

from ..models import Finding, ScanContext


class ModuleDispatcher:
    """Runs Lite modules in a predictable order without changing their behavior."""

    def run(self, modules: Iterable[object], context: ScanContext) -> list[Finding]:
        findings: list[Finding] = []
        for module in modules:
            findings.extend(module.run(context))
        return findings
