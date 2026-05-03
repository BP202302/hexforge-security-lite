from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
from urllib.parse import ParseResult


@dataclass
class Finding:
    id: str
    module: str
    title: str
    description: str
    location: str
    evidence: str
    recommendation: str
    severity: str = "medium"
    confidence: str = "medium"
    kind: str = "Review"
    evidence_type: str = "observed"
    precision_note: str = "Classified with passive evidence only."

    def to_dict(self) -> dict:
        data = asdict(self)
        data["evidence"] = self.evidence[:900]
        return data


@dataclass
class ScanContext:
    requested_url: str
    final_url: str
    status: int
    headers: Dict[str, str]
    html: str
    parsed: ParseResult
    artifacts: Dict[str, object] = field(default_factory=dict)
    fetched_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def host(self) -> str:
        return self.parsed.hostname or ""

    @property
    def scheme(self) -> str:
        return self.parsed.scheme


@dataclass
class ScanReport:
    ok: bool
    url: str
    final_url: str
    status: int
    headers: Dict[str, str]
    findings: List[Finding]
    count: int
    limit: int
    version: str
    modules: List[str]
    generated_at: str
    summary: Dict[str, object] = field(default_factory=dict)
    surface_map: Dict[str, object] = field(default_factory=dict)
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "ok": self.ok,
            "url": self.url,
            "final_url": self.final_url,
            "status": self.status,
            "headers": self.headers,
            "findings": [item.to_dict() for item in self.findings],
            "count": self.count,
            "limit": self.limit,
            "version": self.version,
            "modules": self.modules,
            "summary": self.summary,
            "surface_map": self.surface_map,
            "generated_at": self.generated_at,
            "error": self.error,
        }
