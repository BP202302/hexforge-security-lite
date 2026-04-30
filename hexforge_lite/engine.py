from __future__ import annotations

from datetime import datetime, timezone
from threading import Lock
from typing import Iterable, List

from .config import MAX_URLS_PER_SESSION, VERSION
from .fetcher import fetch_url
from .models import Finding, ScanReport
from .modules import (
    CachePolicyModule,
    ClickjackingModule,
    ContentTypeModule,
    CookieFlagsModule,
    CorsPolicyModule,
    EmailTokenExposureModule,
    ExternalResourcesModule,
    FormsBasicsModule,
    MetadataExposureModule,
    MixedContentModule,
    RobotsSitemapModule,
    SecurityHeadersModule,
    TlsBasicsModule,
    CommentsExposureModule,
    RedirectPolicyModule,
)
from .utils.urls import normalize_url
from .validators import (
    ContentValidator,
    CookieValidator,
    CorsValidator,
    DedupValidator,
    ExposureValidator,
    FormValidator,
    HeaderValidator,
    NetworkValidator,
)


class ScanEngine:
    def __init__(self) -> None:
        self._urls_scanned: set[str] = set()
        self._lock = Lock()
        self.modules = [
            SecurityHeadersModule(),
            ClickjackingModule(),
            CorsPolicyModule(),
            CookieFlagsModule(),
            CachePolicyModule(),
            RedirectPolicyModule(),
            ContentTypeModule(),
            MetadataExposureModule(),
            CommentsExposureModule(),
            EmailTokenExposureModule(),
            ExternalResourcesModule(),
            MixedContentModule(),
            FormsBasicsModule(),
            RobotsSitemapModule(),
            TlsBasicsModule(),
        ]
        self.header_validator = HeaderValidator()
        self.network_validator = NetworkValidator()
        self.content_validator = ContentValidator()
        self.cookie_validator = CookieValidator()
        self.form_validator = FormValidator()
        self.cors_validator = CorsValidator()
        self.exposure_validator = ExposureValidator()
        self.dedup = DedupValidator()

    def _register_url(self, url: str) -> None:
        with self._lock:
            if url not in self._urls_scanned and len(self._urls_scanned) >= MAX_URLS_PER_SESSION:
                raise RuntimeError(f"Community limit reached: {MAX_URLS_PER_SESSION} URLs per server session.")
            self._urls_scanned.add(url)

    def _validate(self, findings: Iterable[Finding]) -> List[Finding]:
        validated = []
        for item in findings:
            candidate = item
            for validator in [
                self.header_validator,
                self.network_validator,
                self.content_validator,
                self.cookie_validator,
                self.form_validator,
                self.cors_validator,
                self.exposure_validator,
            ]:
                updated = validator.validate(candidate)
                if updated is None:
                    candidate = None
                    break
                candidate = updated
            if candidate is not None:
                validated.append(candidate)
        return self.dedup.filter(validated)

    def scan(self, url: str) -> dict:
        normalized = normalize_url(url)
        self._register_url(normalized)
        context = fetch_url(normalized)
        raw_findings: List[Finding] = []
        for module in self.modules:
            raw_findings.extend(module.run(context))
        findings = self._validate(raw_findings)
        report = ScanReport(
            ok=True,
            url=normalized,
            final_url=context.final_url,
            status=context.status,
            headers=context.headers,
            findings=findings,
            count=len(findings),
            limit=MAX_URLS_PER_SESSION,
            version=VERSION,
            modules=[module.name for module in self.modules],
            generated_at=datetime.now(timezone.utc).isoformat(),
        )
        return report.to_dict()
