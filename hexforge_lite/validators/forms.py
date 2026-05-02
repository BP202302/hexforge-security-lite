from __future__ import annotations

from dataclasses import replace

from .base import BaseValidator
from ..models import Finding


class FormValidator(BaseValidator):
    def validate(self, finding: Finding) -> Finding | None:
        finding = super().validate(finding)
        if finding is None:
            return None
        if finding.module == "forms_basics" and "password" in finding.evidence.lower() and "http://" in finding.evidence.lower():
            return replace(finding, severity="high", confidence="high", kind="Confirmed")
        if finding.module == "forms_basics":
            return replace(finding, severity="low", confidence="high", kind="Review")
        return finding
