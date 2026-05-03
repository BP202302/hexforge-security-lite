from __future__ import annotations

import json
from typing import Any


def json_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


def error_payload(message: str, *, code: str = "bad_request") -> bytes:
    return json_bytes({"ok": False, "error": message, "code": code})


def parse_json_body(raw_body: bytes) -> dict[str, Any]:
    if not raw_body:
        return {}
    payload = json.loads(raw_body.decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("JSON body must be an object.")
    return payload
