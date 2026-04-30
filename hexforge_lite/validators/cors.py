from __future__ import annotations

from dataclasses import replace

from .base import BaseValidator
from ..models import Finding


class CorsValidator(BaseValidator):
    def validate(self, finding: Finding) -> Finding | None:
        finding = super().validate(finding)
        if finding is None:
            return None
        if finding.module == "cors_policy" and "*" in finding.evidence:
            severity = "high" if "credentials" in finding.evidence.lower() else "medium"
            return replace(finding, severity=severity, confidence="high")
        return finding
