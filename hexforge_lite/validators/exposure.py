from __future__ import annotations

from dataclasses import replace

from .base import BaseValidator
from ..models import Finding


class ExposureValidator(BaseValidator):
    def validate(self, finding: Finding) -> Finding | None:
        finding = super().validate(finding)
        if finding is None:
            return None

        if finding.module == "client_surface" and finding.id in {"HF-LITE-031", "HF-LITE-033"}:
            return replace(
                finding,
                severity="info",
                confidence=finding.confidence,
                kind="Informational",
                precision_note=finding.precision_note,
            )

        if finding.module == "robots_sitemap":
            return replace(
                finding,
                severity="info",
                confidence="high",
                kind="Informational",
                precision_note="Public discovery files are normal; this is only useful if they expose internal or staging paths.",
            )

        if finding.module == "email_token_exposure":
            evidence = finding.evidence.lower()
            if "example.com" in evidence or "support@" in evidence:
                return replace(
                    finding,
                    severity="info",
                    confidence="medium",
                    kind="Informational",
                    precision_note="Public contact-style data is informational unless it exposes secrets or private data.",
                )
            return replace(finding, confidence="medium", kind="Review")

        return finding
