from __future__ import annotations

from .base import BaseModule
from ..models import ScanContext


class SecurityHeadersModule(BaseModule):
    name = "security_headers"
    required_headers = [
        "content-security-policy",
        "strict-transport-security",
        "x-content-type-options",
        "referrer-policy",
        "permissions-policy",
    ]

    def run(self, context: ScanContext):
        headers = {key.lower(): value for key, value in context.headers.items()}
        missing = [name for name in self.required_headers if name not in headers]
        findings = []
        if missing:
            findings.append(
                self.finding(
                    "HF-LITE-001",
                    "Missing security headers",
                    "One or more browser hardening headers are missing.",
                    "HTTP response headers",
                    f"Missing: {', '.join(missing)}",
                    "Add conservative browser security headers and tune them per application behavior.",
                    severity="medium",
                    confidence="medium",
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
                    kind="Info",
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
                    kind="Info",
                )
            )
        return findings
