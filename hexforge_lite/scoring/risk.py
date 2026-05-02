from __future__ import annotations

from collections import Counter
from typing import Iterable

from ..models import Finding

SEVERITY_POINTS = {"critical": 3.0, "high": 2.4, "medium": 1.2, "low": 0.45, "info": 0.0}
CONFIDENCE_MULTIPLIER = {"high": 1.0, "medium": 0.72, "low": 0.45}


class RiskScorer:
    def summarize(self, findings: Iterable[Finding]) -> dict:
        items = list(findings)
        counts = Counter(item.severity for item in items)
        confidence = Counter(item.confidence for item in items)
        kinds = Counter(item.kind for item in items)
        raw = 0.0
        for item in items:
            raw += SEVERITY_POINTS.get(item.severity, 0.8) * CONFIDENCE_MULTIPLIER.get(item.confidence, 0.7)
        score = min(10.0, round(raw, 1))
        posture = "clean" if score == 0 else "review" if score < 4 else "elevated" if score < 7 else "high"
        return {
            "risk_score": score,
            "posture": posture,
            "severity_counts": {key: counts.get(key, 0) for key in ["critical", "high", "medium", "low", "info"]},
            "confidence_counts": {key: confidence.get(key, 0) for key in ["high", "medium", "low"]},
            "finding_types": dict(kinds),
            "precision_mode": "low-noise passive analysis",
            "note": "Score is conservative and does not claim exploitability without proof.",
        }
