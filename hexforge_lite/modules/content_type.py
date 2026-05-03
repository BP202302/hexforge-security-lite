from __future__ import annotations

from .base import BaseModule
from ..models import ScanContext


class ContentTypeModule(BaseModule):
    name = "content_type"

    def run(self, context: ScanContext):
        headers = {key.lower(): value for key, value in context.headers.items()}
        content_type = headers.get("content-type", "")
        findings = []
        if content_type and "text/html" in content_type.lower() and "charset=" not in content_type.lower():
            findings.append(
                self.finding(
                    "HF-LITE-015",
                    "HTML response omits an explicit charset",
                    "The HTML response declares no explicit charset parameter.",
                    "HTTP response headers",
                    content_type,
                    "Set an explicit charset such as UTF-8 for HTML responses.",
                    severity="low",
                    confidence="high",
                    kind="Low",
                )
            )
        if headers.get("x-content-type-options", "").lower() != "nosniff":
            findings.append(
                self.finding(
                    "HF-LITE-016",
                    "MIME sniffing protection missing",
                    "The response does not explicitly disable MIME sniffing.",
                    "HTTP response headers",
                    "X-Content-Type-Options is missing or not set to nosniff",
                    "Set X-Content-Type-Options: nosniff.",
                    severity="low",
                    confidence="high",
                    kind="Low",
                )
            )
        return findings
