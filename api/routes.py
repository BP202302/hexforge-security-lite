from __future__ import annotations

from typing import Any

from hexforge_lite.config import (
    AUTHOR_EMAIL,
    AUTHOR_NAME,
    ENABLE_LITE_ACTIVE_CHECKS,
    ENABLE_PLUGINS,
    GITHUB_URL,
    PAYPAL_URL,
    SITE_URL,
    VERSION,
    DEMO_URL,
    ENABLE_DEMO_WAITLIST,
)
from hexforge_lite.datasets import cors_dataset, headers_dataset, severity_profile
from hexforge_lite.engine import ScanEngine
from hexforge_lite.plugins import load_lite_plugins

from .handlers import json_bytes, parse_json_body
from .waitlist import waitlist_response

ENGINE = ScanEngine()


def health_payload() -> bytes:
    return json_bytes(
        {
            "ok": True,
            "version": VERSION,
            "service": "HexForge Security Lite",
            "site_url": SITE_URL,
            "live_demo_url": DEMO_URL,
            "github_url": GITHUB_URL,
            "paypal_url": PAYPAL_URL,
            "author": AUTHOR_NAME,
            "email": AUTHOR_EMAIL,
        }
    )


def meta_payload() -> bytes:
    return json_bytes(
        {
            "ok": True,
            "version": VERSION,
            "modules": [module.name for module in ENGINE.modules],
            "datasets": {
                "headers": headers_dataset(),
                "cors_patterns": cors_dataset(),
                "severity_profiles": severity_profile(),
            },
            "plugins_enabled": ENABLE_PLUGINS,
            "loaded_plugins": [module.name for module in load_lite_plugins()],
            "lite_active_checks_enabled": ENABLE_LITE_ACTIVE_CHECKS,
            "waitlist_enabled": ENABLE_DEMO_WAITLIST,
            "live_demo_url": DEMO_URL,
        }
    )


def scan_payload(raw_body: bytes) -> bytes:
    payload = parse_json_body(raw_body)
    result = ENGINE.scan(str(payload.get("url", "")))
    return json_bytes(result)


def waitlist_payload(raw_body: bytes, client_ip: str = "unknown") -> bytes:
    payload = parse_json_body(raw_body)
    return json_bytes(waitlist_response(payload, client_ip=client_ip))


def handle_get(path: str) -> tuple[int, str, bytes] | None:
    if path == "/health":
        return 200, "application/json; charset=utf-8", health_payload()
    if path == "/api/meta":
        return 200, "application/json; charset=utf-8", meta_payload()
    return None


def handle_post(path: str, raw_body: bytes) -> tuple[int, str, bytes] | None:
    if path == "/api/scan":
        return 200, "application/json; charset=utf-8", scan_payload(raw_body)
    if path == "/api/waitlist":
        return 200, "application/json; charset=utf-8", waitlist_payload(raw_body)
    return None
