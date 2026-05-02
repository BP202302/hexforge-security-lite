from __future__ import annotations

from dataclasses import replace

from .base import BaseValidator
from ..models import Finding


class NetworkValidator(BaseValidator):
    def validate(self, finding: Finding) -> Finding | None:
        finding = super().validate(finding)
        if finding is None:
            return None
        if finding.module == "tls_basics":
            return replace(finding, severity="info" if "reviewed" in finding.title.lower() else finding.severity, confidence="high")
        if finding.module == "redirect_policy":
            return replace(finding, confidence="high")
        return finding
