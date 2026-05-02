from __future__ import annotations

from .base import BaseModule
from ..models import ScanContext


class RedirectPolicyModule(BaseModule):
    name = "redirect_policy"

    def run(self, context: ScanContext):
        findings = []
        if context.final_url != context.requested_url:
            findings.append(
                self.finding(
                    "HF-LITE-013",
                    "Request followed a redirect",
                    "The final URL differs from the requested target.",
                    "HTTP redirect chain",
                    f"{context.requested_url} -> {context.final_url}",
                    "Verify the redirect target and enforce HTTPS where expected.",
                    severity="info",
                    confidence="high",
                    kind="Info",
                )
            )
        if context.requested_url.startswith("http://") and context.final_url.startswith("http://"):
            findings.append(
                self.finding(
                    "HF-LITE-014",
                    "HTTP target did not upgrade to HTTPS",
                    "The target stayed on plaintext HTTP.",
                    "HTTP redirect chain",
                    context.final_url,
                    "Redirect HTTP traffic to HTTPS where supported.",
                    severity="medium",
                    confidence="high",
                )
            )
        return findings
