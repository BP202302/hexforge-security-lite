from __future__ import annotations

from dataclasses import replace
from typing import Iterable, List

from ..models import Finding


class BaseValidator:
    def validate(self, finding: Finding) -> Finding | None:
        if not finding.evidence or not finding.title or not finding.location:
            return None
        return replace(finding, evidence=str(finding.evidence).strip()[:900])

    def validate_many(self, findings: Iterable[Finding]) -> List[Finding]:
        result = []
        for item in findings:
            validated = self.validate(item)
            if validated is not None:
                result.append(validated)
        return result
