from __future__ import annotations

import re

from .base import BaseModule
from ..models import ScanContext
from ..utils.html import html_line_for


class FormsBasicsModule(BaseModule):
    name = "forms_basics"

    def run(self, context: ScanContext):
        findings = []
        forms = re.findall(r'<form[^>]*>', context.html, re.I)
        if forms:
            missing_method = [tag for tag in forms if "method=" not in tag.lower()]
            if missing_method:
                findings.append(
                    self.finding(
                        "HF-LITE-025",
                        "Form missing explicit HTTP method",
                        "A form tag does not declare a method attribute.",
                        html_line_for(context.html, missing_method[0]),
                        missing_method[0],
                        "Declare explicit GET or POST methods on forms to avoid ambiguous behavior.",
                        severity="low",
                        confidence="high",
                        kind="Low",
                    )
                )
        password_field = re.search(r'<input[^>]+type=["\']password["\'][^>]*>', context.html, re.I)
        if password_field and context.final_url.startswith("http://"):
            findings.append(
                self.finding(
                    "HF-LITE-026",
                    "Password field served over HTTP",
                    "The page contains a password input but the target is not using HTTPS.",
                    html_line_for(context.html, password_field.group(0)),
                    f"Password field over HTTP at {context.final_url}",
                    "Serve credential entry points exclusively over HTTPS.",
                    severity="high",
                    confidence="high",
                )
            )
        return findings
