from __future__ import annotations

from .base import BaseModule
from ..models import ScanContext


class CorsPolicyModule(BaseModule):
    name = "cors_policy"

    def run(self, context: ScanContext):
        headers = {key.lower(): value for key, value in context.headers.items()}
        origin = headers.get("access-control-allow-origin")
        credentials = headers.get("access-control-allow-credentials", "")
        if not origin:
            return []
        findings = []
        if origin.strip() == "*":
            findings.append(
                self.finding(
                    "HF-LITE-005",
                    "Wildcard CORS policy detected",
                    "The response allows every origin to read the resource.",
                    "HTTP response headers",
                    f"Access-Control-Allow-Origin: {origin}; Access-Control-Allow-Credentials: {credentials or 'absent'}",
                    "Avoid wildcard CORS on sensitive or authenticated endpoints.",
                    severity="medium",
                    confidence="high",
                )
            )
        return findings
