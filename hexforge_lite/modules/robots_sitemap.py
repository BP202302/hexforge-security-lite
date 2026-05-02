from __future__ import annotations

from .base import BaseModule
from ..config import ROBOTS_TIMEOUT
from ..fetcher import fetch_text
from ..models import ScanContext


class RobotsSitemapModule(BaseModule):
    name = "robots_sitemap"

    def run(self, context: ScanContext):
        base = f"{context.scheme}://{context.parsed.netloc}"
        findings = []
        for fid, path in [("HF-LITE-027", "/robots.txt"), ("HF-LITE-028", "/sitemap.xml")]:
            try:
                status, _, body = fetch_text(base + path, timeout=ROBOTS_TIMEOUT)
            except Exception:
                continue
            if status >= 400:
                continue
            excerpt = body[:220].replace("\n", " ").strip() or f"{path} is reachable"
            findings.append(
                self.finding(
                    fid,
                    f"{path} is publicly reachable",
                    f"The lightweight discovery file {path} is accessible.",
                    path,
                    excerpt,
                    "Review whether the file exposes unnecessary internal paths or staging references.",
                    severity="info",
                    confidence="medium",
                    kind="Info",
                )
            )
        return findings
