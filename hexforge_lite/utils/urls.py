from urllib.parse import urlparse, urlunparse


def normalize_url(url: str) -> str:
    candidate = (url or "").strip()

    if not candidate:
        raise ValueError("URL required")

    if not candidate.startswith(("http://", "https://")):
        candidate = "https://" + candidate

    parsed = urlparse(candidate)

    if not parsed.netloc:
        raise ValueError("Invalid URL")

    normalized = parsed._replace(
        fragment="",
        path=parsed.path or "/"
    )

    return urlunparse(normalized)
