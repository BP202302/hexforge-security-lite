<div align="center">

# ⚔️ HexForge Security Lite

### Passive Web Security Analysis · Low Noise · Evidence First

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
  <img src="https://img.shields.io/badge/Edition-Lite%20Community-2ECC71?style=flat-square">
  <img src="https://img.shields.io/badge/Mode-Passive%20Analysis-00D4FF?style=flat-square">
  <img src="https://img.shields.io/badge/Focus-Defensive%20Review-8A63FF?style=flat-square">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white">
</p>

<br>

**HexForge Security Lite** is a defensive, passive web security scanner built to turn visible web signals into clear, structured, human-readable findings.

It focuses on **evidence**, **clarity**, and **safe review workflows** instead of noisy aggressive automation.

</div>

---

## 🧭 Navigation

| Section | Description |
|---|---|
| [What is HexForge Lite?](#-what-is-hexforge-security-lite) | Product overview |
| [Live Demo](#-live-demo) | Try the hosted version |
| [Core Philosophy](#-core-philosophy) | Why Lite exists |
| [What It Checks](#-what-it-checks) | Main detection areas |
| [How It Works](#-how-it-works) | Internal workflow |
| [Architecture](#-architecture) | Project structure |
| [Quick Start](#-quick-start) | Run locally |
| [API](#-api) | Programmatic usage |
| [Safety Boundaries](#-safety-boundaries) | What Lite will not do |
| [Roadmap](#-roadmap) | Where the project is going |
| [Support](#-support-the-project) | Help development continue |

---

# 🛡️ What is HexForge Security Lite?

**HexForge Security Lite** is a lightweight web security analysis tool designed for:

- developers
- students
- security learners
- small teams
- blue team workflows
- defensive review
- controlled labs
- portfolio demonstrations
- passive web visibility

It analyzes a target from a **read-only perspective** and produces a structured report with findings, severity, confidence, evidence and recommendations.

The goal is simple:

> **Show what is visible. Explain why it matters. Keep the workflow safe.**

---

# 🚀 Live Demo

You can test the hosted community edition here:

<p align="center">
  <a href="https://hexforge-security-lite.onrender.com">
    <img src="https://img.shields.io/badge/Open%20HexForge%20Lite-Live%20Demo-00D4FF?style=for-the-badge&labelColor=0B1020">
  </a>
</p>

Main routes:

```text
/
 /scanner
 /results
 /health
 /api/meta
 /api/scan
```

Recommended first test target:

```text
https://example.com
```

For security practice labs, you can test with authorized environments such as OWASP Juice Shop or your own deployed applications.

---

# 🧠 Core Philosophy

HexForge Lite is built around a different idea from noisy scanners.

## Signal over noise

Not every observation deserves to become an alarm.  
Lite attempts to keep results readable and review-oriented.

## Evidence before hype

Every finding should answer:

| Question | Purpose |
|---|---|
| What was observed? | Shows the raw security signal |
| Where was it found? | Gives context |
| Why does it matter? | Explains impact |
| What should be reviewed? | Guides next step |
| How confident is it? | Avoids exaggeration |

## Passive before aggressive

The Lite edition is intentionally conservative.  
It is useful without becoming a destructive framework.

---

# 🔍 What It Checks

HexForge Lite focuses on visible web security signals.

## Browser security headers

Reviews common browser-facing protections such as:

- Content-Security-Policy
- Strict-Transport-Security
- Referrer-Policy
- Permissions-Policy
- X-Content-Type-Options
- frame and iframe protection indicators

## HTTP and TLS posture

Observes:

- HTTPS usage
- redirect behavior
- exposed response metadata
- transport-related hints
- configuration gaps visible from the client side

## Cookies and session surface

Checks observable cookie attributes such as:

- Secure
- HttpOnly
- SameSite
- scope and exposure hints

## CORS behavior

Identifies permissive CORS patterns and separates critical signals from review-only observations.

## Client-side surface

Extracts visible references from HTML and scripts:

- routes
- API-like paths
- forms
- parameters
- visible endpoints
- client-referenced paths

## Forms and parameters

Maps visible input surfaces without submitting destructive payloads.

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

---

# 📊 Report Style

HexForge Lite reports are designed to be readable.

A result can include:

| Field | Meaning |
|---|---|
| Severity | Critical, high, medium, low or informational |
| Confidence | How reliable the observation is |
| Evidence | What the scanner actually saw |
| Location | Where the signal appeared |
| Recommendation | What the user should review or improve |
| Precision note | Why the finding should not be overclaimed |

Example finding style:

```text
Finding: Missing browser hardening headers
Severity: Medium
Confidence: High
Location: HTTP response headers
Evidence: Missing Content-Security-Policy, Referrer-Policy, Permissions-Policy
Recommendation: Add browser hardening headers based on application behavior.
Precision: Confirmed from response headers, but final impact depends on application context.
```

---

# 🧱 Architecture

HexForge Lite is organized as a modular Python project.

```text
hexforge-security-lite/
├── api/
│   ├── handlers
│   └── routes
│
├── assets/
│   └── branding and visual resources
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

If your environment uses a different port, check your terminal output.

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

HexForge Lite can include modules for:

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
| Report output | Structured result rendering |

---

# 🧠 Result Interpretation

HexForge Lite findings should be treated as **review guidance**, not automatic proof of exploitation.

A missing header may be important.  
A permissive CORS policy may require more context.  
A visible route may be normal or sensitive depending on the application.  
A client-side endpoint may be expected, internal, deprecated or worth reviewing.

The scanner gives you the signal.  
The analyst decides the final impact.

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

## Lite does not

- brute force
- credential attacks
- destructive exploitation
- unauthorized bypass attempts
- heavy fuzzing
- payload automation against third-party targets
- intrusive vulnerability exploitation

Use only on systems you own, manage, or have explicit permission to review.

---

# 🧭 Use Cases

## Developer review

Check whether a web app exposes basic configuration weaknesses before publishing.

## Security learning

Understand common web security signals through readable evidence.

## Lab analysis

Use with intentionally vulnerable or controlled targets.

## Portfolio project

Show a real security tool with UI, API, reports and deployable architecture.

## Blue team visibility

Perform quick passive review of visible posture and browser-facing configuration.

---

# 🧱 Design Language

HexForge Lite uses a dark, technical interface designed around:

- strong contrast
- report cards
- severity labels
- structured evidence
- readable sections
- visual endpoint mapping
- low-noise presentation

The interface is built to feel like a security console, but still remain understandable.

---

# 🗺️ Roadmap

| Version | Focus |
|---|---|
| v1.9.x | Stabilization, cleanup, documentation and demo polish |
| v2.x | Better reporting, stronger module organization, improved CLI |
| v3.x | More visual mapping, richer exports and better developer workflows |
| Pro track | Separate private/commercial direction |
| Specter track | Advanced premium/enterprise direction |

Lite should remain clean, public and community-friendly.

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

Suggested release naming:

```text
v1.9.1-clean
v1.9.2-stable
v2.0.0-community
```

---

# 🏗️ Product Positioning

HexForge Lite is not just a script.  
It is the public foundation of a larger security product ecosystem.

| Edition | Purpose |
|---|---|
| Lite | Public community edition |
| Pro | Future advanced individual edition |
| Specter | Future premium / enterprise direction |

The Lite repository should stay clean, safe and trustworthy.

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

This project is intended for educational, defensive and authorized security review.

Do not use HexForge Security Lite against systems without permission.

You are responsible for your own usage.

---

<div align="center">

## HexForge Security Lite

### Built for signal. Designed for clarity. Limited for safety.

<p>
  <a href="https://hexforge-security-lite.onrender.com">
    <img src="https://img.shields.io/badge/Open%20Live%20Demo-00D4FF?style=for-the-badge&labelColor=0B1020">
  </a>
  <a href="https://hexforgeai.dev/">
    <img src="https://img.shields.io/badge/Official%20Website-FF7A00?style=for-the-badge&labelColor=0B1020">
  </a>
</p>

</div>
