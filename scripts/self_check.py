#!/usr/bin/env python3
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from urllib.parse import urlparse

from hexforge_lite.engine import ScanEngine
from hexforge_lite.models import ScanContext
import hexforge_lite.engine.scanner as scanner_module
import hexforge_lite.modules.robots_sitemap as robots_module
import hexforge_lite.modules.tls as tls_module
import hexforge_lite.modules.client_surface as client_surface_module
import hexforge_lite.modules.security_txt as security_txt_module
import hexforge_lite.modules.http_methods as http_methods_module
import hexforge_lite.modules.js_surface as js_surface_module

LAB_PAGES = [
    ("strong", "https://lab.local/strong", {"Content-Security-Policy":"default-src 'self'","X-Content-Type-Options":"nosniff","Referrer-Policy":"strict-origin","Permissions-Policy":"camera=()","Strict-Transport-Security":"max-age=31536000"}, "<html></html>", False),
    ("missing", "https://lab.local/missing", {"Server":"ExampleServer","Content-Type":"text/html"}, "<html></html>", False),
    ("cors-open", "https://lab.local/cors-open", {"Access-Control-Allow-Origin":"*","Content-Type":"text/html"}, "<html></html>", False),
    ("cors-creds", "https://lab.local/cors-creds", {"Access-Control-Allow-Origin":"*","Access-Control-Allow-Credentials":"true"}, "<html></html>", False),
    ("http-password", "http://lab.local/login", {"Content-Type":"text/html"}, "<form><input type='password'></form>", False),
    ("robots", "https://lab.local/robots", {"Content-Type":"text/html"}, "<html></html>", True),
    ("comment", "https://lab.local/comment", {"Content-Type":"text/html"}, "<!-- TODO internal debug note -->", False),
    ("token", "https://lab.local/token", {"Content-Type":"text/html"}, "eyJabc.def.ghi", False),
    ("mixed", "https://lab.local/mixed", {"Content-Type":"text/html"}, "<img src='http://cdn.local/a.png'>", False),
    ("external", "https://lab.local/external", {"Content-Type":"text/html"}, "<script src='https://cdn1.local/a.js'></script><script src='https://cdn2.local/b.js'></script><link href='https://cdn3.local/c.css'>", False),
    ("client-surface", "https://lab.local/app", {"Content-Type":"text/html"}, "<script src='/app.js'></script><a href='/account'>Account</a>", False),
    ("security-txt", "https://lab.local/security", {"Content-Type":"text/html"}, "<html></html>", False),
    ("http-methods", "https://lab.local/options", {"Content-Type":"text/html"}, "<html></html>", False),
    ("plugin-generator", "https://lab.local/plugin", {"Content-Type":"text/html"}, "<meta name='generator' content='HexForgeFixture 1.0'>", False),
]

def make_context(url, headers, html):
    return ScanContext(url, url, 200, headers, html, urlparse(url))

def run_case(case):
    name, url, headers, html, robots = case
    def fake_fetch(_url):
        return make_context(url, headers, html)
    def fake_fetch_text(_url, timeout=5, max_bytes=1200):
        if robots:
            return 200, {"Content-Type":"text/plain"}, "User-agent: *\nDisallow: /admin-test"
        if _url.endswith("/app.js"):
            return 200, {"Content-Type":"application/javascript"}, "fetch('/api/profile'); fetch('/rest/products/search'); const font='/v18/pxiKyp0ihIEF2isQFJXGdg.woff2'; const access_token = null; localStorage.setItem('theme','dark');"
        if _url.endswith("/.well-known/security.txt") and name == "security-txt":
            return 200, {"Content-Type":"text/plain"}, "Contact: mailto:security@example.com\nExpires: 2099-01-01T00:00:00Z"
        raise RuntimeError("not present")
    def fake_fetch_method(_url, method="OPTIONS", timeout=5, max_bytes=2048):
        if name == "http-methods":
            return 204, {"Allow":"GET, POST, OPTIONS, TRACE"}, ""
        return 204, {}, ""

    old_fetch, old_text, old_tls, old_client_text, old_security_text, old_methods, old_js_text = scanner_module.fetch_url, robots_module.fetch_text, tls_module.tls_summary, client_surface_module.fetch_text, security_txt_module.fetch_text, http_methods_module.fetch_method, js_surface_module.fetch_text
    scanner_module.fetch_url = fake_fetch
    robots_module.fetch_text = fake_fetch_text
    tls_module.tls_summary = lambda host: "TLSv1.3; CN=lab.local; expires future"
    client_surface_module.fetch_text = fake_fetch_text
    security_txt_module.fetch_text = fake_fetch_text
    http_methods_module.fetch_method = fake_fetch_method
    js_surface_module.fetch_text = fake_fetch_text
    try:
        return ScanEngine().scan(url)
    finally:
        scanner_module.fetch_url = old_fetch
        robots_module.fetch_text = old_text
        tls_module.tls_summary = old_tls
        client_surface_module.fetch_text = old_client_text
        security_txt_module.fetch_text = old_security_text
        http_methods_module.fetch_method = old_methods
        js_surface_module.fetch_text = old_js_text

def assert_true(value, message):
    if not value:
        raise AssertionError(message)

for pass_no in range(1, 4):
    print(f"[HexForge] self-check pass {pass_no}/3", flush=True)
    for case in LAB_PAGES:
        report = run_case(case)
        assert_true(report["ok"], case[0])
        assert_true(report["version"] == "1.9.0-stable", "version mismatch")
        assert_true(len(report["modules"]) >= 20, "module count mismatch")
        for finding in report["findings"]:
            assert_true(finding["kind"] in {"Confirmed","Review","Informational"}, finding)
    cors_open = run_case(LAB_PAGES[2])
    cors = [f for f in cors_open["findings"] if f["module"] == "cors_policy"]
    assert_true(cors and cors[0]["severity"] != "high", "CORS without credentials inflated")
    cors_creds = run_case(LAB_PAGES[3])
    cors = [f for f in cors_creds["findings"] if f["module"] == "cors_policy"]
    assert_true(cors and cors[0]["severity"] == "high", "CORS with credentials not high")
    discovery = run_case(LAB_PAGES[5])
    assert_true(all(f["severity"] == "info" for f in discovery["findings"] if f["module"] == "robots_sitemap"), "discovery inflated")

    client_surface = run_case(LAB_PAGES[10])
    api_routes = client_surface.get("surface_map", {}).get("api_routes", [])
    evidence = "\n".join(f.get("evidence", "") for f in client_surface.get("findings", []) if f.get("module") == "client_surface")
    assert_true("/api/profile" in evidence and "/rest/products/search" in evidence, "API-like routes not detected")
    assert_true(all(".woff2" not in route for route in api_routes), "static font asset classified as API route")
    assert_true(any(f["id"] == "HF-LITE-040" for f in client_surface["findings"]), "JS surface analyzer finding missing")
    security_report = run_case(LAB_PAGES[11])
    assert_true(any(f["id"] == "HF-LITE-037" and f["severity"] == "info" for f in security_report["findings"]), "security.txt informational finding missing")
    method_report = run_case(LAB_PAGES[12])
    assert_true(any(f["id"] == "HF-LITE-039" for f in method_report["findings"]), "HTTP method review finding missing")
    plugin_report = run_case(LAB_PAGES[13])
    assert_true(any(f["id"] == "HF-PLUGIN-001" for f in plugin_report["findings"]), "safe plugin finding missing")
print("[HexForge] self-check complete: 14 lab profiles passed x3", flush=True)
os._exit(0)
