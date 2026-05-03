from html.parser import HTMLParser


class _LineHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lines = []

    def handle_starttag(self, tag, attrs):
        attrs_text = "".join(f' {name}="{value}"' for name, value in attrs)
        self.lines.append(f"<{tag}{attrs_text}>")

    def handle_endtag(self, tag):
        self.lines.append(f"</{tag}>")

    def handle_data(self, data):
        text = data.strip()
        if text:
            self.lines.append(text)


def html_line_for(html: str, needle: str) -> str:
    html = html or ""
    needle = needle or ""

    if not needle:
        return ""

    for line in html.splitlines():
        if needle in line:
            return line.strip()

    parser = _LineHTMLParser()
    try:
        parser.feed(html)
        for line in parser.lines:
            if needle in line:
                return line.strip()
    except Exception:
        pass

    return ""
