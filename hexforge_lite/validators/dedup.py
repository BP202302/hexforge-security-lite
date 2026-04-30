from __future__ import annotations

from typing import Iterable, List, Set, Tuple

from ..models import Finding


class DedupValidator:
    def filter(self, findings: Iterable[Finding]) -> List[Finding]:
        seen: Set[Tuple[str, str, str]] = set()
        unique: List[Finding] = []
        for item in findings:
            fingerprint = (item.module, item.title, item.location)
            if fingerprint in seen:
                continue
            seen.add(fingerprint)
            unique.append(item)
        return unique
