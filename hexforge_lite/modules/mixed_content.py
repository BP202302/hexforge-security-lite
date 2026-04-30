from __future__ import annotations

import re

from .base import BaseModule
from ..models import ScanContext
from ..utils.html import html_line_for


class MixedContentModule(BaseModule):
    name = "mixed_content"

    def run(self, context: ScanContext):
        if not context.final_url.startswith("https://"):
            return []
        match = re.search(r'http://[^"\'\s<>]+', context.html, re.I)
        if not match:
            return []
        return [
            self.finding(
                "HF-LITE-024",
                "Insecure HTTP resource referenced from an HTTPS page",
                "The page contains a plaintext HTTP reference while the main document is served over HTTPS.",
                html_line_for(context.html, match.group(0)),
                match.group(0),
                "Replace HTTP resource references with HTTPS equivalents.",
                severity="medium",
                confidence="high",
            )
        ]
