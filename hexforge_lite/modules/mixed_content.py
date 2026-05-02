from __future__ import annotations

import re
from urllib.parse import urlparse

from .base import BaseModule
from ..models import ScanContext
from ..utils.html import html_line_for


IGNORED_HTTP_REFERENCES = {
    "www.w3.org",
    "w3.org",
    "schemas.xmlsoap.org",
    "www.w3.org/2000/svg",
}


def _is_namespace_or_schema(url: str) -> bool:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    path = parsed.path.lower()
    if host in {"www.w3.org", "w3.org"} and (
        path.startswith("/2000/")
        or path.startswith("/1999/")
        or path.startswith("/tr/")
    ):
        return True
    if host in {"schema.org", "schemas.xmlsoap.org"}:
        return True
    return False


class MixedContentModule(BaseModule):
    name = "mixed_content"

    def run(self, context: ScanContext):
        if not context.final_url.startswith("https://"):
            return []

        for match in re.finditer(r'http://[^"\'\s<>]+', context.html, re.I):
            url = match.group(0)
            if _is_namespace_or_schema(url):
                continue
            return [
                self.finding(
                    "HF-LITE-024",
                    "Insecure HTTP resource referenced from an HTTPS page",
                    "The page contains a plaintext HTTP reference while the main document is served over HTTPS.",
                    html_line_for(context.html, url),
                    url,
                    "Replace active HTTP resource references with HTTPS equivalents.",
                    severity="medium",
                    confidence="high",
                    precision_note="Known namespace/schema URLs such as W3C SVG references are ignored to reduce false positives.",
                )
            ]
        return []
