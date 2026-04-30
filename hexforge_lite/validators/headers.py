from __future__ import annotations

from dataclasses import replace

from .base import BaseValidator
from ..models import Finding


class HeaderValidator(BaseValidator):
    def validate(self, finding: Finding) -> Finding | None:
        finding = super().validate(finding)
        if finding is None:
            return None
        if "Missing:" in finding.evidence and finding.severity == "medium":
            count = len([part for part in finding.evidence.split(":", 1)[-1].split(",") if part.strip()])
            confidence = "high" if count >= 2 else "medium"
            return replace(finding, confidence=confidence)
        return finding
