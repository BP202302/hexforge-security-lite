from __future__ import annotations

import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Dict

from hexforge_lite.engine import ScanEngine


ROUTES: Dict[str, dict] = {}


def route(path: str, *, status: int = 200, headers: dict | None = None, body: str = "") -> None:
    ROUTES[path] = {"status": status, "headers": headers or {}, "body": body}


class LabHandler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        payload = ROUTES.get(self.path)
        if payload is None:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"not found")
            return
        self.send_response(payload["status"])
        for key, value in payload["headers"].items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(payload["body"].encode("utf-8"))

    def log_message(self, fmt, *args):
        return


class HexForgeEngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), LabHandler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join(timeout=5)

    def setUp(self):
        ROUTES.clear()
        self.engine = ScanEngine()
        base_headers = {
            "Content-Type": "text/html; charset=utf-8",
            "Content-Security-Policy": "default-src 'self'; frame-ancestors 'none'",
            "Strict-Transport-Security": "max-age=31536000",
            "X-Content-Type-Options": "nosniff",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "geolocation=()",
        }
        route("/clean", headers=base_headers, body="<html><head><title>ok</title></head><body>Hello</body></html>")
        route("/robots.txt", headers={"Content-Type": "text/plain; charset=utf-8"}, body="User-agent: *\nDisallow:")
        route("/sitemap.xml", headers={"Content-Type": "application/xml; charset=utf-8"}, body="<urlset></urlset>")
        route(
            "/weak",
            headers={
                "Content-Type": "text/html",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": "true",
                "Cache-Control": "public, max-age=3600",
                "Server": "Apache/2.4.57",
                "X-Powered-By": "PHP/8.2",
                "Set-Cookie": "sessionid=abc123; Path=/",
            },
            body=(
                "<html><head>"
                "<meta name='generator' content='WordPress 6.6'>"
                "<link rel='canonical' href='http://lab.local/weak'>"
                "</head><body>"
                "<!-- TODO internal debug key rotation -->"
                "admin@example.com"
                " eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0In0.signature"
                "<script src='https://cdn.example.org/app.js'></script>"
                "<a href='http://cdn.example.org/file.js'>file</a>"
                "<form action='/login'><input type='password' name='password'></form>"
                "</body></html>"
            ),
        )
        route(
            "/http-login",
            headers={"Content-Type": "text/html; charset=utf-8"},
            body="<html><body><form method='post'><input type='password'></form></body></html>",
        )
        route(
            "/comment-clean",
            headers=base_headers,
            body="<html><body><!-- welcome message only --></body></html>",
        )
        route(
            "/sri-good",
            headers=base_headers,
            body="<html><body><script src='https://cdn.example.org/app.js' integrity='sha384-test'></script></body></html>",
        )
        route(
            "/form-good",
            headers=base_headers,
            body="<html><body><form method='post'><input type='text' name='q'></form></body></html>",
        )

    def url(self, path: str, scheme: str = "http") -> str:
        return f"{scheme}://127.0.0.1:{self.port}{path}"

    def test_clean_page_has_no_noise(self):
        report = self.engine.scan(self.url("/clean"))
        titles = {item["title"] for item in report["findings"]}
        self.assertNotIn("Wildcard CORS policy detected", titles)
        self.assertNotIn("Potentially sensitive HTML comments found", titles)
        self.assertNotIn("Generator metadata exposed", titles)

    def test_weak_page_triggers_expected_findings(self):
        report = self.engine.scan(self.url("/weak"))
        titles = {item["title"] for item in report["findings"]}
        expected = {
            "Missing security headers",
            "Page may be embeddable in frames",
            "Wildcard CORS policy detected",
            "Cookie missing security attributes",
            "Potentially sensitive page has weak cache policy",
            "HTML response omits an explicit charset",
            "MIME sniffing protection missing",
            "Generator metadata exposed",
            "Potentially sensitive HTML comments found",
            "Emails exposed in client-side HTML",
            "JWT-like token exposed in HTML",
            "External scripts loaded from third-party origins",
            "External script without Subresource Integrity",
            "Form missing explicit HTTP method",
            "Password field served over HTTP",
        }
        self.assertTrue(expected.issubset(titles))
        self.assertEqual(len(titles), len(report["findings"]))

    def test_http_password_page_is_detected(self):
        report = self.engine.scan(self.url("/http-login"))
        titles = [item["title"] for item in report["findings"]]
        self.assertIn("Password field served over HTTP", titles)

    def test_low_signal_comments_do_not_trigger(self):
        report = self.engine.scan(self.url("/comment-clean"))
        titles = {item["title"] for item in report["findings"]}
        self.assertNotIn("Potentially sensitive HTML comments found", titles)

    def test_sri_present_avoids_false_positive(self):
        report = self.engine.scan(self.url("/sri-good"))
        titles = {item["title"] for item in report["findings"]}
        self.assertNotIn("External script without Subresource Integrity", titles)

    def test_explicit_form_method_avoids_false_positive(self):
        report = self.engine.scan(self.url("/form-good"))
        titles = {item["title"] for item in report["findings"]}
        self.assertNotIn("Form missing explicit HTTP method", titles)

    def test_limit_is_enforced(self):
        engine = ScanEngine()
        route("/limit-base", headers={"Content-Type": "text/html; charset=utf-8"}, body="<html></html>")
        for index in range(50):
            path = f"/limit-{index}"
            route(path, headers={"Content-Type": "text/html; charset=utf-8"}, body=f"<html>{index}</html>")
            engine.scan(self.url(path))
        with self.assertRaises(RuntimeError):
            route("/limit-over", headers={"Content-Type": "text/html; charset=utf-8"}, body="<html>51</html>")
            engine.scan(self.url("/limit-over"))

    def test_health_payload_shape_serializable(self):
        report = self.engine.scan(self.url("/clean"))
        json.dumps(report)
        self.assertTrue(report["ok"])
        self.assertEqual(report["version"], "1.7.0-community")

    def test_controlled_lab_matrix_50_cases(self):
        for index in range(50):
            path = f"/matrix-{index}"
            headers = {"Content-Type": "text/html; charset=utf-8"}
            body = f"<html><body>case {index}</body></html>"
            if index % 5 == 0:
                headers["Access-Control-Allow-Origin"] = "*"
            if index % 7 == 0:
                body = body.replace("</body>", "<!-- TODO internal --> </body>")
            if index % 9 == 0:
                body = body.replace("</body>", "<script src='https://cdn.example.org/a.js'></script></body>")
            if index % 11 == 0:
                body = body.replace("</body>", "<form action='/login'><input type='password'></form></body>")
            route(path, headers=headers, body=body)
            report = self.engine.scan(self.url(path))
            self.assertTrue(report["ok"])
            self.assertIsInstance(report["findings"], list)
            titles = {item["title"] for item in report["findings"]}
            if index % 5 == 0:
                self.assertIn("Wildcard CORS policy detected", titles)
            if index % 7 == 0:
                self.assertIn("Potentially sensitive HTML comments found", titles)
            if index % 9 == 0:
                self.assertIn("External script without Subresource Integrity", titles)
            if index % 11 == 0:
                self.assertIn("Form missing explicit HTTP method", titles)


if __name__ == "__main__":
    unittest.main()
