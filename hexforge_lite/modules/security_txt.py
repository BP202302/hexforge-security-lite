from __future__ import annotations

from urllib.parse import urljoin

from .base import BaseModule
from ..config import ROBOTS_TIMEOUT
from ..fetcher import fetch_text
from ..models import ScanContext
from ..utils.html import compact_text


class SecurityTxtModule(BaseModule):
    """Passive RFC 9116 security.txt discovery. Informational only."""

    name = "security_txt"

    def run(self, context: ScanContext):
        findings = []
        candidates = [
            urljoin(context.final_url, "/.well-known/security.txt"),
            urljoin(context.final_url, "/security.txt"),
        ]
        for candidate in candidates:
            try:
                status, headers, body = fetch_text(candidate, timeout=ROBOTS_TIMEOUT, max_bytes=12000)
            except Exception:
                continue
            content_type = (headers.get("Content-Type") or "").lower()
            if status != 200 or not body.strip():
                continue
            lowered = body.lower()
            if "contact:" not in lowered and "security" not in lowered:
                continue
            lines = [line.strip() for line in body.splitlines() if line.strip() and not line.strip().startswith("#")]
            observed = []
            for key in ["Contact", "Expires", "Encryption", "Policy", "Acknowledgments", "Preferred-Languages", "Canonical"]:
                for line in lines:
                    if line.lower().startswith(key.lower() + ":"):
                        observed.append(line)
                        break
            findings.append(
                self.finding(
                    "HF-LITE-037",
                    "security.txt policy file observed",
                    "A security.txt file is publicly reachable. This helps researchers find the correct reporting channel and is informational by itself.",
                    candidate,
                    compact_text("\n".join(observed or lines[:8]), max_len=900),
                    "Keep security.txt accurate, include a valid Contact field, and maintain expiration or policy links according to your disclosure process.",
                    severity="info",
                    confidence="high",
                    kind="Informational",
                    evidence_type="passive_disclosure_policy",
                    precision_note="security.txt discovery is passive and does not indicate a vulnerability; it only documents the target disclosure channel when present.",
                )
            )
            break
        return findings
