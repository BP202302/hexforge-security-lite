from __future__ import annotations

from dataclasses import replace
from typing import Iterable, List

from ..models import Finding

SEVERITIES = {"critical", "high", "medium", "low", "info"}
CONFIDENCE = {"high", "medium", "low"}
KIND_BY_SEVERITY = {
    "critical": "Confirmed",
    "high": "Confirmed",
    "medium": "Review",
    "low": "Review",
    "info": "Informational",
}


class BaseValidator:
    def validate(self, finding: Finding) -> Finding | None:
        if not finding.evidence or not finding.title or not finding.location:
            return None
        severity = finding.severity.lower().strip()
        confidence = finding.confidence.lower().strip()
        if severity not in SEVERITIES:
            severity = "medium"
        if confidence not in CONFIDENCE:
            confidence = "medium"
        kind = finding.kind if finding.kind in {"Confirmed", "Review", "Informational"} else KIND_BY_SEVERITY[severity]
        return replace(
            finding,
            severity=severity,
            confidence=confidence,
            kind=kind,
            evidence=str(finding.evidence).strip()[:900],
        )

    def validate_many(self, findings: Iterable[Finding]) -> List[Finding]:
        result = []
        for item in findings:
            validated = self.validate(item)
            if validated is not None:
                result.append(validated)
        return result
