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
                    "Wildcard CORS policy observed",
                    "The response allows any origin. This is not automatically critical unless sensitive data or credentials are involved.",
                    "HTTP response headers",
                    f"Access-Control-Allow-Origin: {origin}; Access-Control-Allow-Credentials: {credentials or 'absent'}",
                    "Avoid wildcard CORS on sensitive or authenticated endpoints.",
                    severity="low",
                    confidence="high",
                    kind="Review",
                    evidence_type="direct_header_observation",
                    precision_note="No severity inflation: wildcard CORS without credentials is a review item, not a confirmed high-risk issue.",
                )
            )
        return findings
