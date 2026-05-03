from __future__ import annotations

import re
from urllib.parse import parse_qsl, urljoin, urlparse

from .base import BaseModule
from .client_surface import _is_static_asset_path, _same_host
from ..config import JS_FETCH_MAX_BYTES, ROBOTS_TIMEOUT
from ..fetcher import fetch_text
from ..models import ScanContext
from ..utils.html import compact_text

# Lite-safe JavaScript surface analysis. It reads only same-origin scripts already
# discovered by ClientSurfaceModule and extracts review clues without payloads.
JS_URL_LITERAL_RE = re.compile(r"[\"'`]((?:https?://|/)(?:[^\"'`\\\s<>]{2,220}))[\"'`]", re.I)
JS_FETCH_RE = re.compile(r"\b(?:fetch|open|axios\.(?:get|post|put|delete|patch)|postMessage)\s*\(\s*[\"'`]([^\"'`]{1,220})[\"'`]", re.I)
GRAPHQL_RE = re.compile(r"\b(query|mutation)\s+[A-Za-z0-9_]{2,80}|/graphql\b", re.I)
STORAGE_RE = re.compile(r"\b(?:localStorage|sessionStorage|indexedDB)\b", re.I)
SENSITIVE_NAME_RE = re.compile(
    r"\b(?:api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret|secret|jwt|bearer|authorization)\b",
    re.I,
)


def _clean_candidate(base_url: str, raw: str) -> str | None:
    raw = (raw or "").strip()
    if not raw or raw.startswith(("//", "data:", "blob:", "mailto:", "tel:", "#")):
        return None
    if raw.startswith(("/", "http://", "https://")):
        return urljoin(base_url, raw)
    return None


def _path_or_url_for_display(base_host: str, candidate: str) -> str:
    parsed = urlparse(candidate)
    if parsed.hostname and parsed.hostname.lower() != base_host.lower():
        return f"{parsed.scheme}://{parsed.hostname}{parsed.path or '/'}"
    value = parsed.path or candidate
    if parsed.query:
        value = f"{value}?{parsed.query}"
    return value


def _looks_interesting_path(value: str) -> bool:
    parsed = urlparse(value)
    path = parsed.path or value
    lower = path.lower()
    if _is_static_asset_path(lower):
        return False
    interesting = (
        "/api", "/rest", "/graphql", "/auth", "/oauth", "/login", "/signin",
        "/account", "/admin", "/user", "/profile", "/cart", "/checkout",
        "/orders", "/search", "/v1", "/v2", "/v3", "/internal",
    )
    return lower.startswith(interesting) or any(part in lower for part in ("token", "session", "callback"))


class JsSurfaceAnalyzerModule(BaseModule):
    """Read-only JavaScript review map for Lite."""

    name = "js_surface_analyzer"

    def run(self, context: ScanContext):
        surface = context.artifacts.setdefault("surface_map", {})
        scripts = list(dict.fromkeys(surface.get("scripts", []) or []))[:6]
        if not scripts:
            return []

        endpoints: set[str] = set()
        external_hosts: set[str] = set()
        parameters: set[str] = set(surface.get("parameters", []) or [])
        sensitive_names: set[str] = set()
        storage_markers: set[str] = set()
        graphql_markers: set[str] = set()
        inspected: list[str] = []

        for script_url in scripts:
            if not _same_host(context.host, script_url):
                continue
            try:
                status, headers, body = fetch_text(script_url, timeout=ROBOTS_TIMEOUT, max_bytes=JS_FETCH_MAX_BYTES)
            except TypeError:
                try:
                    status, headers, body = fetch_text(script_url, timeout=ROBOTS_TIMEOUT)
                except Exception:
                    continue
            except Exception:
                continue
            if status >= 400 or not body:
                continue
            ctype = (headers.get("Content-Type") or "").lower()
            if ctype and not any(token in ctype for token in ("javascript", "ecmascript", "text/plain", "octet-stream")):
                # Some CDNs return generic types, but avoid analyzing clear non-JS payloads.
                continue
            inspected.append(script_url)
            sample = body[:JS_FETCH_MAX_BYTES]

            for regex in (JS_FETCH_RE, JS_URL_LITERAL_RE):
                for match in regex.finditer(sample):
                    candidate = _clean_candidate(context.final_url, match.group(1))
                    if not candidate:
                        continue
                    parsed = urlparse(candidate)
                    if parsed.hostname and parsed.hostname.lower() != context.host.lower():
                        external_hosts.add(parsed.hostname.lower())
                        continue
                    if _looks_interesting_path(candidate):
                        endpoints.add(_path_or_url_for_display(context.host, candidate))
                    for key, _ in parse_qsl(parsed.query, keep_blank_values=True):
                        if key:
                            parameters.add(key)

            for match in SENSITIVE_NAME_RE.finditer(sample):
                sensitive_names.add(match.group(0).lower())
            for match in STORAGE_RE.finditer(sample):
                storage_markers.add(match.group(0))
            if GRAPHQL_RE.search(sample):
                graphql_markers.add("GraphQL marker")

        if inspected:
            js_surface = surface.setdefault("js_surface", {})
            js_surface.update(
                {
                    "inspected_scripts": inspected[:6],
                    "endpoints": sorted(endpoints)[:40],
                    "external_hosts": sorted(external_hosts)[:20],
                    "sensitive_names_redacted": sorted(sensitive_names)[:20],
                    "browser_storage": sorted(storage_markers)[:10],
                    "graphql_markers": sorted(graphql_markers)[:8],
                }
            )
            surface["parameters"] = sorted(parameters)[:50]
            if endpoints:
                existing_api = set(surface.get("api_routes", []) or [])
                surface["api_routes"] = sorted(existing_api | endpoints)[:50]

        findings = []
        if endpoints or graphql_markers:
            evidence = []
            if endpoints:
                evidence.append("JS endpoints: " + " | ".join(sorted(endpoints)[:18]))
            if graphql_markers:
                evidence.append("GraphQL: marker observed")
            findings.append(
                self.finding(
                    "HF-LITE-040",
                    "JavaScript surface exposes reviewable endpoints",
                    "Same-origin JavaScript references endpoint-like paths. This is a high-value map for manual review, not proof of vulnerability.",
                    "Same-origin JavaScript bundle analysis",
                    compact_text("\n".join(evidence), max_len=850),
                    "Review discovered paths only within authorized scope. Verify authentication, authorization and data exposure manually.",
                    severity="low",
                    confidence="medium",
                    kind="Review",
                    evidence_type="passive_js_route_extraction",
                    precision_note="Lite reads already referenced same-origin scripts with byte limits. It does not fuzz, execute app flows, bypass auth or send payloads.",
                )
            )

        if sensitive_names:
            findings.append(
                self.finding(
                    "HF-LITE-041",
                    "Sensitive-looking JavaScript identifiers observed",
                    "JavaScript contains variable or property names that look security-relevant. Values are intentionally not extracted or displayed by Lite.",
                    "Same-origin JavaScript bundle analysis",
                    compact_text("Names only: " + " | ".join(sorted(sensitive_names)[:16]), max_len=650),
                    "Manually confirm whether these are harmless names or references to real secrets. Do not report without validating exposure and impact.",
                    severity="info",
                    confidence="medium",
                    kind="Informational",
                    evidence_type="redacted_identifier_observation",
                    precision_note="Only identifier names are reported to reduce false positives and avoid exposing secrets in reports.",
                )
            )

        if storage_markers or external_hosts:
            evidence = []
            if storage_markers:
                evidence.append("Browser storage APIs: " + ", ".join(sorted(storage_markers)))
            if external_hosts:
                evidence.append("External hosts referenced by JS: " + " | ".join(sorted(external_hosts)[:10]))
            findings.append(
                self.finding(
                    "HF-LITE-042",
                    "JavaScript client behavior hints mapped",
                    "Lite observed client-side behavior hints such as browser storage or external hosts. This helps manual review without claiming exploitability.",
                    "Same-origin JavaScript bundle analysis",
                    compact_text("\n".join(evidence), max_len=850),
                    "Review whether storage use and external hosts are expected for the application and target scope.",
                    severity="info",
                    confidence="medium",
                    kind="Informational",
                    evidence_type="passive_js_behavior_hint",
                    precision_note="These are client-side hints only; impact depends on application context and requires manual confirmation.",
                )
            )

        return findings
