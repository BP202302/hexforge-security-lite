from __future__ import annotations

from dataclasses import replace

from .base import BaseValidator
from ..models import Finding


class HeaderValidator(BaseValidator):
    def validate(self, finding: Finding) -> Finding | None:
        finding = super().validate(finding)
        if finding is None:
            return None
        if finding.module == "security_headers" and "Missing:" in finding.evidence:
            missing = [p.strip().lower() for p in finding.evidence.split(":", 1)[-1].split(",") if p.strip()]
            severity = "low"
            if "content-security-policy" in missing and len(missing) >= 2:
                severity = "medium"
            confidence = "high" if missing else "medium"
            return replace(
                finding,
                severity=severity,
                confidence=confidence,
                kind="Review",
                precision_note="Missing headers are confirmed from the HTTP response, but impact depends on application behavior.",
            )
        return finding
