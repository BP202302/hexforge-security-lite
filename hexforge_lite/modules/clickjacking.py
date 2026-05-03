from __future__ import annotations

import re

from .base import BaseModule
from ..models import ScanContext


class ClickjackingModule(BaseModule):
    name = "clickjacking"

    def run(self, context: ScanContext):
        headers = {key.lower(): value for key, value in context.headers.items()}
        csp = headers.get("content-security-policy", "").lower()
        if "x-frame-options" in headers or "frame-ancestors" in csp:
            return []

        sensitive_ui = bool(
            re.search(
                r'type=["\']password["\']|sign in|log in|checkout|payment|transfer|delete|admin',
                context.html,
                re.I,
            )
        )
        severity = "medium" if sensitive_ui else "low"
        confidence = "medium" if sensitive_ui else "high"

        return [
            self.finding(
                "HF-LITE-004",
                "Frame embedding protection not observed",
                "Neither X-Frame-Options nor CSP frame-ancestors was found in the initial response.",
                "HTTP response headers",
                "Missing X-Frame-Options and CSP frame-ancestors",
                "Set X-Frame-Options or a CSP frame-ancestors directive on sensitive interactive pages.",
                severity=severity,
                confidence=confidence,
                kind="Review",
                precision_note="This is not automatically reportable. Confirm manually that the page remains interactive inside a frame and impacts a sensitive action.",
            )
        ]
