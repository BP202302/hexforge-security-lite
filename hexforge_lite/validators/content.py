from __future__ import annotations

from dataclasses import replace

from .base import BaseValidator
from ..models import Finding


class ContentValidator(BaseValidator):
    def validate(self, finding: Finding) -> Finding | None:
        finding = super().validate(finding)
        if finding is None:
            return None
        if finding.module in {"metadata_exposure", "comments_exposure"}:
            return replace(finding, severity="info", confidence="medium", kind="Informational")
        if finding.module in {"mixed_content", "external_resources"}:
            return replace(finding, confidence="high", kind="Review")
        return finding
