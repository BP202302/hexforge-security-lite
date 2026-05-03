from __future__ import annotations

from .base import BaseModule
from ..models import ScanContext


class CookieFlagsModule(BaseModule):
    name = "cookie_flags"

    def run(self, context: ScanContext):
        set_cookie = [
            value
            for key, value in context.headers.items()
            if key.lower() == "set-cookie"
        ]
        findings = []
        for index, cookie in enumerate(set_cookie[:6], start=1):
            lowered = cookie.lower()
            missing = []
            if "secure" not in lowered and context.scheme == "https":
                missing.append("Secure")
            if "httponly" not in lowered:
                missing.append("HttpOnly")
            if "samesite" not in lowered:
                missing.append("SameSite")
            if missing:
                findings.append(
                    self.finding(
                        f"HF-LITE-00{5 + index}",
                        "Cookie missing security attributes",
                        "A response cookie is missing one or more defensive attributes.",
                        f"Set-Cookie #{index}",
                        f"Missing {', '.join(missing)} in: {cookie[:220]}",
                        "Set Secure, HttpOnly, and SameSite attributes according to the session model.",
                        severity="medium",
                        confidence="high",
                    )
                )
        return findings
