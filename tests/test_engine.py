from __future__ import annotations

import unittest
from urllib.parse import urlparse

from hexforge_lite.engine import ScanEngine
from hexforge_lite.models import ScanContext


def ctx(url: str, headers: dict[str, str], html: str = "<html></html>", status: int = 200) -> ScanContext:
    return ScanContext(
        requested_url=url,
        final_url=url,
        status=status,
        headers=headers,
        html=html,
        parsed=urlparse(url),
    )


LAB_PAGES = [
    {
        "name": "strong_headers",
        "url": "https://lab.local/strong",
        "headers": {
            "Content-Security-Policy": "default-src 'self'",
            "X-Content-Type-Options": "nosniff",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "camera=()",
            "Strict-Transport-Security": "max-age=31536000",
        },
        "html": "<html><body>baseline</body></html>",
    },
    {
        "name": "missing_headers",
        "url": "https://lab.local/missing-headers",
        "headers": {"Server": "ExampleServer", "Content-Type": "text/html"},
        "html": "<html><body>missing headers</body></html>",
    },
    {
        "name": "cors_wildcard_no_credentials",
        "url": "https://lab.local/cors-open",
        "headers": {"Access-Control-Allow-Origin": "*", "Content-Type": "text/html"},
        "html": "<html><body>public api doc</body></html>",
    },
    {
        "name": "cors_wildcard_with_credentials",
        "url": "https://lab.local/cors-credentialed",
        "headers": {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials": "true"},
        "html": "<html><body>credentialed content</body></html>",
    },
    {
        "name": "http_password_form",
        "url": "http://lab.local/login",
        "headers": {"Content-Type": "text/html"},
        "html": "<form><input type='password' name='password'></form>",
    },
    {
        "name": "public_discovery_files",
        "url": "https://lab.local/discovery",
        "headers": {"Content-Type": "text/html"},
        "html": "<html><body>normal</body></html>",
        "robots": True,
    },
    {
        "name": "debug_comment",
        "url": "https://lab.local/comment",
        "headers": {"Content-Type": "text/html"},
        "html": "<html><!-- TODO remove internal staging note --></html>",
    },
    {
        "name": "jwt_like_token",
        "url": "https://lab.local/token",
        "headers": {"Content-Type": "text/html"},
        "html": "<script>const t='eyJabc.def.ghi';</script>",
    },
    {
        "name": "mixed_content",
        "url": "https://lab.local/mixed",
        "headers": {"Content-Type": "text/html"},
        "html": "<img src='http://cdn.local/a.png'>",
    },
    {
        "name": "external_resources",
        "url": "https://lab.local/external",
        "headers": {"Content-Type": "text/html"},
        "html": "<script src='https://cdn1.local/a.js'></script><script src='https://cdn2.local/b.js'></script><link href='https://cdn3.local/c.css'>",
    },
    {
        "name": "client_surface_app",
        "url": "https://lab.local/app",
        "headers": {"Content-Type": "text/html"},
        "html": "<html><script src='/app.js'></script><a href='/account'>Account</a></html>",
        "js_body": "fetch('/api/profile'); fetch('/rest/products/search'); const font='/v18/pxiKyp0ihIEF2isQFJXGdg.woff2';",
    },
    {
        "name": "security_txt_present",
        "url": "https://lab.local/security-policy",
        "headers": {"Content-Type": "text/html"},
        "html": "<html><body>security policy test</body></html>",
        "security_txt": "Contact: mailto:security@example.com\nExpires: 2099-01-01T00:00:00Z\nPolicy: https://lab.local/policy",
    },
]


class EnginePrecisionTests(unittest.TestCase):
    def run_case(self, case: dict) -> dict:
        def fake_fetch(url: str):
            return ctx(case["url"], case["headers"], case.get("html", ""))

        def fake_fetch_text(url: str, timeout: int = 5, max_bytes: int = 1200):
            if case.get("robots"):
                return 200, {"Content-Type": "text/plain"}, "User-agent: *\nDisallow: /admin-test"
            if url.endswith("/app.js") and case.get("js_body"):
                return 200, {"Content-Type": "application/javascript"}, case["js_body"]
            if url.endswith("/.well-known/security.txt") and case.get("security_txt"):
                return 200, {"Content-Type": "text/plain"}, case["security_txt"]
            raise RuntimeError("not present")

        import hexforge_lite.engine.scanner as scanner_module
        import hexforge_lite.modules.robots_sitemap as robots_module
        import hexforge_lite.modules.tls as tls_module
        import hexforge_lite.modules.client_surface as client_surface_module
        import hexforge_lite.modules.security_txt as security_txt_module

        original_fetch = scanner_module.fetch_url
        original_fetch_text = robots_module.fetch_text
        original_tls = tls_module.tls_summary
        original_client_surface_fetch_text = client_surface_module.fetch_text
        original_security_txt_fetch_text = security_txt_module.fetch_text
        scanner_module.fetch_url = fake_fetch
        robots_module.fetch_text = fake_fetch_text
        tls_module.tls_summary = lambda hostname: "TLSv1.3; CN=lab.local; certificate expires: future"
        client_surface_module.fetch_text = fake_fetch_text
        security_txt_module.fetch_text = fake_fetch_text
        try:
            return ScanEngine().scan(case["url"])
        finally:
            scanner_module.fetch_url = original_fetch
            robots_module.fetch_text = original_fetch_text
            tls_module.tls_summary = original_tls
            client_surface_module.fetch_text = original_client_surface_fetch_text
            security_txt_module.fetch_text = original_security_txt_fetch_text

    def test_all_10_lab_profiles_return_valid_reports(self):
        for case in LAB_PAGES:
            with self.subTest(case=case["name"]):
                report = self.run_case(case)
                self.assertTrue(report["ok"])
                self.assertEqual(report["version"], "1.8.5-community")
                self.assertIn("summary", report)
                self.assertEqual(len(report["modules"]), 17)
                for finding in report["findings"]:
                    self.assertIn(finding["severity"], {"critical", "high", "medium", "low", "info"})
                    self.assertIn(finding["confidence"], {"high", "medium", "low"})
                    self.assertIn(finding["kind"], {"Confirmed", "Review", "Informational"})
                    self.assertTrue(finding["precision_note"])

    def test_cors_wildcard_without_credentials_is_not_high(self):
        case = LAB_PAGES[2]
        report = self.run_case(case)
        cors = [f for f in report["findings"] if f["module"] == "cors_policy"]
        self.assertTrue(cors)
        self.assertNotEqual(cors[0]["severity"], "high")
        self.assertEqual(cors[0]["kind"], "Review")

    def test_cors_wildcard_with_credentials_can_be_high(self):
        case = LAB_PAGES[3]
        report = self.run_case(case)
        cors = [f for f in report["findings"] if f["module"] == "cors_policy"]
        self.assertTrue(cors)
        self.assertEqual(cors[0]["severity"], "high")
        self.assertEqual(cors[0]["kind"], "Confirmed")

    def test_discovery_files_remain_informational(self):
        report = self.run_case(LAB_PAGES[5])
        discovery = [f for f in report["findings"] if f["module"] == "robots_sitemap"]
        self.assertTrue(discovery)
        self.assertTrue(all(f["severity"] == "info" for f in discovery))

    def test_hsts_is_not_duplicated(self):
        report = self.run_case(LAB_PAGES[1])
        hsts = [f for f in report["findings"] if "hsts" in (f["title"] + f["evidence"]).lower() or "strict-transport-security" in (f["title"] + f["evidence"]).lower()]
        self.assertLessEqual(len(hsts), 1)

    def test_client_surface_maps_api_like_routes(self):
        report = self.run_case(next(case for case in LAB_PAGES if case["name"] == "client_surface_app"))
        surface = [f for f in report["findings"] if f["module"] == "client_surface"]
        self.assertTrue(surface)
        evidence = "\n".join(f["evidence"] for f in surface)
        self.assertIn("/api/profile", evidence)
        self.assertIn("/rest/products/search", evidence)
        self.assertNotIn(".woff2", evidence)
        self.assertTrue(all(".woff2" not in route for route in report.get("surface_map", {}).get("api_routes", [])))

    def test_security_txt_present_is_informational(self):
        report = self.run_case(next(case for case in LAB_PAGES if case["name"] == "security_txt_present"))
        items = [f for f in report["findings"] if f["id"] == "HF-LITE-037"]
        self.assertTrue(items)
        self.assertEqual(items[0]["severity"], "info")
        self.assertEqual(items[0]["kind"], "Informational")
        self.assertIn("Contact:", items[0]["evidence"])


class ServerGuardrailTests(unittest.TestCase):
    def test_rate_limit_allows_then_blocks(self):
        import server
        server.RATE_LIMIT_BUCKETS.clear()
        ip = "203.0.113.10"
        for _ in range(server.RATE_LIMIT_MAX_SCANS):
            self.assertFalse(server.is_rate_limited(ip))
        self.assertTrue(server.is_rate_limited(ip))
        server.RATE_LIMIT_BUCKETS.clear()

    def test_fetch_text_default_is_not_tiny(self):
        from hexforge_lite.config import FETCH_TEXT_MAX_BYTES
        self.assertGreaterEqual(FETCH_TEXT_MAX_BYTES, 100_000)


if __name__ == "__main__":
    unittest.main()
