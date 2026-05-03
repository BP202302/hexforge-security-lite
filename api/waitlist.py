from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from hexforge_lite.config import ENABLE_DEMO_WAITLIST, WAITLIST_FILE

EMAIL_RE = re.compile(r"^[^@\s]{1,80}@[^@\s]{1,180}\.[^@\s]{2,24}$")
MAX_FIELD = 180


def _clean(value: Any) -> str:
    return str(value or "").strip()[:MAX_FIELD]


def waitlist_response(payload: dict[str, Any], client_ip: str = "unknown") -> dict[str, Any]:
    if not ENABLE_DEMO_WAITLIST:
        return {"ok": False, "error": "Waitlist is disabled.", "code": "waitlist_disabled"}

    email = _clean(payload.get("email", "")).lower()
    name = _clean(payload.get("name", ""))
    source = _clean(payload.get("source", "demo")) or "demo"
    consent = bool(payload.get("consent"))

    if not EMAIL_RE.match(email):
        return {"ok": False, "error": "Valid email is required.", "code": "invalid_email"}
    if not consent:
        return {"ok": False, "error": "Consent is required to join the Pro waitlist.", "code": "consent_required"}

    record = {
        "email": email,
        "name": name,
        "source": source,
        "client_ip_hint": client_ip,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "purpose": "Notify about HexForge Pro/Specter releases.",
    }
    path = Path(WAITLIST_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    return {
        "ok": True,
        "message": "You are on the HexForge Pro waitlist.",
        "email": email,
    }
