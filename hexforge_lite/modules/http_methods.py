from __future__ import annotations

from .base import BaseModule
from ..config import ENABLE_LITE_ACTIVE_CHECKS, LITE_ACTIVE_TIMEOUT
from ..fetcher import fetch_method
from ..models import ScanContext

RISKY_METHODS = {"TRACE", "TRACK", "PUT", "DELETE", "PATCH"}


class HttpMethodsModule(BaseModule):
    """Low-impact OPTIONS probe for authorized Lite scans."""

    name = "http_methods"

    def run(self, context: ScanContext):
        if not ENABLE_LITE_ACTIVE_CHECKS:
            return []
        if context.scheme not in {"http", "https"}:
            return []

        try:
            status, headers, body = fetch_method(
                context.final_url,
                method="OPTIONS",
                timeout=LITE_ACTIVE_TIMEOUT,
                max_bytes=2048,
            )
        except Exception:
            return []

        lower_headers = {key.lower(): value for key, value in headers.items()}
        allow = lower_headers.get("allow", "")
        cors_methods = lower_headers.get("access-control-allow-methods", "")
        observed = []
        for source in (allow, cors_methods):
            for item in source.replace(";", ",").split(","):
                method = item.strip().upper()
                if method and method.replace("-", "").isalpha():
                    observed.append(method)
        methods = sorted(set(observed))
        surface_map = context.artifacts.setdefault("surface_map", {})
        if methods:
            surface_map["http_methods"] = methods

        findings = []
        if methods:
            findings.append(
                self.finding(
                    "HF-LITE-038",
                    "HTTP methods observed through safe OPTIONS probe",
                    "The target responded to a single low-impact OPTIONS request and exposed allowed HTTP methods. This maps surface only and is not a vulnerability by itself.",
                    "OPTIONS response headers",
                    f"HTTP {status}; Allow: {allow or 'absent'}; Access-Control-Allow-Methods: {cors_methods or 'absent'}",
                    "Review exposed methods and confirm that state-changing methods are restricted to authenticated, authorized workflows.",
                    severity="info",
                    confidence="high",
                    kind="Informational",
                    evidence_type="safe_options_probe",
                    precision_note="Lite sends one OPTIONS request only. It does not send PUT, DELETE, PATCH, TRACE, payloads, authentication bypasses, or exploit attempts.",
                )
            )

        risky = sorted(set(methods) & RISKY_METHODS)
        if risky:
            findings.append(
                self.finding(
                    "HF-LITE-039",
                    "Potentially sensitive HTTP methods advertised",
                    "The OPTIONS response advertises methods that deserve manual review. This is not proof that unauthenticated state changes are possible.",
                    "OPTIONS response headers",
                    "Advertised methods: " + ", ".join(risky),
                    "Manually verify authorization and server behavior for advertised state-changing or diagnostic methods inside the permitted scope.",
                    severity="low",
                    confidence="medium",
                    kind="Review",
                    evidence_type="safe_options_probe",
                    precision_note="The methods were advertised by headers only. HexForge Lite did not execute those methods, mutate resources, or attempt exploitation.",
                )
            )
        return findings
