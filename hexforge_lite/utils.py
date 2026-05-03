from urllib.parse import urlparse


def normalize_url(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return ""

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    if not parsed.netloc:
        return url

    scheme = parsed.scheme or "https"
    netloc = parsed.netloc.lower()
    path = parsed.path or ""

    return f"{scheme}://{netloc}{path}"
