from __future__ import annotations

import socket
import ssl
from typing import Dict, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.parse import urlparse

from .config import MAX_BODY_BYTES, REQUEST_TIMEOUT, USER_AGENT
from .models import ScanContext
from .utils.urls import normalize_url


def _decode_body(body: bytes, headers) -> str:
    charset = getattr(headers, "get_content_charset", lambda: None)() or "utf-8"
    return body.decode(charset, errors="replace")


def fetch_url(url: str) -> ScanContext:
    normalized = normalize_url(url)
    request = Request(normalized, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            body = response.read(MAX_BODY_BYTES)
            html = _decode_body(body, response.headers)
            headers = dict(response.headers.items())
            return ScanContext(
                requested_url=normalized,
                final_url=response.geturl(),
                status=getattr(response, "status", 200),
                headers=headers,
                html=html,
                parsed=urlparse(response.geturl()),
            )
    except HTTPError as exc:
        body = exc.read(MAX_BODY_BYTES)
        html = _decode_body(body, exc.headers)
        headers = dict(exc.headers.items())
        return ScanContext(
            requested_url=normalized,
            final_url=exc.geturl() or normalized,
            status=exc.code,
            headers=headers,
            html=html,
            parsed=urlparse(exc.geturl() or normalized),
        )
    except URLError as exc:
        raise RuntimeError(f"Request failed: {exc.reason}") from exc


def fetch_text(url: str, timeout: int = REQUEST_TIMEOUT) -> Tuple[int, Dict[str, str], str]:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:
        body = response.read(1_200)
        text = _decode_body(body, response.headers)
        return getattr(response, "status", 200), dict(response.headers.items()), text


def tls_summary(hostname: str) -> str:
    if not hostname:
        return "TLS check skipped: missing hostname"
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=6) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as wrapped:
                cert = wrapped.getpeercert()
                version = wrapped.version() or "unknown"
                expiry = cert.get("notAfter", "unknown")
                subject = cert.get("subject", [])
                common_names = []
                for item in subject:
                    for key, value in item:
                        if key == "commonName":
                            common_names.append(value)
                subject_text = ", ".join(common_names) if common_names else "unknown"
                return f"TLS {version}; CN={subject_text}; certificate expires: {expiry}"
    except Exception as exc:  # pragma: no cover - network dependent
        return f"TLS check failed: {exc}"
