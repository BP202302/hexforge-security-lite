from __future__ import annotations

import re
from urllib.parse import urljoin, urlparse

from .base import BaseModule
from ..models import ScanContext
from ..utils.html import compact_text, html_line_for

FORM_RE = re.compile(r"<form\b(?P<attrs>[^>]*)>(?P<body>.*?)</form>", re.I | re.S)
INPUT_RE = re.compile(r"<(?:input|textarea|select)\b(?P<attrs>[^>]*)>", re.I | re.S)
ATTR_RE = re.compile(r"([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*['\"]([^'\"]*)['\"]")


def _attrs(raw: str) -> dict[str, str]:
    return {key.lower(): value.strip() for key, value in ATTR_RE.findall(raw or "")}


class FormsBasicsModule(BaseModule):
    name = "forms_basics"

    def run(self, context: ScanContext):
        findings = []
        forms: list[dict[str, object]] = []
        missing_method = []

        for index, match in enumerate(FORM_RE.finditer(context.html), start=1):
            attrs = _attrs(match.group("attrs"))
            body = match.group("body")
            method = (attrs.get("method") or "get").lower()
            raw_action = attrs.get("action") or context.final_url
            action = urljoin(context.final_url, raw_action)
            inputs = []
            input_names = []
            for input_match in INPUT_RE.finditer(body):
                input_attrs = _attrs(input_match.group("attrs"))
                input_type = (input_attrs.get("type") or "text").lower()
                input_name = input_attrs.get("name") or "(unnamed)"
                if input_name != "(unnamed)":
                    input_names.append(input_name)
                inputs.append({"type": input_type, "name": input_name})
            forms.append(
                {
                    "index": index,
                    "method": method.upper(),
                    "action": action,
                    "path": urlparse(action).path or "/",
                    "field_count": len(inputs),
                    "fields": inputs[:12],
                }
            )
            if "method" not in attrs:
                missing_method.append(match.group(0)[:240])

        surface_map = context.artifacts.setdefault("surface_map", {})
        if forms:
            surface_map["forms"] = forms[:8]
            names = set(surface_map.get("parameters", []))
            for form in forms:
                for field in form["fields"]:
                    name = field.get("name")
                    if name and name != "(unnamed)":
                        names.add(name)
            surface_map["parameters"] = sorted(names)[:40]

        if missing_method:
            findings.append(
                self.finding(
                    "HF-LITE-025",
                    "Form missing explicit HTTP method",
                    "A form tag does not declare a method attribute.",
                    html_line_for(context.html, missing_method[0]),
                    compact_text(missing_method[0], max_len=240),
                    "Declare explicit GET or POST methods on forms to avoid ambiguous behavior.",
                    severity="low",
                    confidence="high",
                    kind="Low",
                )
            )

        password_field = re.search(r'<input[^>]+type=["\']password["\'][^>]*>', context.html, re.I)
        if password_field and context.final_url.startswith("http://"):
            findings.append(
                self.finding(
                    "HF-LITE-026",
                    "Password field served over HTTP",
                    "The page contains a password input but the target is not using HTTPS.",
                    html_line_for(context.html, password_field.group(0)),
                    f"Password field over HTTP at {context.final_url}",
                    "Serve credential entry points exclusively over HTTPS.",
                    severity="high",
                    confidence="high",
                )
            )

        if forms:
            summary_parts = []
            for form in forms[:5]:
                summary_parts.append(
                    f"{form['method']} {form['path']} · fields={form['field_count']} · "
                    f"names={', '.join(field['name'] for field in form['fields'][:6])}"
                )
            findings.append(
                self.finding(
                    "HF-LITE-036",
                    "Forms surface mapped for manual review",
                    "The page exposes HTML forms and input names that may guide safe manual review. This is informational and not a vulnerability by itself.",
                    "HTML form extraction",
                    "\n".join(summary_parts),
                    "Review visible form actions, methods, and field names to understand the target workflow without submitting data automatically.",
                    severity="info",
                    confidence="high",
                    kind="Informational",
                    evidence_type="passive_form_mapping",
                    precision_note="HexForge Lite only reads visible form markup and does not submit forms, brute force inputs, or attempt bypasses.",
                )
            )

        return findings
