from __future__ import annotations

from typing import List

from ..models import Finding, ScanContext


class BaseModule:
    name = "base"

    def run(self, context: ScanContext) -> List[Finding]:
        raise NotImplementedError

    def finding(
        self,
        fid: str,
        title: str,
        description: str,
        location: str,
        evidence: str,
        recommendation: str,
        severity: str = "medium",
        confidence: str = "medium",
        kind: str = "Medium",
    ) -> Finding:
        return Finding(
            id=fid,
            module=self.name,
            title=title,
            description=description,
            location=location,
            evidence=evidence,
            recommendation=recommendation,
            severity=severity,
            confidence=confidence,
            kind=kind,
        )
