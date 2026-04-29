#!/usr/bin/env python3
import json
import os
import re
import ssl
import socket
import time
from datetime import datetime
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

VERSION = "1.6.0-community"
PORT = int(os.environ.get("PORT", "8000"))
MAX_URLS_PER_SESSION = 50
SITE_URL = "https://hexforgeai.dev"
PAYPAL_URL = "https://www.paypal.com/donate/?hosted_button_id=S3335NNBYZXES"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
URLS_SCANNED = set()

TR = {
    "es": {
        "missing_headers": "Faltan cabeceras de seguridad",
        "missing_headers_desc": "La respuesta no incluye una o más cabeceras recomendadas para reducir riesgos comunes del navegador.",
        "mime": "Protección contra MIME sniffing ausente",
        "clickjacking": "Prueba básica de clickjacking",
        "cache": "Revisión de Cache-Control",
        "cors": "CORS permite cualquier origen",
        "server": "Divulgación de tecnología en cabecera Server",
        "powered": "Divulgación de tecnología en X-Powered-By",
        "email": "Correos expuestos en HTML",
        "jwt": "Posible JWT expuesto en HTML",
        "sri": "Subresource Integrity ausente en script externo",
        "mixed": "Referencia HTTP insegura dentro de una página HTTPS",
        "http_links": "Enlaces HTTP inseguros detectados",
        "forms": "Formulario sin protección básica detectado",
        "password": "Campo de contraseña revisado",
        "robots": "Archivo robots.txt revisado",
        "sitemap": "Sitemap revisado",
        "cookies": "Revisión básica de cookies",
        "tls": "Revisión TLS básica",
        "tech": "Fingerprinting básico de tecnologías",
        "comments": "Comentarios HTML encontrados",
        "meta_generator": "Meta generator expuesto",
        "redirect": "Redirección revisada",
        "status": "Código de estado HTTP revisado",
        "content_type": "Tipo de contenido revisado",
        "large_html": "HTML grande detectado",
        "external_scripts": "Scripts externos detectados",
        "inline_scripts": "Scripts inline detectados",
        "iframes": "Iframes detectados",
        "open_graph": "Metadatos Open Graph revisados",
        "canonical": "Canonical URL revisada",
        "location": "Ubicación",
        "recommendation": "Recomendación",
    },
    "en": {}
}
TR["en"] = {
    "missing_headers": "Missing security headers", "missing_headers_desc": "The response does not include one or more recommended browser security headers.", "mime": "MIME sniffing protection missing", "clickjacking": "Basic clickjacking test", "cache": "Cache-Control review", "cors": "CORS allows any origin", "server": "Server technology disclosure", "powered": "X-Powered-By technology disclosure", "email": "Emails exposed in HTML", "jwt": "Possible JWT exposed in HTML", "sri": "Subresource Integrity missing on external script", "mixed": "Insecure HTTP reference inside HTTPS page", "http_links": "Insecure HTTP links detected", "forms": "Form without basic protection detected", "password": "Password field reviewed", "robots": "robots.txt reviewed", "sitemap": "Sitemap reviewed", "cookies": "Basic cookies review", "tls": "Basic TLS review", "tech": "Basic technology fingerprinting", "comments": "HTML comments found", "meta_generator": "Meta generator exposed", "redirect": "Redirect reviewed", "status": "HTTP status code reviewed", "content_type": "Content-Type reviewed", "large_html": "Large HTML detected", "external_scripts": "External scripts detected", "inline_scripts": "Inline scripts detected", "iframes": "Iframes detected", "open_graph": "Open Graph metadata reviewed", "canonical": "Canonical URL reviewed", "location": "Location", "recommendation": "Recommendation"}
TR["pt"] = {k:v for k,v in TR["es"].items()}
TR["zh"] = {k:v for k,v in TR["en"].items()}


def t(lang, key):
    return TR.get(lang, TR["es"]).get(key, TR["es"].get(key, key))


def norm_url(url):
    url = (url or "").strip()
    if not url:
        raise ValueError("URL required")
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    p = urlparse(url)
    if not p.netloc:
        raise ValueError("Invalid URL")
    return url


def fetch_url(url):
    req = Request(url, headers={"User-Agent": "HexForgeSecurityLite/1.6"})
    with urlopen(req, timeout=12) as resp:
        body = resp.read(600000)
        charset = resp.headers.get_content_charset() or "utf-8"
        html = body.decode(charset, errors="replace")
        return resp.geturl(), resp.status, dict(resp.headers.items()), html


def line_for(html, needle):
    idx = html.lower().find(needle.lower())
    if idx < 0:
        return "HTML"
    return "HTML line " + str(html[:idx].count("\n") + 1)


def finding(fid, title, desc, loc, evidence, rec, severity="medium", confidence="medium", kind="Medio"):
    return {"id": fid, "title": title, "description": desc, "location": loc, "evidence": evidence[:900] if isinstance(evidence, str) else evidence, "recommendation": rec, "severity": severity, "confidence": confidence, "kind": kind}


def check_tls(hostname):
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=8) as sock:
            with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                version = ssock.version()
                exp = cert.get("notAfter", "unknown")
                return f"TLS: {version}; certificate expires: {exp}"
    except Exception as e:
        return f"TLS check failed: {e}"


def scan(url, lang="es"):
    url = norm_url(url)
    if url not in URLS_SCANNED and len(URLS_SCANNED) >= MAX_URLS_PER_SESSION:
        return {"ok": False, "error": f"Community limit reached: {MAX_URLS_PER_SESSION} URLs per server session."}
    URLS_SCANNED.add(url)
    final_url, status, headers, html = fetch_url(url)
    h = {k.lower(): v for k, v in headers.items()}
    p = urlparse(final_url)
    host = p.hostname or ""
    out = []

    missing = []
    required = ["content-security-policy", "x-frame-options", "x-content-type-options", "referrer-policy", "permissions-policy"]
    for name in required:
        if name not in h:
            missing.append(name)
    if missing:
        out.append(finding("HF-LITE-001", t(lang,"missing_headers"), t(lang,"missing_headers_desc"), "HTTP response headers", "Missing: " + ", ".join(missing), "Add missing security headers with conservative policies."))
    if h.get("x-content-type-options", "").lower() != "nosniff":
        out.append(finding("HF-LITE-002", t(lang,"mime"), t(lang,"mime"), "HTTP response headers", "X-Content-Type-Options is missing or not nosniff", "Set X-Content-Type-Options: nosniff.", "low", "medium", "Bajo"))
    if "x-frame-options" not in h and "frame-ancestors" not in h.get("content-security-policy", ""):
        out.append(finding("HF-LITE-003", t(lang,"clickjacking"), "Page may be embeddable in an iframe.", "HTTP response headers", "No X-Frame-Options and no CSP frame-ancestors directive", "Set CSP frame-ancestors or X-Frame-Options."))
    cc = h.get("cache-control", "")
    if cc:
        out.append(finding("HF-LITE-004", t(lang,"cache"), "Cache policy was reviewed.", "HTTP response headers", "Cache-Control: " + cc, "Use no-store/private for authenticated or sensitive content.", "info", "medium", "Informativo"))
    if h.get("access-control-allow-origin") == "*":
        out.append(finding("HF-LITE-005", t(lang,"cors"), t(lang,"cors"), "HTTP response headers", "Access-Control-Allow-Origin: *", "Avoid wildcard CORS on sensitive endpoints."))
    if "server" in h:
        out.append(finding("HF-LITE-006", t(lang,"server"), t(lang,"server"), "HTTP response headers", "Server: " + h["server"], "Consider minimizing version disclosure.", "info", "high", "Informativo"))
    if "x-powered-by" in h:
        out.append(finding("HF-LITE-007", t(lang,"powered"), t(lang,"powered"), "HTTP response headers", "X-Powered-By: " + h["x-powered-by"], "Remove X-Powered-By if unnecessary."))
    if status:
        out.append(finding("HF-LITE-008", t(lang,"status"), "HTTP response status was reviewed.", "HTTP response", str(status), "Verify status code is expected.", "info", "high", "Informativo"))
    if "content-type" in h:
        out.append(finding("HF-LITE-009", t(lang,"content_type"), "Content-Type was reviewed.", "HTTP response headers", h["content-type"], "Ensure charset and type are correct.", "info", "high", "Informativo"))
    if final_url != url:
        out.append(finding("HF-LITE-010", t(lang,"redirect"), "Final URL differs from requested URL.", "HTTP redirect", f"{url} -> {final_url}", "Review redirects and HTTPS enforcement.", "info", "medium", "Informativo"))
    if "generator" in html.lower():
        m = re.search(r'<meta[^>]+name=["\']generator["\'][^>]*>', html, re.I)
        if m:
            out.append(finding("HF-LITE-011", t(lang,"meta_generator"), t(lang,"meta_generator"), line_for(html, m.group(0)), m.group(0), "Avoid exposing generator metadata if unnecessary.", "info", "medium", "Informativo"))
    emails = sorted(set(re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', html)))[:8]
    if emails:
        out.append(finding("HF-LITE-012", t(lang,"email"), t(lang,"email"), line_for(html, emails[0]), ", ".join(emails), "Avoid exposing unnecessary internal emails.", "info", "medium", "Informativo"))
    jwts = re.findall(r'eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+', html)[:3]
    if jwts:
        out.append(finding("HF-LITE-013", t(lang,"jwt"), t(lang,"jwt"), line_for(html, jwts[0]), jwts[0], "Do not expose JWTs in client-side HTML.", "high", "medium", "Alto"))
    comments = re.findall(r'<!--(.*?)-->', html, re.S)[:5]
    if comments:
        out.append(finding("HF-LITE-014", t(lang,"comments"), t(lang,"comments"), "HTML comments", " | ".join(c.strip()[:120] for c in comments), "Remove sensitive comments before production.", "info", "medium", "Informativo"))
    scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\'][^>]*>', html, re.I)
    external = [s for s in scripts if s.startswith("http") and urlparse(s).hostname != host]
    if external:
        out.append(finding("HF-LITE-015", t(lang,"external_scripts"), t(lang,"external_scripts"), "HTML scripts", "\n".join(external[:10]), "Review external dependencies.", "info", "medium", "Informativo"))
    no_sri = []
    for tag in re.findall(r'<script[^>]+src=["\']https?://[^"\']+["\'][^>]*>', html, re.I):
        if "integrity=" not in tag.lower():
            no_sri.append(tag)
    if no_sri:
        out.append(finding("HF-LITE-016", t(lang,"sri"), t(lang,"sri"), line_for(html, no_sri[0]), no_sri[0], "Add integrity and crossorigin attributes to trusted external scripts.", "low", "medium", "Bajo"))
    if final_url.startswith("https://") and "http://" in html:
        sample = re.search(r'http://[^"\'\s<>]+', html)
        out.append(finding("HF-LITE-017", t(lang,"mixed"), t(lang,"mixed"), line_for(html, "http://"), sample.group(0) if sample else "http:// reference", "Use HTTPS resources only."))
    http_links = sorted(set(re.findall(r'href=["\'](http://[^"\']+)["\']', html, re.I)))[:10]
    if http_links:
        out.append(finding("HF-LITE-018", t(lang,"http_links"), t(lang,"http_links"), "HTML links", "\n".join(http_links), "Prefer HTTPS links.", "low", "medium", "Bajo"))
    forms = re.findall(r'<form[^>]*>', html, re.I)
    if forms:
        bad = [f for f in forms if "method=" not in f.lower() or "csrf" not in html.lower()]
        if bad:
            out.append(finding("HF-LITE-019", t(lang,"forms"), t(lang,"forms"), line_for(html, bad[0]), bad[0], "Review CSRF protection and form methods."))
    if 'type="password"' in html.lower() or "type='password'" in html.lower():
        out.append(finding("HF-LITE-020", t(lang,"password"), t(lang,"password"), line_for(html, "password"), "Password input present", "Ensure HTTPS, autocomplete policy, and rate limits.", "info", "medium", "Informativo"))
    inline_count = len(re.findall(r'<script(?![^>]+src=)[^>]*>', html, re.I))
    if inline_count:
        out.append(finding("HF-LITE-021", t(lang,"inline_scripts"), t(lang,"inline_scripts"), "HTML scripts", f"Inline script blocks: {inline_count}", "Use CSP nonce/hash policies where possible.", "info", "medium", "Informativo"))
    iframes = re.findall(r'<iframe[^>]*>', html, re.I)[:5]
    if iframes:
        out.append(finding("HF-LITE-022", t(lang,"iframes"), t(lang,"iframes"), line_for(html, iframes[0]), iframes[0], "Review iframe sandboxing and trusted origins."))
    og = re.findall(r'<meta[^>]+property=["\']og:[^>]+>', html, re.I)
    if og:
        out.append(finding("HF-LITE-023", t(lang,"open_graph"), t(lang,"open_graph"), "HTML metadata", f"Open Graph tags: {len(og)}", "Verify public metadata does not leak internal data.", "info", "high", "Informativo"))
    canon = re.findall(r'<link[^>]+rel=["\']canonical["\'][^>]*>', html, re.I)
    if canon:
        out.append(finding("HF-LITE-024", t(lang,"canonical"), t(lang,"canonical"), "HTML metadata", canon[0], "Verify canonical URL is correct.", "info", "high", "Informativo"))
    if final_url.startswith("https://"):
        out.append(finding("HF-LITE-025", t(lang,"tls"), "TLS certificate and protocol were reviewed using a standard secure connection.", "TLS certificate", check_tls(host), "Monitor certificate expiration and disable legacy TLS versions.", "info", "high", "Informativo"))
    tech = []
    for pat, name in [(r"wp-content", "WordPress"), (r"react", "React"), (r"vue", "Vue"), (r"angular", "Angular"), (r"next", "Next.js"), (r"vite", "Vite")]:
        if re.search(pat, html, re.I): tech.append(name)
    if tech:
        out.append(finding("HF-LITE-026", t(lang,"tech"), t(lang,"tech"), "HTML patterns", ", ".join(sorted(set(tech))), "Fingerprinting is informational; verify manually.", "info", "low", "Informativo"))
    if len(html) > 300000:
        out.append(finding("HF-LITE-027", t(lang,"large_html"), t(lang,"large_html"), "HTML body", f"HTML size: {len(html)} bytes", "Large HTML can affect performance and review complexity.", "info", "medium", "Informativo"))
    # robots and sitemap are intentionally lightweight
    for fid, path, key in [("HF-LITE-028","/robots.txt","robots"),("HF-LITE-029","/sitemap.xml","sitemap")]:
        try:
            base = f"{p.scheme}://{p.netloc}"
            req = Request(base + path, headers={"User-Agent": "HexForgeSecurityLite/1.6"})
            with urlopen(req, timeout=5) as r:
                sample = r.read(300).decode("utf-8", errors="replace")
                out.append(finding(fid, t(lang,key), f"{path} exists and was reviewed.", path, sample, "Verify no sensitive paths are exposed.", "info", "medium", "Informativo"))
        except Exception:
            pass
    out.append(finding("HF-LITE-030", "Community scan completed", "30 active community checks executed or evaluated.", "HexForge engine", f"Target: {final_url}; checked at {datetime.utcnow().isoformat()}Z", "Manually validate important findings before reporting.", "info", "high", "Informativo"))
    return {"ok": True, "url": url, "final_url": final_url, "status": status, "headers": headers, "findings": out[:30], "count": len(out[:30]), "limit": MAX_URLS_PER_SESSION, "version": VERSION}


def read_file(path, mode="rb"):
    with open(path, mode) as f:
        return f.read()

class Handler(BaseHTTPRequestHandler):
    def send_bytes(self, data, content_type="application/octet-stream", status=200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            data = read_file(os.path.join(BASE_DIR, "frontend", "static", "index.html"))
            return self.send_bytes(data, "text/html; charset=utf-8")
        if path.startswith("/static/"):
            name = path.split("/static/",1)[1]
            full = os.path.join(BASE_DIR, "frontend", "static", name)
            if not os.path.isfile(full): return self.send_bytes(b"Not found", "text/plain", 404)
            ctype = "text/css" if name.endswith(".css") else "application/javascript" if name.endswith(".js") else "text/plain"
            return self.send_bytes(read_file(full), ctype)
        if path.startswith("/assets/"):
            name = path.split("/assets/",1)[1]
            full = os.path.join(BASE_DIR, "assets", name)
            if not os.path.isfile(full): return self.send_bytes(b"Not found", "text/plain", 404)
            return self.send_bytes(read_file(full), "image/png")
        if path == "/api/status":
            return self.send_bytes(json.dumps({"ok": True, "version": VERSION, "urls_used": len(URLS_SCANNED), "url_limit": MAX_URLS_PER_SESSION}).encode(), "application/json")
        return self.send_bytes(b"Not found", "text/plain", 404)
    def do_POST(self):
        if urlparse(self.path).path != "/api/scan":
            return self.send_bytes(b"Not found", "text/plain", 404)
        length = int(self.headers.get("Content-Length", "0"))
        try:
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            result = scan(data.get("url"), data.get("lang", "es"))
            return self.send_bytes(json.dumps(result, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")
        except Exception as e:
            return self.send_bytes(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8", 400)
    def log_message(self, fmt, *args):
        pass

def main():
    print(f"HexForge Security Lite {VERSION} running at http://0.0.0.0:{PORT}")
    print(f"Open http://localhost:{PORT} or your VM external address on port {PORT}")
    httpd = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    httpd.serve_forever()

if __name__ == "__main__":
    main()
