from __future__ import annotations

import re

from .base import BaseModule
from ..models import ScanContext
from ..utils.html import html_line_for


class EmailTokenExposureModule(BaseModule):
    name = "email_token_exposure"
    sensitive_locals = {"admin", "administrator", "root", "security", "dev", "devops", "ops", "infra", "internal", "backend", "db", "noreply"}

    def _interesting_emails(self, html: str):
        found = sorted(set(re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', html)))
        interesting = []
        for email in found:
            local = email.split('@', 1)[0].lower()
            if local in self.sensitive_locals:
                interesting.append(email)
        if len(found) >= 3:
            return found[:8]
        return interesting[:8]

    def run(self, context: ScanContext):
        findings = []
        emails = self._interesting_emails(context.html)
        if emails:
            findings.append(
                self.finding(
                    "HF-LITE-020",
                    "Emails exposed in client-side HTML",
                    "The page exposes one or more potentially sensitive email addresses in the HTML source.",
                    html_line_for(context.html, emails[0]),
                    ", ".join(emails[:8]),
                    "Remove unnecessary internal or administrative addresses from public HTML.",
                    severity="info",
                    confidence="medium",
                    kind="Info",
                )
            )
        jwt_like = re.findall(r'eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+', context.html)
        if jwt_like:
            findings.append(
                self.finding(
                    "HF-LITE-021",
                    "JWT-like token exposed in HTML",
                    "The page contains a token string that matches a JWT pattern.",
                    html_line_for(context.html, jwt_like[0]),
                    jwt_like[0],
                    "Do not expose bearer tokens or JWT-like values in public HTML or scripts.",
                    severity="high",
                    confidence="medium",
                )
            )
        return findings
