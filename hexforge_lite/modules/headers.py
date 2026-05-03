from __future__ import annotations

from .base import BaseModule
from ..datasets import headers_dataset
from ..models import ScanContext


class SecurityHeadersModule(BaseModule):
    name = "security_headers"
    def __init__(self) -> None:
        data = headers_dataset()
        self.required_headers = [str(item).lower() for item in data.get("required", [])]

    def run(self, context: ScanContext):
        headers = {key.lower(): value for key, value in context.headers.items()}
        missing = [name for name in self.required_headers if name not in headers]
        findings = []
        if missing:
            findings.append(
                self.finding(
                    "HF-LITE-001",
                    "Browser hardening headers missing",
                    "One or more defensive browser headers were not observed in the response. This is reported conservatively and does not prove exploitation.",
                    "HTTP response headers",
                    f"Missing: {', '.join(missing)}",
                    "Add conservative browser security headers and tune them per application behavior.",
                    severity="low",
                    confidence="high",
                    kind="Review",
                    evidence_type="direct_header_observation",
                    precision_note="Confirmed from response headers; severity is conservative because exploitability depends on app context.",
                )
            )
        if "server" in headers:
            findings.append(
                self.finding(
                    "HF-LITE-002",
                    "Server header discloses technology",
                    "The response exposes implementation details in the Server header.",
                    "HTTP response headers",
                    f"Server: {headers['server']}",
                    "Minimize unnecessary technology disclosure in the Server header.",
                    severity="info",
                    confidence="high",
                    kind="Informational",
                )
            )
        if "x-powered-by" in headers:
            findings.append(
                self.finding(
                    "HF-LITE-003",
                    "X-Powered-By discloses framework details",
                    "The response exposes implementation details in the X-Powered-By header.",
                    "HTTP response headers",
                    f"X-Powered-By: {headers['x-powered-by']}",
                    "Remove or generalize X-Powered-By where possible.",
                    severity="info",
                    confidence="high",
                    kind="Informational",
                )
            )
        return findings
