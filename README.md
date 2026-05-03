<div align="center">

```
██╗  ██╗███████╗██╗  ██╗███████╗ ██████╗ ██████╗  ██████╗ ███████╗
██║  ██║██╔════╝╚██╗██╔╝██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
███████║█████╗   ╚███╔╝ █████╗  ██║   ██║██████╔╝██║  ███╗█████╗  
██╔══██║██╔══╝   ██╔██╗ ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝  
██║  ██║███████╗██╔╝ ██╗██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
```

### `SECURITY · LITE · v1.9.0-stable`

**Low-noise. Evidence-first. Defensively sharp.**

[![CI](https://github.com/BP202302/hexforge-security-lite/actions/workflows/ci.yml/badge.svg)](https://github.com/BP202302/hexforge-security-lite/actions/workflows/ci.yml)
![Status](https://img.shields.io/badge/status-stable-00ff88?style=flat-square)
![Lang](https://img.shields.io/badge/python-3.x-cyan?style=flat-square)
![License](https://img.shields.io/badge/license-see%20LICENSE-blue?style=flat-square)

<br>

[**→ Live Demo**](https://hexforge-security-lite.onrender.com) · [**→ Official Site**](https://hexforgeai.dev/) · [**→ GitHub**](https://github.com/BP202302/hexforge-security-lite) · [**→ Support**](https://www.paypal.com/donate/?hosted_button_id=S3335NNBYZXES)

</div>

-----

## ░░ WHAT IS THIS

> Most free web scanners are noise machines or blunt hammers.
> HexForge Lite is neither.

Built for a different lane — **map clearly, report only what can be evidenced, guide safe manual review without inflating risk.**

Not a replacement for manual testing. A force multiplier for the first phase.

-----

## ░░ QUICK START

### Docker

```bash
docker build -t hexforge-security-lite .
docker run --rm -p 8000:8000 hexforge-security-lite
```

```
→ open http://127.0.0.1:8000
```

### Local

```bash
python3 -B server.py
```

```
→ open http://127.0.0.1:8000
```

### No install — try now

```
https://hexforge-security-lite.onrender.com
```

> ⚠️ Authorized targets only. Labs, your own systems, explicit scope.

-----

## ░░ WHAT MAKES IT DIFFERENT

```
◆  LOW-NOISE FINDINGS      Conservative severity · confidence labels · precision notes
◆  VISUAL ENDPOINT MAP     Routes · API paths · params · forms · scripts · HTTP methods  
◆  SAFE LITE PLUGINS       Opt-in passive plugins wired into the real scan pipeline
◆  DATASETS AT RUNTIME     Headers · CORS patterns · severity profiles — not decorative
◆  API THAT WORKS          /api/scan · /api/meta · /health — actually wired
◆  SEMI-ACTIVE CONTROL     One safe OPTIONS probe. Maps methods. Zero mutation.
◆  INTERNATIONAL UI        ES · EN · PT · JA · ZH · AR · HI
```

-----

## ░░ SAFETY BOUNDARY

<table>
<tr>
<td width="50%">

### ✅ LITE DOES

- Passive HTTP / TLS analysis
- Read visible HTML, headers, client refs
- Map routes, params, forms, scripts (read-only)
- One safe `OPTIONS` probe
- Load local `lite_safe = True` plugins
- Support authorized recon & bug bounty

</td>
<td width="50%">

### ❌ LITE DOES NOT

- Brute force
- Fuzz aggressively
- Submit exploit payloads
- Bypass authentication
- Execute destructive requests
- Claim exploitability without proof

</td>
</tr>
</table>

-----

## ░░ DETECTION PIPELINE

```
[1] Normalize authorized target URL
[2] Fetch initial response — safely
[3] Run focused modules
[4] Execute Lite-safe plugins
[5] Map visible client surface
[6] Single safe HTTP method probe
[7] Validate + deduplicate findings
[8] Score conservatively
[9] Render evidence · confidence · precision notes
```

-----

## ░░ BUILT-IN MODULES

```
security headers          clickjacking protection     CORS policy
cookie flags              cache policy                redirect policy
content type              metadata exposure           HTML comments
email/token exposure      external resources          mixed content
forms basics              client surface mapping      JS surface analyzer
robots/sitemap            security.txt                HTTP methods probe
TLS basics                safe Lite plugins
```

-----

## ░░ ARCHITECTURE

```
hexforge-security-lite/
├── hexforge_lite/
│   ├── engine/          ← scan orchestration
│   ├── modules/         ← passive + Lite-safe modules
│   ├── validators/      ← anti-noise validation layer
│   ├── scoring/         ← conservative risk scoring
│   ├── output/          ← report ordering/formatting
│   ├── datasets.py      ← runtime dataset loader
│   └── plugins.py       ← safe Lite plugin loader
├── api/                 ← routing and handlers
├── cli/                 ← command-line usage
├── datasets/            ← runtime JSON profiles
├── plugins/             ← Lite plugin examples
├── website/             ← product-style UI
└── tests/               ← unit tests
```

-----

## ░░ RUNTIME DATASETS

```bash
datasets/headers.json
datasets/cors_patterns.json
datasets/severity_profiles.json
```

Consumed by `modules.headers` · `modules.cors` · `scoring.risk`
Not decorative. Actually running.

-----

## ░░ LITE PLUGINS

A plugin must:

```python
class MyPlugin(BaseModule):
    lite_safe = True   # ← required

    def run(self):
        # passive only. read-only. structured findings.
        ...
```

Load from `plugins/examples/` — disable with:

```bash
HEXFORGE_ENABLE_PLUGINS=0 python3 server.py
```

-----

## ░░ API

```bash
# Health
curl http://127.0.0.1:8000/health

# Metadata
curl http://127.0.0.1:8000/api/meta

# Scan
curl -X POST http://127.0.0.1:8000/api/scan \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

Rate-limited. Size-limited. Not decorative.

-----

## ░░ CLI

```bash
python3 -B cli/hexforge.py https://example.com
```

-----

## ░░ QUALITY

```bash
python3 -B -m unittest discover tests
python3 -B scripts/self_check.py
```

Self-check validates **14 controlled lab profiles** across **3 passes**.

-----

## ░░ VALIDATED TARGETS

```
✓ your own applications          ✓ staging environments
✓ internal labs                  ✓ OWASP Juice Shop
✓ DVWA                           ✓ WebGoat
✓ VulnWeb
```

> Do not use on systems you don’t own or have explicit authorization for.

-----

## ░░ RELEASE NOTES — v1.9.0

```diff
+ Dockerfile + .dockerignore for clean deployment
+ Working Lite-safe example plugin (HF-PLUGIN-001)
+ Severity donut chart on results page (vanilla HTML/CSS/JS)
+ One-click JSON report copy
+ Animated progress feedback during scan
+ "How it works" section on homepage
+ Subtle animated hacker ambience — no external assets
+ /api/scan and /api/meta documented
+ JS Surface Analyzer — maps client endpoints, redacts sensitive IDs
+ Pro/Specter optional waitlist via /api/waitlist (explicit consent)
```

-----

## ░░ POSITIONING

```
HexForge Lite  →  free · community · accurate surface mapping · conservative evidence
HexForge Pro   →  authenticated workflows · deeper active validation · logic testing
HexForge Specter →  high-scale recon · exploitation chains · role-aware analysis
```

-----

<div align="center">

**HexForge Security Lite** — community edition.

Use it on what you own. Report what you can evidence. Stay in scope.

-----

*HexForge Security name, logo and branding are protected project assets.*
*See `LICENSE` and `TRADEMARKS.md`*

</div>
