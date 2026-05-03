import re
from html import unescape


def html_line_for(html: str, needle: str) -> str:
    if not needle:
        return "HTML"
    index = html.lower().find(needle.lower())
    if index < 0:
        return "HTML"
    return f"HTML line {html[:index].count(chr(10)) + 1}"


def compact_text(value: str, max_len: int = 160) -> str:
    compact = re.sub(r"\s+", " ", unescape(value or "")).strip()
    return compact[:max_len]


def excerpt(html: str, needle: str, radius: int = 90) -> str:
    if not html or not needle:
        return needle[: radius * 2]
    index = html.lower().find(needle.lower())
    if index < 0:
        return compact_text(needle, max_len=radius * 2)
    start = max(0, index - radius)
    end = min(len(html), index + len(needle) + radius)
    return compact_text(html[start:end], max_len=radius * 2)
