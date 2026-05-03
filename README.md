# HexForge Security Lite

[![CI](https://github.com/BP202302/hexforge-security-lite/actions/workflows/ci.yml/badge.svg)](https://github.com/BP202302/hexforge-security-lite/actions/workflows/ci.yml)

<p align="center">
  <img src="assets/hexforge-logo.png" width="180" alt="HexForge Security logo">
</p>

<p align="center">
  <strong>Low-noise defensive web security analysis for authorized targets.</strong><br>
  Evidence-first findings · Visual endpoint map · Safe Lite plugins · Community edition
</p>

<p align="center">
  <a href="https://hexforge-security-lite.onrender.com">Live Demo</a> ·
  <a href="https://hexforgeai.dev/">Official Site</a> ·
  <a href="https://github.com/BP202302/hexforge-security-lite">GitHub</a> ·
  <a href="https://www.paypal.com/donate/?hosted_button_id=S3335NNBYZXES">Support</a>
</p>

---

## Why HexForge Lite exists

Most free web scanners are either noisy scripts or heavy offensive tools. HexForge Security Lite is built for a different lane:

> **map the target clearly, report only what can be evidenced, and guide safe manual review without inflating risk.**

HexForge Lite is not designed to replace manual testing. It is designed to make the first phase of authorized review cleaner, faster and more professional.

---


## Docker quick start

Run HexForge Lite in a container:

```bash
docker build -t hexforge-security-lite .
docker run --rm -p 8000:8000 hexforge-security-lite
```

Then open:

```text
http://127.0.0.1:8000
```

## Try it without installing

You can use the hosted community demo here:

```text
https://hexforge-security-lite.onrender.com
```

Use it only on targets you own, labs, or systems where you have explicit authorization.

---

## What makes it different

- **Low-noise findings** — conservative severity, confidence labels and precision notes.
- **Visual endpoint map** — routes, API-like paths, parameters, forms, scripts and HTTP methods.
- **Safe Lite plugin system** — opt-in passive plugins loaded into the real scan pipeline.
- **Datasets connected to runtime** — headers, CORS patterns and severity profiles are read by the engine.
- **API that is not decorative** — `/api/scan`, `/api/meta` and `/health` are wired through route handlers.
- **Controlled semi-active checks** — a single safe `OPTIONS` probe maps advertised HTTP methods without mutation.
- **International UI** — Spanish, English, Portuguese, Japanese, Chinese, Arabic and Hindi.

---

## Safety boundaries

HexForge Lite is intentionally limited.

### Lite does

- Perform passive HTTP/TLS analysis.
- Read visible HTML, headers and same-origin client references.
- Map routes, parameters, forms and scripts in read-only mode.
- Send one safe `OPTIONS` request to observe allowed methods.
- Load local plugins only when they explicitly declare `lite_safe = True`.
- Support authorized manual review and bug bounty reconnaissance.

### Lite does not

- Brute force.
- Fuzz aggressively.
- Submit exploit payloads automatically.
- Bypass authentication.
- Execute destructive or state-changing requests.
- Claim exploitability without proof.

---

## Current release

**v1.9.0-stable**

### Release highlights

- Dockerfile and `.dockerignore` added for cleaner execution and deployment.
- Working Lite-safe example plugin returns `HF-PLUGIN-001` for public generator metadata.
- Results page includes a vanilla HTML/CSS/JS severity donut chart.
- Results page includes one-click JSON report copy.
- Scanner page shows animated progress feedback during analysis.
- Homepage includes a simple three-step "How it works" section.
- Homepage includes a subtle animated hacker/gamer ambience without external assets.
- Basic API access is documented for `/api/scan` and `/api/meta`.
- JavaScript Surface Analyzer maps reviewable client endpoints, redacted sensitive-looking identifiers and browser-storage hints without executing attacks.
- Hosted demo includes an optional Pro/Specter waitlist (`/api/waitlist`) with explicit consent; Lite remains usable without login.

---

## Architecture

```text
hexforge-security-lite/
├── hexforge_lite/                # core package
│   ├── engine/                   # scan orchestration
│   ├── modules/                  # passive and Lite-safe modules
│   ├── validators/               # anti-noise validation layer
│   ├── scoring/                  # conservative risk scoring
│   ├── output/                   # report ordering/formatting
│   ├── datasets.py               # runtime dataset loader
│   └── plugins.py                # safe Lite plugin loader
├── api/                          # API routing and handlers
├── cli/                          # command-line usage
├── datasets/                     # runtime JSON profiles
├── docs/                         # architecture, modules, validation, scoring
├── benchmarks/                   # controlled lab notes
├── lab/                          # local test scenarios
├── plugins/                      # Lite plugin examples
├── website/                      # product-style UI
├── frontend/                     # frontend notes and extension guidance
├── screenshots/                  # visual assets
├── tests/                        # unit tests
└── scripts/                      # self-check and runners
```

---

## Detection pipeline

1. Normalize the authorized target URL.
2. Fetch the initial response safely.
3. Run focused modules.
4. Execute Lite-safe plugins.
5. Map visible client surface.
6. Run a single safe HTTP method probe.
7. Validate and deduplicate findings.
9. Score conservatively.
10. Render evidence, confidence and precision notes.

---

## Built-in modules

- Security headers
- Clickjacking protection
- CORS policy
- Cookie flags
- Cache policy
- Redirect policy
- Content type
- Metadata exposure
- HTML comments
- Email/token exposure
- External resources
- Mixed content
- Forms basics
- Client surface mapping
- JavaScript surface analyzer
- Robots/sitemap
- security.txt
- HTTP methods safe probe
- TLS basics
- Safe Lite plugins

---

## Runtime datasets

The engine reads JSON profiles from `datasets/`:

```text
datasets/headers.json
datasets/cors_patterns.json
datasets/severity_profiles.json
```

These files are not decorative. They are consumed by:

- `hexforge_lite.modules.headers`
- `hexforge_lite.modules.cors`
- `hexforge_lite.scoring.risk`

---

## Lite plugins

Plugins are loaded from:

```text
plugins/examples/
```

A plugin must:

- inherit `BaseModule`
- set `lite_safe = True`
- return structured findings
- stay passive/read-only

Disable plugins:

```bash
HEXFORGE_ENABLE_PLUGINS=0 python3 server.py
```

---

## Run locally

```bash
python3 -B server.py
```

Open:

```text
http://127.0.0.1:8000/
```

---

## API

### Health

```bash
curl http://127.0.0.1:8000/health
```

### Runtime metadata

```bash
curl http://127.0.0.1:8000/api/meta
```

### Scan

```bash
curl -X POST http://127.0.0.1:8000/api/scan \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

`/api/scan` includes request-size limits and lightweight rate limiting.

---

## CLI

```bash
python3 -B cli/hexforge.py https://example.com
```

---

## Quality checks

```bash
python3 -B -m unittest discover tests
python3 -B scripts/self_check.py
```

The self-check validates 14 controlled lab profiles across 3 passes.

---

## Recommended validation targets

Use only where authorized:

- your own applications
- staging environments
- internal labs
- OWASP Juice Shop
- DVWA
- WebGoat
- VulnWeb

---

## Hosted demo waitlist

The hosted demo can show an optional waitlist form for future Pro/Specter updates. It stores explicit opt-in records through:

```text
/api/waitlist
```

This is not required for Lite usage and is hidden outside the hosted demo/local preview.

---

## Project positioning

HexForge Lite is the free community baseline. It focuses on accurate surface mapping and conservative evidence.

Advanced exploitation chains, authenticated workflow analysis, deeper active validation, role-aware logic testing and high-scale recon belong in future paid/pro editions.

---

## Responsible use

Use HexForge Security Lite only on systems you own, labs, or explicitly authorized scopes.

Do not use it for unauthorized testing.

---

## License and trademark

See:

- `LICENSE`
- `TRADEMARKS.md`

HexForge Security name, logo and branding remain protected project assets.
