from __future__ import annotations

import json

from hexforge_lite.engine import ScanEngine

ENGINE = ScanEngine()


def scan_payload(raw_body: bytes) -> bytes:
    payload = json.loads(raw_body.decode("utf-8")) if raw_body else {}
    result = ENGINE.scan(payload.get("url", ""))
    return json.dumps(result, ensure_ascii=False).encode("utf-8")
