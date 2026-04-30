from __future__ import annotations

import re
from urllib.parse import urlparse

from .base import BaseModule
from ..models import ScanContext
from ..utils.html import html_line_for


class ExternalResourcesModule(BaseModule):
    name = "external_resources"

    def run(self, context: ScanContext):
        findings = []
        external_scripts = []
        script_tags = re.findall(r'<script[^>]+src=["\']([^"\']+)["\'][^>]*>', context.html, re.I)
        for src in script_tags:
            parsed = urlparse(src)
            if parsed.scheme in {"http", "https"} and parsed.hostname and parsed.hostname != context.host:
                external_scripts.append(src)
        if external_scripts:
            findings.append(
                self.finding(
                    "HF-LITE-022",
                    "External scripts loaded from third-party origins",
                    "The page loads one or more script resources from a different host.",
                    "HTML <script> tags",
                    "\n".join(external_scripts[:8]),
                    "Review trust boundaries for third-party scripts and pin versions where possible.",
                    severity="info",
                    confidence="high",
                    kind="Info",
                )
            )
        tags_without_sri = []
        for tag in re.findall(r'<script[^>]+src=["\']https?://[^"\']+["\'][^>]*>', context.html, re.I):
            if "integrity=" not in tag.lower():
                tags_without_sri.append(tag)
        if tags_without_sri:
            findings.append(
                self.finding(
                    "HF-LITE-023",
                    "External script without Subresource Integrity",
                    "A remote script tag does not declare an integrity attribute.",
                    html_line_for(context.html, tags_without_sri[0]),
                    tags_without_sri[0],
                    "Add integrity and crossorigin attributes to trusted external scripts.",
                    severity="low",
                    confidence="high",
                    kind="Low",
                )
            )
        return findings
