from __future__ import annotations

import re

from .base import BaseModule
from ..models import ScanContext


class CachePolicyModule(BaseModule):
    name = "cache_policy"

    def run(self, context: ScanContext):
        headers = {key.lower(): value for key, value in context.headers.items()}
        cache_control = headers.get("cache-control", "")
        if not cache_control:
            return []

        # Keep this intentionally strict. Public docs often contain words such as
        # "login" in links or menus, so Lite only flags cache policy when the
        # page contains stronger sensitive markers.
        sensitive_markers = [
            r'type=["\']password["\']',
            r'name=["\']password["\']',
            r'name=["\']csrf["\']',
            r'csrf-token',
            r'authenticity_token',
        ]
        contains_sensitive_content = any(
            re.search(pattern, context.html, re.I) for pattern in sensitive_markers
        )
        restrictive_tokens = ["no-store", "private"]

        if contains_sensitive_content and not any(
            token in cache_control.lower() for token in restrictive_tokens
        ):
            return [
                self.finding(
                    "HF-LITE-012",
                    "Sensitive form markers with weak cache policy",
                    "The response contains stronger sensitive-form markers, but the cache policy is not restrictive.",
                    "HTTP response headers",
                    f"Cache-Control: {cache_control}",
                    "Use no-store or private for authenticated or sensitive content where appropriate.",
                    severity="medium",
                    confidence="medium",
                    precision_note="Lite only reports this when password/CSRF-style markers are present to reduce false positives on public pages.",
                )
            ]
        return []
