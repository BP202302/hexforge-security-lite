#!/usr/bin/env python3
from __future__ import annotations

import json
import mimetypes
import time
from collections import defaultdict, deque
from threading import Lock
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from hexforge_lite.config import (
    AUTHOR_EMAIL,
    AUTHOR_NAME,
    BASE_DIR,
    GITHUB_URL,
    MAX_API_BODY_BYTES,
    PAYPAL_URL,
    PORT,
    RATE_LIMIT_MAX_SCANS,
    RATE_LIMIT_WINDOW_SECONDS,
    SITE_URL,
    VERSION,
)
from hexforge_lite.engine import ScanEngine

WEB_DIR = BASE_DIR / "website"
ASSETS_DIR = BASE_DIR / "assets"
ENGINE = ScanEngine()
RATE_LIMIT_BUCKETS = defaultdict(deque)
RATE_LIMIT_LOCK = Lock()


def is_rate_limited(client_ip: str) -> bool:
    now = time.time()
    with RATE_LIMIT_LOCK:
        bucket = RATE_LIMIT_BUCKETS[client_ip]
        while bucket and now - bucket[0] > RATE_LIMIT_WINDOW_SECONDS:
            bucket.popleft()
        if len(bucket) >= RATE_LIMIT_MAX_SCANS:
            return True
        bucket.append(now)
        return False



def read_bytes(path: Path) -> bytes:
    with path.open("rb") as handle:
        return handle.read()


class Handler(BaseHTTPRequestHandler):
    server_version = f"HexForgeSecurityLite/{VERSION}"

    def send_payload(self, payload: bytes, content_type: str, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def route_file(self, relative_path: str) -> None:
        safe_path = relative_path.lstrip("/") or "index.html"
        if safe_path == "scanner":
            safe_path = "scanner.html"
        if safe_path == "results":
            safe_path = "results.html"
        if ".." in Path(safe_path).parts:
            self.send_payload(b"Not found", "text/plain; charset=utf-8", status=404)
            return
        candidate = WEB_DIR / safe_path
        if not candidate.exists() or candidate.is_dir():
            self.send_payload(b"Not found", "text/plain; charset=utf-8", status=404)
            return
        mime, _ = mimetypes.guess_type(str(candidate))
        self.send_payload(read_bytes(candidate), mime or "application/octet-stream")

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            payload = json.dumps(
                {
                    "ok": True,
                    "version": VERSION,
                    "service": "HexForge Security Lite",
                    "site_url": SITE_URL,
                    "github_url": GITHUB_URL,
                    "paypal_url": PAYPAL_URL,
                    "author": AUTHOR_NAME,
                    "email": AUTHOR_EMAIL,
                },
                ensure_ascii=False,
            ).encode("utf-8")
            self.send_payload(payload, "application/json; charset=utf-8")
            return
        if parsed.path.startswith("/assets/"):
            asset_name = parsed.path.replace("/assets/", "")
            asset = ASSETS_DIR / asset_name
            if ".." not in Path(asset_name).parts and asset.exists() and asset.is_file():
                mime, _ = mimetypes.guess_type(str(asset))
                self.send_payload(read_bytes(asset), mime or "application/octet-stream")
                return
        self.route_file(parsed.path)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path != "/api/scan":
            self.send_payload(b"Not found", "text/plain; charset=utf-8", status=404)
            return
        try:
            client_ip = self.client_address[0] if self.client_address else "unknown"
            if is_rate_limited(client_ip):
                self.send_payload(
                    json.dumps(
                        {
                            "ok": False,
                            "error": f"Rate limit exceeded: {RATE_LIMIT_MAX_SCANS} scans per {RATE_LIMIT_WINDOW_SECONDS} seconds.",
                        },
                        ensure_ascii=False,
                    ).encode("utf-8"),
                    "application/json; charset=utf-8",
                    status=429,
                )
                return
            raw_length = int(self.headers.get("Content-Length", "0"))
            if raw_length > MAX_API_BODY_BYTES:
                self.send_payload(
                    json.dumps({"ok": False, "error": "Request body too large."}, ensure_ascii=False).encode("utf-8"),
                    "application/json; charset=utf-8",
                    status=413,
                )
                return
            raw_body = self.rfile.read(raw_length)
            payload = json.loads(raw_body.decode("utf-8")) if raw_body else {}
            result = ENGINE.scan(payload.get("url", ""))
            self.send_payload(json.dumps(result, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")
        except Exception as exc:  # pragma: no cover - integration path
            self.send_payload(
                json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False).encode("utf-8"),
                "application/json; charset=utf-8",
                status=400,
            )

    def log_message(self, fmt: str, *args) -> None:
        return


def main() -> None:
    print(f"HexForge Security Lite {VERSION} running at http://0.0.0.0:{PORT}")
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
