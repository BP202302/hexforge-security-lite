from __future__ import annotations

import re

from hexforge_lite.modules.base import BaseModule
from hexforge_lite.utils.html import compact_text, html_line_for

GENERATOR_RE = re.compile(
    r'<meta[^>]+name=["\']generator["\'][^>]+content=["\'](?P<content>[^"\']+)["\'][^>]*>',
    re.I,
)


class GeneratorMetadataPlugin(BaseModule):
    """Safe Lite plugin that observes public generator metadata."""

    name = "generator_metadata_plugin"
    lite_safe = True

    def run(self, context):
        match = GENERATOR_RE.search(context.html or "")
        if not match:
            return []
        evidence = compact_text(match.group("content"), max_len=240)
        return [
            self.finding(
                "HF-PLUGIN-001",
                "Generator metadata observed by Lite plugin",
                "A Lite plugin observed public generator metadata in the HTML. This is informational and not a vulnerability by itself.",
                html_line_for(context.html, match.group(0)),
                evidence,
                "Review whether public generator metadata is intentional. Remove or generalize it if it exposes unnecessary implementation detail.",
                severity="info",
                confidence="high",
                kind="Informational",
                evidence_type="plugin_passive_html_observation",
                precision_note="This Lite plugin reads the already-fetched HTML only; it does not make network requests or attempt exploitation.",
            )
        ]
