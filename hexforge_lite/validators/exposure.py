from __future__ import annotations

from dataclasses import replace

from .base import BaseValidator
from ..models import Finding


class ExposureValidator(BaseValidator):
    def validate(self, finding: Finding) -> Finding | None:
        finding = super().validate(finding)
        if finding is None:
            return None
        if finding.module == "email_token_exposure":
            severity = "high" if "JWT" in finding.title else "info"
            return replace(finding, severity=severity, confidence="medium")
        return finding
