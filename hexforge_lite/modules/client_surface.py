from __future__ import annotations

import re
from pathlib import PurePosixPath
from urllib.parse import parse_qsl, urljoin, urlparse

from .base import BaseModule
from ..config import JS_FETCH_MAX_BYTES, ROBOTS_TIMEOUT
from ..fetcher import fetch_text
from ..models import ScanContext
from ..utils.html import compact_text

API_ROUTE_RE = re.compile(
    r"(?P<route>/(?:api|rest|graphql|auth|oauth|login|signin|account|admin|user|users|profile|cart|checkout|orders|search|query|v[1-3](?:/|$))[A-Za-z0-9_./?=&%:-]{0,160})",
    re.I,
)
ROUTE_RE = re.compile(r"(?:href|src|action)=['\"](?P<route>[^'\"]{1,240})['\"]", re.I)
JS_SRC_RE = re.compile(r"<script[^>]+src=['\"](?P<src>[^'\"]+\.js(?:\?[^'\"]*)?)['\"][^>]*>", re.I)

STATIC_ASSET_EXTENSIONS = {
    ".js", ".mjs", ".css", ".map", ".ico", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".avif",
    ".woff", ".woff2", ".ttf", ".otf", ".eot", ".mp4", ".webm", ".mp3", ".wav", ".pdf", ".zip",
    ".gz", ".br", ".wasm", ".json", ".xml",
}
API_PREFIXES = ("/api", "/rest", "/graphql", "/auth", "/oauth", "/v1", "/v2", "/v3")
API_WORDS = ("login", "signin", "account", "admin", "user", "users", "profile", "cart", "checkout", "orders", "search", "query")


def _path_extension(path: str) -> str:
    return PurePosixPath(urlparse(path).path).suffix.lower()


def _is_static_asset_path(path: str) -> bool:
    return _path_extension(path) in STATIC_ASSET_EXTENSIONS


def _is_api_like_path(path: str) -> bool:
    parsed = urlparse(path)
    clean_path = parsed.path or path
    clean_lower = clean_path.lower()
    if _is_static_asset_path(clean_lower):
        return False
    if clean_lower.startswith(API_PREFIXES):
        # Avoid /v18/font.woff2 being interpreted as /v1.
        if re.match(r"^/v\d+", clean_lower) and not re.match(r"^/v[1-3](?:/|$)", clean_lower):
            return False
        return True
    segments = [segment for segment in clean_lower.strip("/").split("/") if segment]
    return any(segment in API_WORDS for segment in segments)


def _same_host(base_host: str, url: str) -> bool:
    parsed = urlparse(url)
    if not parsed.netloc:
        return True
    return (parsed.hostname or "").lower() == base_host.lower()


def _normalize_route(base_url: str, raw: str) -> str | None:
    raw = (raw or "").strip()
    if not raw or raw.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None
    try:
        return urljoin(base_url, raw)
    except Exception:
        return None


def _extract_surface(base_url: str, base_host: str, html: str) -> tuple[set[str], set[str], set[str], set[str], list[str]]:
    routes: set[str] = set()
    api_routes: set[str] = set()
    parameters: set[str] = set()
    assets: set[str] = set()
    scripts: list[str] = []

    for match in ROUTE_RE.finditer(html):
        url = _normalize_route(base_url, match.group("route"))
        if not url or not _same_host(base_host, url):
            continue
        parsed = urlparse(url)
        if parsed.path and _is_static_asset_path(parsed.path):
            assets.add(url)
        else:
            routes.add(url)
            if parsed.path and _is_api_like_path(parsed.path):
                api_routes.add(parsed.path)
        for key, _ in parse_qsl(parsed.query, keep_blank_values=True):
            if key:
                parameters.add(key)

    for match in API_ROUTE_RE.finditer(html):
        api_route = match.group("route")
        if not _is_api_like_path(api_route):
            continue
        api_routes.add(urlparse(api_route).path or api_route)
        parsed = urlparse(api_route)
        for key, _ in parse_qsl(parsed.query, keep_blank_values=True):
            if key:
                parameters.add(key)

    for match in JS_SRC_RE.finditer(html):
        url = _normalize_route(base_url, match.group("src"))
        if url and _same_host(base_host, url):
            scripts.append(url)
            assets.add(url)

    return routes, api_routes, parameters, assets, scripts


class ClientSurfaceModule(BaseModule):
    """Passive client-side surface discovery for Lite."""

    name = "client_surface"

    def _collect_routes(self, context: ScanContext) -> tuple[list[str], list[str], list[str], list[str], list[str], list[str]]:
        base = context.final_url
        routes: set[str] = set()
        api_routes: set[str] = set()
        parameters: set[str] = set()
        assets: set[str] = set()
        scripts: list[str] = []
        crawled_pages: list[str] = []

        root_routes, root_api, root_params, root_assets, root_scripts = _extract_surface(base, context.host, context.html)
        routes.update(root_routes)
        api_routes.update(root_api)
        parameters.update(root_params)
        assets.update(root_assets)
        scripts.extend(root_scripts)

        candidate_pages = []
        for url in sorted(routes):
            parsed = urlparse(url)
            if parsed.path and parsed.path not in ["/", urlparse(base).path] and not _is_static_asset_path(parsed.path):
                candidate_pages.append(url)
        candidate_pages = candidate_pages[:4]

        for page_url in candidate_pages:
            try:
                status, headers, body = fetch_text(page_url, timeout=ROBOTS_TIMEOUT)
            except Exception:
                continue
            content_type = (headers.get("Content-Type") or "").lower()
            if status >= 400 or ("html" not in content_type and not body.lstrip().startswith("<")):
                continue
            crawled_pages.append(page_url)
            nested_routes, nested_api, nested_params, nested_assets, nested_scripts = _extract_surface(page_url, context.host, body)
            routes.update(nested_routes)
            api_routes.update(nested_api)
            parameters.update(nested_params)
            assets.update(nested_assets)
            for script_url in nested_scripts:
                if script_url not in scripts:
                    scripts.append(script_url)

        for script_url in scripts[:4]:
            try:
                status, _, body = fetch_text(script_url, timeout=ROBOTS_TIMEOUT, max_bytes=JS_FETCH_MAX_BYTES)
            except TypeError:
                try:
                    status, _, body = fetch_text(script_url, timeout=ROBOTS_TIMEOUT)
                except Exception:
                    continue
            except Exception:
                continue
            if status >= 400 or not body:
                continue
            for found in API_ROUTE_RE.finditer(body[:JS_FETCH_MAX_BYTES]):
                api_route = found.group("route")
                if not _is_api_like_path(api_route):
                    if _is_static_asset_path(api_route):
                        assets.add(urljoin(base, api_route))
                    continue
                clean_api = urlparse(api_route).path or api_route
                api_routes.add(clean_api)
                for key, _ in parse_qsl(urlparse(api_route).query, keep_blank_values=True):
                    if key:
                        parameters.add(key)

        return (
            sorted(routes)[:30],
            sorted(api_routes)[:40],
            sorted(parameters)[:30],
            sorted(assets)[:40],
            scripts[:6],
            crawled_pages[:4],
        )

    def run(self, context: ScanContext):
        routes, api_routes, parameters, assets, scripts, crawled_pages = self._collect_routes(context)
        findings = []
        surface_map = context.artifacts.setdefault("surface_map", {})
        surface_map.update(
            {
                "routes": routes,
                "api_routes": api_routes,
                "parameters": sorted(set(surface_map.get("parameters", [])) | set(parameters))[:40],
                "assets": assets,
                "scripts": scripts,
                "crawled_pages": crawled_pages,
                "pages_crawled": 1 + len(crawled_pages),
            }
        )

        framework_markers = []
        html_l = context.html.lower()
        for marker, label in [
            ("ng-version", "Angular"),
            ("data-reactroot", "React"),
            ("__next", "Next.js"),
            ("astro", "Astro"),
            ("vite", "Vite"),
            ("webpack", "Webpack"),
        ]:
            if marker in html_l:
                framework_markers.append(label)

        if scripts or framework_markers:
            evidence = []
            if framework_markers:
                evidence.append("Client markers: " + ", ".join(sorted(set(framework_markers))))
            if crawled_pages:
                evidence.append("Read-only crawl pages: " + " | ".join(crawled_pages[:4]))
            if scripts:
                evidence.append("Same-origin scripts: " + " | ".join(scripts[:5]))
            findings.append(
                self.finding(
                    "HF-LITE-031",
                    "Client-side application surface detected",
                    "The page appears to load a client-side application or JavaScript bundles that may contain routes for manual review.",
                    "HTML and same-origin script references",
                    "\n".join(evidence),
                    "Use the extracted surface as a manual review map; do not treat bundle presence as a vulnerability.",
                    severity="info",
                    confidence="high",
                    kind="Informational",
                    evidence_type="passive_surface_map",
                    precision_note="Lite only observes same-origin client assets with a small read-only limit; no fuzzing or exploitation is performed.",
                )
            )

        if api_routes:
            findings.append(
                self.finding(
                    "HF-LITE-032",
                    "API-like routes referenced by the client",
                    "The client response or same-origin scripts reference API-looking paths. This is not a vulnerability, but it identifies where manual review may continue.",
                    "HTML/client bundle route extraction",
                    "\n".join(api_routes[:24]),
                    "Manually verify whether each endpoint is in scope, authenticated as expected, and free of sensitive unauthenticated data exposure.",
                    severity="low",
                    confidence="medium",
                    kind="Review",
                    evidence_type="passive_route_extraction",
                    precision_note="Route discovery is passive. Static assets such as fonts, images, CSS, JavaScript and maps are filtered out before API-like classification.",
                )
            )

        if parameters:
            findings.append(
                self.finding(
                    "HF-LITE-034",
                    "Query and form parameters discovered",
                    "Visible URLs, forms, or client references expose parameter names that can guide safe manual review.",
                    "Passive parameter extraction",
                    compact_text(" | ".join(parameters[:24]), max_len=780),
                    "Review parameter names carefully and validate only within authorized workflows. Parameter discovery alone is not a vulnerability.",
                    severity="info",
                    confidence="medium",
                    kind="Informational",
                    evidence_type="passive_parameter_extraction",
                    precision_note="Parameter names are extracted without sending payloads or mutating requests.",
                )
            )

        if routes and not api_routes:
            findings.append(
                self.finding(
                    "HF-LITE-033",
                    "Same-origin routes mapped for manual review",
                    "The page exposes same-origin links or actions that can help guide a controlled manual review.",
                    "HTML routes",
                    compact_text(" | ".join(routes[:16]), max_len=780),
                    "Use this as a navigation map. Only test assets allowed by the target program or your own lab.",
                    severity="info",
                    confidence="medium",
                    kind="Informational",
                    evidence_type="passive_route_extraction",
                    precision_note="Route mapping is informational and does not claim vulnerability. Static assets are separated from route/API findings.",
                )
            )

        return findings
