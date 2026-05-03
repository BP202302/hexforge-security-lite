from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from .config import BASE_DIR

DATASETS_DIR = BASE_DIR / "datasets"

_DEFAULTS: dict[str, Any] = {
    "headers": {
        "required": [
            "content-security-policy",
            "x-content-type-options",
            "referrer-policy",
            "permissions-policy",
        ],
        "transport": ["strict-transport-security"],
        "note": "HSTS is evaluated separately to avoid duplicate header findings.",
    },
    "cors_patterns": {
        "wildcard_without_credentials": {
            "severity": "low",
            "kind": "Review",
            "reason": "Wildcard CORS without credentials is a review item, not a confirmed critical issue.",
        },
        "wildcard_with_credentials": {
            "severity": "high",
            "kind": "Confirmed",
            "reason": "Wildcard origin plus credentials is a stronger misconfiguration signal.",
        },
    },
    "severity_profiles": {
        "critical": 3.0,
        "high": 2.4,
        "medium": 1.2,
        "low": 0.45,
        "info": 0.0,
    },
}


@lru_cache(maxsize=8)
def load_dataset(name: str) -> dict[str, Any]:
    """Load a bundled JSON dataset with safe defaults.

    Datasets are intentionally read-only runtime inputs. If a dataset is missing or
    malformed, HexForge Lite falls back to embedded defaults instead of failing a scan.
    """
    path = DATASETS_DIR / f"{name}.json"
    fallback = dict(_DEFAULTS.get(name, {}))
    if not path.exists():
        return fallback
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else fallback
    except Exception:
        return fallback


def headers_dataset() -> dict[str, Any]:
    return load_dataset("headers")


def cors_dataset() -> dict[str, Any]:
    return load_dataset("cors_patterns")


def severity_profile() -> dict[str, float]:
    raw = load_dataset("severity_profiles")
    clean: dict[str, float] = {}
    for key, value in raw.items():
        try:
            clean[str(key)] = float(value)
        except (TypeError, ValueError):
            continue
    return clean or dict(_DEFAULTS["severity_profiles"])
