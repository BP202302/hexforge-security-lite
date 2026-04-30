from __future__ import annotations

from .base import BaseModule
from ..models import ScanContext


class ClickjackingModule(BaseModule):
    name = "clickjacking"

    def run(self, context: ScanContext):
        headers = {key.lower(): value for key, value in context.headers.items()}
        csp = headers.get("content-security-policy", "").lower()
        if "x-frame-options" in headers or "frame-ancestors" in csp:
            return []
        return [
            self.finding(
                "HF-LITE-004",
                "Page may be embeddable in frames",
                "Neither X-Frame-Options nor CSP frame-ancestors was found.",
                "HTTP response headers",
                "Missing X-Frame-Options and CSP frame-ancestors",
                "Set X-Frame-Options or a CSP frame-ancestors directive.",
                severity="medium",
                confidence="high",
            )
        ]
