from __future__ import annotations

import re

from .base import BaseModule
from ..models import ScanContext
from ..utils.html import compact_text


class CommentsExposureModule(BaseModule):
    name = "comments_exposure"

    def run(self, context: ScanContext):
        comments = re.findall(r'<!--(.*?)-->', context.html, re.S)
        if not comments:
            return []
        meaningful = []
        for comment in comments:
            cleaned = compact_text(comment, max_len=140)
            if not cleaned:
                continue
            if any(marker in cleaned.lower() for marker in ["todo", "debug", "key", "secret", "internal", "staging", "fixme"]):
                meaningful.append(cleaned)
        if not meaningful:
            return []
        return [
            self.finding(
                "HF-LITE-019",
                "Potentially sensitive HTML comments found",
                "The page contains HTML comments with terms often associated with debug or internal notes.",
                "HTML comments",
                " | ".join(meaningful[:4]),
                "Remove debug or internal comments before production deployment.",
                severity="info",
                confidence="medium",
                kind="Info",
            )
        ]
