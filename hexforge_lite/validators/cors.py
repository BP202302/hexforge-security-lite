from __future__ import annotations

from dataclasses import replace

from .base import BaseValidator
from ..models import Finding


class CorsValidator(BaseValidator):
    def validate(self, finding: Finding) -> Finding | None:
        finding = super().validate(finding)
        if finding is None:
            return None
        if finding.module != "cors_policy":
            return finding

        evidence = finding.evidence.lower()
        wildcard = "access-control-allow-origin: *" in evidence
        credentials_true = "access-control-allow-credentials: true" in evidence
        credentials_absent = "credentials: absent" in evidence or "allow-credentials: absent" in evidence

        if wildcard and credentials_true:
            return replace(
                finding,
                severity="high",
                confidence="high",
                kind="Confirmed",
                precision_note="Wildcard origin is combined with credentials; this is a stronger CORS misconfiguration signal.",
            )
        if wildcard and credentials_absent:
            return replace(
                finding,
                severity="low",
                confidence="high",
                kind="Review",
                precision_note="Wildcard CORS was observed, but credentials were absent; this is not automatically a critical issue.",
            )
        if wildcard:
            return replace(
                finding,
                severity="low",
                confidence="medium",
                kind="Review",
                precision_note="Wildcard CORS was observed; impact depends on whether the endpoint exposes sensitive data.",
            )
        return finding
