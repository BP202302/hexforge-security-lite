#!/usr/bin/env python3
from __future__ import annotations

import mimetypes
import time
from collections import defaultdict, deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock
from urllib.parse import urlparse

from api.handlers import error_payload
from api.routes import handle_get, handle_post
from hexforge_lite.config import (
    BASE_DIR,
    MAX_API_BODY_BYTES,
    PORT,
    RATE_LIMIT_MAX_SCANS,
    RATE_LIMIT_WINDOW_SECONDS,
    VERSION,
)

WEB_DIR = BASE_DIR / "website"
ASSETS_DIR = BASE_DIR / "assets"
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
        api_result = handle_get(parsed.path)
        if api_result is not None:
            status, content_type, payload = api_result
            self.send_payload(payload, content_type, status=status)
            return
        if parsed.path.startswith("/assets/"):
            asset_name = parsed.path.replace("/assets/", "", 1)
            asset = ASSETS_DIR / asset_name
            if ".." not in Path(asset_name).parts and asset.exists() and asset.is_file():
                mime, _ = mimetypes.guess_type(str(asset))
                self.send_payload(read_bytes(asset), mime or "application/octet-stream")
                return
        self.route_file(parsed.path)


    def do_OPTIONS(self) -> None:  # noqa: N802
        payload = b""
        self.send_response(204)
        self.send_header("Allow", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/api/scan":
            client_ip = self.client_address[0] if self.client_address else "unknown"
            if is_rate_limited(client_ip):
                self.send_payload(
                    error_payload(
                        f"Rate limit exceeded: {RATE_LIMIT_MAX_SCANS} scans per {RATE_LIMIT_WINDOW_SECONDS} seconds.",
                        code="rate_limited",
                    ),
                    "application/json; charset=utf-8",
                    status=429,
                )
                return
        try:
            raw_length = int(self.headers.get("Content-Length", "0"))
            if raw_length > MAX_API_BODY_BYTES:
                self.send_payload(
                    error_payload("Request body too large.", code="body_too_large"),
                    "application/json; charset=utf-8",
                    status=413,
                )
                return
            raw_body = self.rfile.read(raw_length)
            api_result = handle_post(parsed.path, raw_body)
            if api_result is None:
                self.send_payload(b"Not found", "text/plain; charset=utf-8", status=404)
                return
            status, content_type, payload = api_result
            self.send_payload(payload, content_type, status=status)
        except Exception as exc:  # pragma: no cover - integration path
            self.send_payload(error_payload(str(exc)), "application/json; charset=utf-8", status=400)

    def log_message(self, fmt: str, *args) -> None:
        return


def main() -> None:
    print(f"HexForge Security Lite {VERSION} running at http://0.0.0.0:{PORT}")
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
