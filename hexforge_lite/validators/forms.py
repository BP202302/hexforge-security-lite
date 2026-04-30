from __future__ import annotations

from dataclasses import replace

from .base import BaseValidator
from ..models import Finding


class FormValidator(BaseValidator):
    def validate(self, finding: Finding) -> Finding | None:
        finding = super().validate(finding)
        if finding is None:
            return None
        if finding.module == "forms_basics" and "Password" in finding.evidence:
            return replace(finding, severity="medium", confidence="high")
        return finding
