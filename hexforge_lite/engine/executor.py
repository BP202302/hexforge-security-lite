from __future__ import annotations

from ..fetcher import fetch_url
from ..models import ScanContext
from ..utils.urls import normalize_url


class ScanExecutor:
    def fetch(self, url: str) -> ScanContext:
        return fetch_url(normalize_url(url))
