# HexForge Security Lite

> Lightweight, modular, low-noise passive web security analysis for authorized targets.

![HexForge Security](assets/hexforge-logo.png)

**HexForge Security Lite** is the open-source community edition of HexForge Security.
It is built for **defensive review**, **clean evidence**, **safer manual validation**, and **lower false-positive noise**.

Lite is intentionally **not** an offensive framework.
It does **not** brute force, bypass auth, spray payloads, exploit automatically, or run destructive tests.

---

## What Lite is for

HexForge Security Lite helps you quickly answer:

- What defensive headers are missing?
- What passive exposure is visible from the initial response?
- What same-origin routes, forms, and parameters are visible?
- What should be manually reviewed next?
- How strong is the evidence behind each finding?

The goal is simple:

> **Fewer findings, better signal, clearer evidence.**

---

## Core capabilities

### Passive security review

- Security header review
- Browser hardening checks
- Cookie attribute inspection
- CORS policy review
- TLS certificate and protocol summary
- Cache policy review for sensitive markers
- Redirect behavior review
- MIME and content-type review
- Metadata and comment exposure checks
- External resource review
- Mixed-content detection
- Discovery file review (`robots.txt`, `sitemap.xml`, `security.txt`)

### Surface mapping improvements in v1.8.5-community

- Improved **read-only same-origin crawler**
- **Parameter discovery** from visible URLs and forms
- **Form analysis** with action, method and field-name mapping
- **Visual endpoint map** in the results page
- Expanded **client surface extraction** for manual review guidance
- Passive **security.txt** discovery for responsible disclosure contact mapping
- API rate limiting and request body guardrails for the local scanner endpoint

### Report quality layer

- Deduplication
- Conservative severity assignment
- Confidence labels
- Precision notes
- Risk scoring
- Multi-language interface and translated findings

---

## Safety boundaries

HexForge Security Lite is designed with intentional limits.

### Lite does

- Perform **passive** HTTP/TLS analysis
- Read visible HTML, headers and same-origin references
- Map routes, forms and parameters in **read-only** mode
- Support manual review in **authorized** environments

### Lite does not

- Brute force
- Fuzz aggressively
- Submit exploit payloads automatically
- Bypass authentication
- Attempt destructive actions
- Act as an offensive automation tool

---

## Architecture

```text
hexforge-security-lite/
├── hexforge_lite/          # core package
│   ├── engine/             # scanner orchestration
│   ├── modules/            # passive analysis modules
│   ├── validators/         # anti-noise and precision layer
│   ├── scoring/            # risk scoring
│   └── output/             # formatting helpers
├── api/                    # lightweight API handlers
├── cli/                    # CLI entrypoint
├── datasets/               # reference data
├── rules/                  # simple rule definitions
├── docs/                   # architecture and roadmap notes
├── benchmarks/             # controlled lab notes
├── website/                # product-style web UI
├── tests/                  # unit tests
└── scripts/                # self-check and runners
```

---

## Detection model

HexForge Lite uses a conservative pipeline:

1. Normalize the authorized URL.
2. Fetch the target safely.
3. Run 17 focused passive modules.
4. Map visible routes, forms and parameters.
5. Validate findings to reduce noise.
6. Deduplicate overlapping results.
7. Score the final report conservatively.
8. Render evidence, recommendations, confidence and precision notes.

---

## Web interface

The Lite UI is split into a simple product flow:

- **Home** → explains the product and boundaries
- **Scanner** → accepts one authorized target
- **Results** → shows metrics, endpoint map, evidence and recommendations

### Run locally

```bash
python3 -B server.py
```

Open:

```text
http://127.0.0.1:8000/
```

---

## API usage

```bash
curl -X POST http://127.0.0.1:8000/api/scan \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

---

## CLI usage

```bash
python3 -B cli/hexforge.py https://example.com
```

---

## Quality checks

### Run the controlled self-check suite

```bash
python3 -B scripts/self_check.py
```

### Run unit tests

```bash
python3 -B -m unittest discover tests
```

---

## Validation notes

Lite is best validated in:

- your own apps
- staging environments
- internal labs
- OWASP Juice Shop
- DVWA
- WebGoat
- VulnWeb

Use automated scanning only when the environment is authorized.

---

## Multi-language support

The Lite UI includes:

- Spanish
- English
- Portuguese
- Japanese
- Chinese
- Arabic
- Hindi

Interface labels and supported finding translations are rendered in the selected language.

---

## Version

### Current release

**v1.8.5-community**

### Highlights

- Static assets such as `.woff2`, `.css`, `.js`, images and maps are filtered before API-like route classification
- `fetch_text` now uses a larger safe default read size for passive page/script checks
- `/api/scan` includes lightweight rate limiting and request body limits
- New passive `security.txt` module added as informational-only disclosure-channel discovery
- Versioned assets such as `/v18/*.woff2` no longer appear as API endpoints
- Same-origin JavaScript route discovery reads more of each bundle while staying read-only
- PayPal donation link corrected
- Homepage visual structure improved
- Brand/logo layout cleaned up
- Larger centered ambient emblem with side brand panel
- Multi-language finding translation improved
- Improved read-only crawler
- Parameter detection added
- Form surface mapping added
- Visual endpoint map added to results
- README restructured

---

## Support the project

If HexForge Security Lite helps you, you can support development here:

**PayPal**

https://www.paypal.com/donate/?hosted_button_id=S3335NNBYZXES

**Official site**

https://hexforgeai.dev/

**GitHub**

https://github.com/BP202302/hexforge-security-lite

---

## Responsible use

HexForge Security Lite is intended for:

- your own systems
- lab environments
- authorized security testing
- defensive review
- learning and community improvement

Do **not** use it for unauthorized testing.

---

## License and trademark

See:

- `LICENSE`
- `TRADEMARKS.md`

HexForge Security name, logo and branding remain protected project assets.
