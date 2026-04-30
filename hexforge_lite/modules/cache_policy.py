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
        sensitive_markers = [r'type=["\']password["\']', r'name=["\']password["\']', r'csrf', r'login']
        contains_sensitive_content = any(re.search(pattern, context.html, re.I) for pattern in sensitive_markers)
        if contains_sensitive_content and not any(token in cache_control.lower() for token in ["no-store", "private"]):
            return [
                self.finding(
                    "HF-LITE-012",
                    "Potentially sensitive page has weak cache policy",
                    "The response contains sensitive form markers but the cache policy is not restrictive.",
                    "HTTP response headers",
                    f"Cache-Control: {cache_control}",
                    "Use no-store or private for authenticated or sensitive content where appropriate.",
                    severity="medium",
                    confidence="medium",
                )
            ]
        return []
