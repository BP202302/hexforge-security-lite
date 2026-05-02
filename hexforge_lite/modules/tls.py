from __future__ import annotations

from .base import BaseModule
from ..fetcher import tls_summary
from ..models import ScanContext


class TlsBasicsModule(BaseModule):
    name = "tls_basics"

    def run(self, context: ScanContext):
        if context.scheme != "https":
            return []
        headers = {key.lower(): value for key, value in context.headers.items()}
        summary = tls_summary(context.host)
        findings = [
            self.finding(
                "HF-LITE-029",
                "TLS certificate and protocol reviewed",
                "The target was contacted using a standard TLS client to capture protocol and certificate summary data.",
                "TLS endpoint",
                summary,
                "Track certificate expiration and retire legacy TLS support.",
                severity="info",
                confidence="high",
                kind="Informational",
            )
        ]
        if "strict-transport-security" not in headers:
            findings.append(
                self.finding(
                    "HF-LITE-030",
                    "HSTS header missing on HTTPS target",
                    "The target uses HTTPS but does not send Strict-Transport-Security.",
                    "HTTP response headers",
                    "Strict-Transport-Security header not found",
                    "Add an HSTS policy after confirming the site is ready for forced HTTPS.",
                    severity="medium",
                    confidence="high",
                    kind="Review",
                    evidence_type="direct_header_observation",
                    precision_note="HTTPS was observed without HSTS. This is a configuration gap, not proof of active exploitation.",
                )
            )
        return findings
