from __future__ import annotations

import re

from .base import BaseModule
from ..models import ScanContext
from ..utils.html import html_line_for


class MetadataExposureModule(BaseModule):
    name = "metadata_exposure"

    def run(self, context: ScanContext):
        findings = []
        generator = re.search(r'<meta[^>]+name=["\']generator["\'][^>]*>', context.html, re.I)
        if generator:
            findings.append(
                self.finding(
                    "HF-LITE-017",
                    "Generator metadata exposed",
                    "The page exposes generator metadata that may help fingerprint the stack.",
                    html_line_for(context.html, generator.group(0)),
                    generator.group(0),
                    "Remove generator metadata if it is not required.",
                    severity="info",
                    confidence="high",
                    kind="Info",
                )
            )
        canonical = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', context.html, re.I)
        if canonical and canonical.group(1).startswith("http://") and context.final_url.startswith("https://"):
            findings.append(
                self.finding(
                    "HF-LITE-018",
                    "Canonical URL points to HTTP",
                    "The canonical link references an insecure HTTP URL.",
                    html_line_for(context.html, canonical.group(0)),
                    canonical.group(0),
                    "Use HTTPS canonical URLs when the page is served over HTTPS.",
                    severity="low",
                    confidence="high",
                    kind="Low",
                )
            )
        return findings
