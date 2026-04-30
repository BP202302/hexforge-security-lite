from __future__ import annotations

from dataclasses import replace

from .base import BaseValidator
from ..models import Finding


class CookieValidator(BaseValidator):
    def validate(self, finding: Finding) -> Finding | None:
        finding = super().validate(finding)
        if finding is None:
            return None
        if finding.module == "cookie_flags":
            severity = "medium" if "Secure" in finding.recommendation else finding.severity
            return replace(finding, confidence="high", severity=severity)
        return finding
