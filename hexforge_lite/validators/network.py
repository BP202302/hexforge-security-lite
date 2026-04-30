from __future__ import annotations

from dataclasses import replace

from .base import BaseValidator
from ..models import Finding


class NetworkValidator(BaseValidator):
    def validate(self, finding: Finding) -> Finding | None:
        finding = super().validate(finding)
        if finding is None:
            return None
        if finding.module in {"redirect_policy", "tls_basics"}:
            return replace(finding, confidence="high")
        return finding
