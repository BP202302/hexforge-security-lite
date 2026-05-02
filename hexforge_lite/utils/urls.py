from urllib.parse import urlparse, urlunparse


def normalize_url(url: str) -> str:
    candidate = (url or "").strip()
    if not candidate:
        raise ValueError("URL required")
    if not candidate.startswith(("http://", "https://")):
        candidate = f"https://{candidate}"
    parsed = urlparse(candidate)
    if not parsed.netloc:
        raise ValueError("Invalid URL")
    cleaned_path = parsed.path or "/"
    normalized = parsed._replace(fragment="", path=cleaned_path)
    return urlunparse(normalized)
