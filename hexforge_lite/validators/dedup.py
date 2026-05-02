from __future__ import annotations

from typing import Iterable, List, Set, Tuple

from ..models import Finding


class DedupValidator:
    def filter(self, findings: Iterable[Finding]) -> List[Finding]:
        seen: Set[Tuple[str, str, str]] = set()
        unique: List[Finding] = []
        hsts_reported = False
        order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        for item in sorted(findings, key=lambda f: order.get(f.severity, 9)):
            text = f"{item.title} {item.evidence}".lower()
            if "strict-transport-security" in text or "hsts" in text:
                if hsts_reported:
                    continue
                hsts_reported = True
            fingerprint = (item.id, item.title.lower().strip(), item.location.lower().strip())
            if fingerprint in seen:
                continue
            seen.add(fingerprint)
            unique.append(item)
        return unique
