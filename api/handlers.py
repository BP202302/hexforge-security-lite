from __future__ import annotations

import json


def error_payload(message: str) -> bytes:
    return json.dumps({"ok": False, "error": message}, ensure_ascii=False).encode("utf-8")
