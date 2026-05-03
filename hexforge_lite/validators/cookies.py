from __future__ import annotations

from dataclasses import replace

from .base import BaseValidator
from ..models import Finding


class CookieValidator(BaseValidator):
    def validate(self, finding: Finding) -> Finding | None:
        finding = super().validate(finding)
        if finding is None:
            return None

        if finding.module == "cookie_flags":
            evidence = finding.evidence.lower()
            missing_secure = "missing secure" in evidence
            missing_httponly = "missing httponly" in evidence
            session_like = any(
                token in evidence
                for token in [
                    "session",
                    "auth",
                    "token",
                    "jwt",
                    "sid",
                ]
            )
            severity = "medium" if missing_secure or (missing_httponly and session_like) else "low"
            return replace(
                finding,
                confidence="high",
                severity=severity,
                kind="Review",
                precision_note="Cookie attributes were inspected directly. Severity is conservative unless the cookie appears session/auth-related.",
            )
        return finding
