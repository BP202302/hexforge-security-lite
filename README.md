<div align="center">

# ⚔️ HexForge Security Lite

### Passive Web Security Analysis · Evidence-First Reports · Low-Noise Defensive Review

<br>

<p>
  <a href="https://hexforge-security-lite.onrender.com">
    <img src="https://img.shields.io/badge/Live%20Demo-Online-00D4FF?style=for-the-badge&labelColor=0B1020">
  </a>
  <a href="https://hexforgeai.dev/">
    <img src="https://img.shields.io/badge/Official%20Site-HexForgeAI.dev-FF7A00?style=for-the-badge&labelColor=0B1020">
  </a>
  <a href="https://www.paypal.com/donate/?hosted_button_id=S3335NNBYZXES">
    <img src="https://img.shields.io/badge/Support-PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white&labelColor=0B1020">
  </a>
</p>

<p>
  <img src="https://img.shields.io/badge/Version-1.9.0--stable-FFB000?style=flat-square">
  <img src="https://img.shields.io/badge/Edition-Lite%20Source--Available-2ECC71?style=flat-square">
  <img src="https://img.shields.io/badge/Mode-Passive%20Analysis-00D4FF?style=flat-square">
  <img src="https://img.shields.io/badge/Focus-Defensive%20Security-8A63FF?style=flat-square">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white">
</p>

<br>

<table>
<tr>
<td align="center">

**HexForge Security Lite** is a source-available defensive scanner for passive web security analysis.

It transforms visible web signals into structured findings with severity, confidence, evidence, recommendations and human-readable reports.

</td>
</tr>
</table>

<br>

<strong>Built for signal. Designed for clarity. Limited for safety.</strong>

</div>

---

## 🧭 Navigation

| Section | Purpose |
|---|---|
| [Overview](#-overview) | What HexForge Security Lite does |
| [Live Demo](#-live-demo) | Open the hosted Render version |
| [Screenshots](#-screenshots) | Visual proof of the interface and reports |
| [Core Philosophy](#-core-philosophy) | Why the project exists |
| [What It Checks](#-what-it-checks) | Passive security review areas |
| [How It Works](#-how-it-works) | Internal workflow |
| [Report Format](#-report-format) | How findings are presented |
| [Architecture](#-architecture) | Repository and package structure |
| [Quick Start](#-quick-start) | Run locally or with Docker |
| [API](#-api) | Programmatic usage |
| [Testing](#-testing) | Local validation |
| [Safety Boundaries](#-safety-boundaries) | Responsible limits |
| [Roadmap](#-roadmap) | Future direction |
| [Support](#-support-the-project) | Support development |

---

# 🛡️ Overview

**HexForge Security Lite** is a lightweight passive security analysis platform for reviewing visible web security signals.

It helps developers, learners, researchers and defensive teams identify configuration issues and exposed client-side surface without using destructive techniques.

The goal is not to generate fear.  
The goal is to generate understanding.

HexForge Lite focuses on:

- clear findings
- visible evidence
- low-noise reports
- safe passive review
- structured recommendations
- readable risk context
- beginner-friendly interpretation
- professional-looking output

---

# 🚀 Live Demo

Open the hosted version:

<p align="center">
  <a href="https://hexforge-security-lite.onrender.com">
    <img src="https://img.shields.io/badge/Open%20HexForge%20Security%20Lite-Live%20Demo-00D4FF?style=for-the-badge&labelColor=0B1020">
  </a>
</p>

Useful routes:

```text
/
 /scanner
 /results
 /health
 /api/meta
 /api/scan
```

Recommended safe target for first testing:

```text
https://example.com
```

Use HexForge Lite only on systems you own, manage, or have explicit permission to review.

---

# 🖼️ Screenshots

## Landing Page

<p align="center">
  <img src="screenshots/landing.png" width="100%" alt="HexForge Security Lite landing page">
</p>

## Scanner Interface

<p align="center">
  <img src="screenshots/scanner.png" width="100%" alt="HexForge Security Lite scanner interface">
</p>

## Report Overview

<p align="center">
  <img src="screenshots/report-overview.png" width="100%" alt="HexForge Security Lite report overview">
</p>

## Evidence and Recommendations

<p align="center">
  <img src="screenshots/evidence-recommendations.png" width="100%" alt="HexForge Security Lite evidence and recommendations">
</p>

---

# 🧠 Core Philosophy

HexForge Security Lite is built around one idea:

> **A useful security tool should explain what it sees, not just throw alerts.**

## Signal over noise

Many scanners produce overwhelming output.  
HexForge Lite is designed to keep findings structured, readable and review-oriented.

## Evidence before hype

Every meaningful finding should answer:

| Question | Why it matters |
|---|---|
| What was observed? | Shows the exact signal |
| Where was it found? | Gives context and location |
| Why does it matter? | Explains the security meaning |
| What should be reviewed? | Provides the next step |
| How confident is it? | Avoids exaggerated claims |

## Passive before aggressive

Lite is intentionally conservative.  
It performs safe, read-only analysis and avoids intrusive behavior.

## Human-readable by design

The output is designed for people, not only machines.  
Findings are written so they can be understood, reviewed and explained.

---

# 🔍 What It Checks

HexForge Lite focuses on visible and passive web security signals.

## Browser security headers

Reviews common browser-facing protections such as:

- Content-Security-Policy
- Strict-Transport-Security
- Referrer-Policy
- Permissions-Policy
- X-Content-Type-Options
- iframe and clickjacking-related protections

## HTTP and HTTPS posture

Observes:

- HTTP status
- HTTPS usage
- redirects
- exposed response metadata
- transport-related clues
- visible configuration gaps

## Cookies

Checks observable cookie attributes:

- Secure
- HttpOnly
- SameSite
- cookie scope
- browser-visible session posture

## CORS

Identifies permissive or review-worthy CORS behavior and presents it with context.

## Client-side surface

Extracts visible client-side references:

- routes
- linked scripts
- API-like paths
- forms
- parameters
- same-origin references
- exposed frontend paths

## Forms and parameters

Maps visible forms and parameters without submitting exploit payloads.

## Discovery and metadata

Depending on the deployed modules, Lite may observe:

- robots.txt
- sitemap.xml
- security.txt
- HTML metadata
- visible comments
- linked resources
- client-exposed hints

---

# 🧬 How It Works

```text
Target URL
   │
   ▼
Normalize URL
   │
   ▼
Safe HTTP Fetch
   │
   ▼
Passive HTML / Header / Surface Review
   │
   ▼
Detection Modules
   │
   ▼
Validation and Deduplication
   │
   ▼
Risk Scoring
   │
   ▼
Human-Readable Report
```

HexForge Lite does not attempt to prove exploitation automatically.  
It collects visible signals and presents them for defensive review.

---

# 📊 Report Format

A HexForge Lite finding can include:

| Field | Meaning |
|---|---|
| Severity | Critical, high, medium, low or informational |
| Confidence | How reliable the observation is |
| Location | Where the signal appeared |
| Evidence | What was actually observed |
| Recommendation | What should be reviewed or improved |
| Precision note | Why the finding should not be exaggerated |
| Rule ID | Internal reference for the finding |

Example:

```text
Finding: Missing browser hardening headers
Severity: Medium
Confidence: High
Location: HTTP response headers
Evidence: Missing Content-Security-Policy, Referrer-Policy and Permissions-Policy
Recommendation: Add browser hardening headers based on application behavior.
Precision: Confirmed from the HTTP response, but final impact depends on application context.
```

---

# 🧱 Architecture

HexForge Security Lite is organized as a modular Python project.

```text
hexforge-security-lite/
├── api/
│   ├── handlers
│   └── routes
│
├── assets/
│   └── branding and visual resources
│
├── benchmarks/
│   └── benchmark material
│
├── cli/
│   └── command line entrypoints
│
├── datasets/
│   └── controlled test and reference data
│
├── docs/
│   └── documentation
│
├── examples/
│   └── usage examples
│
├── frontend/
│   └── frontend resources
│
├── hexforge_lite/
│   ├── engine/
│   ├── modules/
│   ├── output/
│   ├── scoring/
│   ├── utils/
│   ├── validators/
│   ├── config.py
│   ├── fetcher.py
│   ├── models.py
│   └── plugins.py
│
├── lab/
│   └── lab resources
│
├── plugins/
│   └── external or experimental plugin resources
│
├── rules/
│   └── rule references
│
├── screenshots/
│   ├── landing.png
│   ├── scanner.png
│   ├── report-overview.png
│   └── evidence-recommendations.png
│
├── scripts/
│   └── automation and checks
│
├── tests/
│   └── test suite
│
├── website/
│   ├── index.html
│   ├── scanner.html
│   ├── results.html
│   ├── static.css
│   └── i18n.js
│
├── Dockerfile
├── README.md
├── requirements.txt
├── run.sh
└── server.py
```

---

# ⚙️ Quick Start

## Run locally

```bash
git clone https://github.com/BP202302/hexforge-security-lite.git
cd hexforge-security-lite
pip install -r requirements.txt
python3 server.py
```

Open:

```text
http://127.0.0.1:10000
```

If your environment uses a different port, use the port shown in your terminal.

---

## Run with shell script

```bash
chmod +x run.sh
./run.sh
```

---

## Run with Docker

```bash
docker build -t hexforge-security-lite .
docker run -p 10000:10000 hexforge-security-lite
```

Then open:

```text
http://127.0.0.1:10000
```

---

# 🌐 API

## Health check

```http
GET /health
```

## Metadata

```http
GET /api/meta
```

## Scan target

```http
POST /api/scan
Content-Type: application/json
```

Example request:

```json
{
  "target": "https://example.com"
}
```

Example response shape:

```json
{
  "ok": true,
  "version": "1.9.0-stable",
  "target": "https://example.com",
  "findings": [],
  "risk_score": 0
}
```

---

# 🧪 Testing

Run the test suite:

```bash
python3 -B -m unittest discover tests
```

Run self-checks if available:

```bash
python3 -B scripts/self_check.py
```

Recommended before every release:

```bash
python3 -B -m unittest discover tests
python3 -B scripts/self_check.py
```

---

# 🧩 Lite Modules

HexForge Lite can include passive modules for:

| Module Area | Purpose |
|---|---|
| Headers | Browser and HTTP header review |
| TLS / HTTPS | Transport posture observations |
| Cookies | Cookie attribute inspection |
| CORS | Cross-origin policy review |
| Discovery | Visible metadata and discovery files |
| Forms | Passive form mapping |
| Parameters | Query and client-side parameter detection |
| Routes | Visible path extraction |
| API-like references | Client-side endpoint discovery |
| Comments | Passive review of visible HTML comments |
| Metadata | HTML and response metadata review |
| Resources | Linked resource observation |
| Report output | Structured result rendering |

---

# 🧠 Result Interpretation

HexForge Lite findings are **review guidance**, not automatic proof of exploitation.

A missing header may be important.  
A permissive CORS policy may require more context.  
A visible route may be normal or sensitive depending on the application.  
A client-side endpoint may be expected, internal, deprecated or worth reviewing.

The scanner provides the signal.  
The reviewer decides the final impact.

---

# 🔒 Safety Boundaries

HexForge Security Lite is intentionally limited.

## Lite does

- passive fetching
- header analysis
- TLS and HTTP observation
- form discovery
- route discovery
- parameter discovery
- client-side reference mapping
- conservative findings
- readable recommendations
- safe report generation

## Lite does not

- brute force
- credential attacks
- destructive exploitation
- unauthorized bypass attempts
- heavy fuzzing
- exploit chaining
- payload automation against third-party targets
- intrusive vulnerability exploitation

Use only on systems you own, manage, or have explicit permission to review.

---

# 🧭 Use Cases

## Developer review

Check whether a web app exposes visible configuration weaknesses before publishing.

## Security learning

Understand common web security signals through readable evidence.

## Lab analysis

Use with intentionally vulnerable or controlled targets.

## Portfolio project

Show a real security tool with UI, API, reports and deployable architecture.

## Blue team visibility

Perform quick passive review of visible posture and browser-facing configuration.

## Pre-audit preparation

Collect visible findings before deeper authorized manual validation.

---

# 🏗️ Product Positioning

HexForge Lite is the public Lite edition of the HexForge ecosystem.

| Edition | Purpose |
|---|---|
| Lite | Public source-available defensive scanner |
| Pro | Future advanced individual workflow |
| Specter | Future premium or enterprise direction |

The Lite repository should remain:

```text
Clean.
Safe.
Readable.
Public-facing.
Useful.
Non-destructive.
```

Advanced commercial functionality should remain separate from the Lite public repository.

---

# 🗺️ Roadmap

| Version | Focus |
|---|---|
| v1.9.x | Stabilization, cleanup, documentation and demo polish |
| v2.x | Better reports, stronger module organization and improved CLI |
| v3.x | Visual mapping, richer exports and deeper workflow support |
| Pro track | Separate private or commercial direction |
| Specter track | Premium or enterprise direction |

---

# 🧾 Release Checklist

Before publishing a new version:

```text
Run tests
Run self-check
Confirm Render deploy
Confirm /scanner works
Confirm /results works
Confirm README version
Confirm CHANGELOG
Create tag
Create release ZIP
```

Suggested release names:

```text
v1.9.0-stable
v1.9.1-clean
v1.9.2-stable
v2.0.0-lite
```

---

# 💎 Why This Project Matters

Security tools should not only find things.  
They should explain them.

HexForge Lite exists because useful security review needs:

- clear findings
- visible evidence
- safe workflows
- practical recommendations
- controlled scope
- honest severity
- readable reports
- low-noise interpretation

The goal is not to generate fear.  
The goal is to generate understanding.

---

# 🤝 Contributing

Good contribution areas:

- passive modules
- report readability
- translations
- UI polish
- test cases
- documentation
- safer validation logic
- performance improvements
- false positive reduction

Contributions should preserve the Lite philosophy:

```text
Safe.
Passive.
Readable.
Evidence-first.
Low-noise.
```

---

# 💰 Support the Project

If HexForge Security Lite helps you, you can support development here:

<p align="center">
  <a href="https://www.paypal.com/donate/?hosted_button_id=S3335NNBYZXES">
    <img src="https://img.shields.io/badge/Support%20HexForge-PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white&labelColor=0B1020">
  </a>
</p>

Official site:

<p align="center">
  <a href="https://hexforgeai.dev/">
    <img src="https://img.shields.io/badge/Visit-HexForgeAI.dev-FF7A00?style=for-the-badge&labelColor=0B1020">
  </a>
</p>

---

# ⚖️ Responsible Use

HexForge Security Lite is intended for educational, defensive and authorized security review.

Do not use this tool against systems without permission.

You are responsible for your own usage.

---

# 📄 License and Usage

HexForge Security Lite is a source-available Lite edition.

Review the repository license before using, modifying, redistributing or deploying this software.

Commercial use may require explicit permission depending on the license terms.

---

<div align="center">

## HexForge Security Lite

### Built for signal. Designed for clarity. Limited for safety.

<br>

<p>
  <a href="https://hexforge-security-lite.onrender.com">
    <img src="https://img.shields.io/badge/Open%20Live%20Demo-00D4FF?style=for-the-badge&labelColor=0B1020">
  </a>
  <a href="https://hexforgeai.dev/">
    <img src="https://img.shields.io/badge/Official%20Website-FF7A00?style=for-the-badge&labelColor=0B1020">
  </a>
</p>

<br>

**HexForge Security Lite · v1.9.0-stable**

</div>
