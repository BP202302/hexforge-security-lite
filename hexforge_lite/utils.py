from urllib.parse import urlparse, urlunparse


def normalize_url(url: str) -> str:
    url = (url or "").strip()

    if not url:
        return ""

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    scheme = parsed.scheme or "https"
    netloc = parsed.netloc.lower()
    path = parsed.path or "/"

    return urlunparse((scheme, netloc, path, "", parsed.query, ""))
