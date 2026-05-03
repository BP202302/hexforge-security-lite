<div align="center">

# HexForge Security Lite

### Low-noise passive security analysis for developers, researchers and blue teams.

<p>
  <img src="assets/logo/hexforge-logo.png" alt="HexForge Security Logo" width="120">
</p>

<p>
  <a href="https://hexforge-security-lite.onrender.com"><img alt="Live Demo" src="https://img.shields.io/badge/Live%20Demo-Open-blue?style=for-the-badge"></a>
  <a href="https://github.com/BP202302/hexforge-security-lite"><img alt="GitHub Repo" src="https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github"></a>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img alt="Version" src="https://img.shields.io/badge/Version-v1.9.0--stable-orange?style=for-the-badge">
  <img alt="Edition" src="https://img.shields.io/badge/Edition-Community-green?style=for-the-badge">
</p>

<p>
  <a href="#-overview">Overview</a> •
  <a href="#-screenshots">Screenshots</a> •
  <a href="#-key-capabilities">Capabilities</a> •
  <a href="#-how-it-works">How it Works</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-api">API</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-safety-boundaries">Safety</a> •
  <a href="#-support-the-project">Support</a>
</p>

</div>

---

## Overview

**HexForge Security Lite** is a **community edition passive security analysis platform** built to generate **signal instead of noise**.

It helps you inspect web targets through **safe, read-only, evidence-first analysis**, focusing on:

- HTTP security headers
- TLS and transport clues
- cookies and browser-facing configuration
- surface mapping
- client-side referenced API routes
- forms and parameters
- passive findings with explanations and recommendations
- multilingual presentation and readable reports

> HexForge Lite is not designed to be a destructive offensive framework.  
> It is designed to help users **observe, map, validate and review**.

---

## Why HexForge Lite?

Most tools either:
- overwhelm the user with raw noise,
- behave too aggressively,
- or require a heavyweight stack for basic visibility.

HexForge Lite aims to be different:

- **Low-noise**
- **Passive by design**
- **Readable evidence**
- **Human-friendly recommendations**
- **Community edition ready**
- **Fast to deploy**
- **Simple to test**
- **Useful for demos, labs and learning**

---

## Screenshots

### 1) Analysis report overview
A clean summary showing risk score, total findings, confidence and passive analysis context.

<p align="center">
  <img src="screenshots/report-overview.png" alt="HexForge report overview" width="100%">
</p>

---

### 2) Evidence and recommendations
Each finding includes context, evidence, recommendation and precision notes.

<p align="center">
  <img src="screenshots/evidence-recommendations.png" alt="HexForge evidence and recommendations" width="100%">
</p>

---

### 3) Community workflow and philosophy
The platform is built around a clear flow: **scan → map → validate → decide**.

<p align="center">
  <img src="screenshots/workflow-community.png" alt="HexForge workflow and community edition" width="100%">
</p>

---

## Key Capabilities

### Passive analysis engine
HexForge Lite performs **passive web inspection** and avoids turning the tool into an unsafe attack framework.

### Evidence-first findings
Every finding is built to be understandable, not just listed.

Each result can include:
- title
- severity
- confidence
- location
- evidence
- recommendation
- precision note
- rule ID / internal reference

### Surface mapping
Lite can extract and organize:
- visible routes
- client-referenced API-like paths
- parameters
- forms
- basic surface signals from the target

### Community edition workflow
HexForge Lite is especially useful for:
- labs
- personal learning
- secure demos
- controlled review targets
- documentation and showcase use cases

### Render-friendly deployment
The project can be deployed as a lightweight web service and tested quickly.

---

## Feature Highlights

| Area | What HexForge Lite does |
|------|--------------------------|
| Headers & browser security | Reviews CSP, HSTS, Referrer-Policy, Permissions-Policy, X-Content-Type-Options and related controls |
| Surface mapping | Extracts visible routes, client-side API references, forms and parameters |
| Transport clues | Observes secure transport hints and configuration gaps |
| Evidence quality | Shows readable findings instead of only raw data |
| Reporting | Renders human-friendly result pages |
| Usability | Easy web UI + API style workflow |
| Philosophy | Low-noise, passive, safe-by-design |

---

## How it Works

HexForge Lite follows a simple operational model:

### 1. Normalize target
The tool prepares and normalizes the input URL.

### 2. Safely fetch the target
The platform performs read-only retrieval and collects observable data.

### 3. Map visible surface
Routes, forms, parameters and client-side references are gathered.

### 4. Validate and deduplicate
Signals are checked, grouped and cleaned to reduce repeated noise.

### 5. Render the report
The result is presented in a report made for humans, not just scripts.

---

## Lite Workflow

```text
Normalize URL
      ↓
Safe Retrieval
      ↓
Passive Mapping
      ↓
Validation & Deduplication
      ↓
Readable Evidence Report
```

---

## What Makes It Different?

### Signal over noise
Many scanners generate too much friction for too little clarity.  
HexForge Lite tries to deliver **structured clarity**.

### Readability matters
The report output is designed to help both:
- technical users
- and people who need a quick explanation of what was found

### Safer by design
The Lite edition is intentionally limited to avoid becoming an unsafe offensive tool.

---

## Safety Boundaries

HexForge Lite is built to remain useful **without becoming reckless**.

### Included in Lite
- passive HTTP/TLS inspection
- read-only mapping
- browser security header checks
- discovery of client-side references
- simple, safe surface observation
- report rendering

### Not the goal of Lite
- brute force
- credential attacks
- fuzzing frameworks
- destructive exploitation
- authentication bypass attempts
- payload launching against third-party systems
- “spray and pray” offensive automation

> Always use HexForge Lite only on systems you own or are explicitly authorized to assess.

---

## Quick Start

### Option A — Local run

```bash
git clone https://github.com/BP202302/hexforge-security-lite.git
cd hexforge-security-lite
pip install -r requirements.txt
python3 server.py
```

Then open:

```text
http://127.0.0.1:10000
```

or the configured port in your environment.

---

### Option B — Docker

```bash
docker build -t hexforge-lite .
docker run -p 10000:10000 hexforge-lite
```

---

### Option C — Render deployment
If you deploy on Render, once the service is live, open:

```text
https://hexforge-security-lite.onrender.com
```

---

## Basic Usage

### Web UI
1. Open the app
2. Go to the scanner
3. Enter an authorized target URL
4. Start the scan
5. Review the report, evidence and recommendations

### Typical paths
Depending on your deployed version, useful routes may include:

```text
/
 /scanner
 /results
 /health
 /api/meta
 /api/scan
```

---

## Example Use Cases

HexForge Lite can be useful for:

- reviewing a lab target before deeper analysis
- checking passive security posture of a personal web app
- mapping client-exposed routes and forms
- building demonstration material
- learning basic web security observation
- showing structured security findings to non-specialists

---

## Example Findings

A report may detect issues such as:

- missing browser hardening headers
- missing HSTS on HTTPS targets
- permissive CORS behavior
- exposed client-side API route references
- visible parameters or forms worth review
- transport or browser-facing configuration gaps

Each finding is meant to answer:
- **What was observed?**
- **Where was it observed?**
- **Why does it matter?**
- **What should be reviewed next?**

---

## API

### Health check

```http
GET /health
```

### Metadata

```http
GET /api/meta
```

### Launch scan

```http
POST /api/scan
Content-Type: application/json
```

Example payload:

```json
{
  "target": "https://example.com"
}
```

---

## Architecture

Below is the conceptual architecture of HexForge Security Lite:

```text
User / Browser
      │
      ▼
   Web UI
      │
      ▼
   server.py
      │
      ├── API layer
      ├── Report rendering
      └── Scan orchestration
              │
              ▼
       hexforge_lite/
              │
              ├── engine/
              ├── modules/
              ├── utils/
              ├── validators/
              ├── scoring/
              ├── output/
              ├── config.py
              ├── fetcher.py
              ├── models.py
              └── plugins.py
```

### Architectural philosophy

HexForge Lite is organized to keep the project:

- modular
- explainable
- testable
- lightweight
- demo-friendly
- extensible for future editions

---

## Repository Structure

```text
hexforge-security-lite/
├── api/
├── assets/
├── benchmarks/
├── cli/
├── datasets/
├── docs/
├── examples/
├── frontend/
├── hexforge_lite/
│   ├── engine/
│   ├── modules/
│   ├── output/
│   ├── scoring/
│   ├── utils/
│   ├── validators/
│   ├── __init__.py
│   ├── config.py
│   ├── fetcher.py
│   ├── models.py
│   └── plugins.py
├── scripts/
├── screenshots/
├── tests/
├── website/
├── Dockerfile
├── requirements.txt
├── run.sh
└── server.py
```

---

## Project Principles

HexForge Security Lite follows these principles:

- **clarity before complexity**
- **evidence before hype**
- **passive before aggressive**
- **community access before vendor lock-in**
- **readability before raw volume**
- **clean reporting before dashboard clutter**

---

## Community Edition Positioning

HexForge Lite is the accessible public-facing edition of the HexForge ecosystem.

It is ideal for:
- public repo visibility
- portfolio credibility
- demos
- community adoption
- educational use
- trust building before advanced editions

---

## Planned Evolution

The broader ecosystem can evolve with separate editions such as:

- **HexForge Lite** → community / public / safe passive edition
- **HexForge Pro** → advanced individual workflow edition
- **HexForge Specter** → premium/private/enterprise-grade direction

> Keep advanced commercial functionality outside the Lite public repository.

---

## Recommended README Enhancements for Maximum Credibility

To make this repository look even stronger over time, keep adding:

- real screenshots
- release notes
- changelog entries
- demo links
- known limitations
- roadmap
- test results
- benchmarks
- architecture docs

---

## Known Limitations

HexForge Lite is intentionally constrained.

This means:
- it will not behave like a full offensive platform
- some findings are informational or review-oriented
- deeper verification is often left to authorized manual analysis
- passive evidence does not always prove exploitability

This is not a weakness of the concept.  
It is part of the **Lite edition design philosophy**.

---

## Support the Project

If you want to support the development of HexForge Security Lite, you can add a donation or support link here.

### Example buttons

<p>
  <a href="https://hexforgeai.dev" target="_blank">
    <img alt="Official Site" src="https://img.shields.io/badge/Official%20Site-HexForgeAI.dev-0A66C2?style=for-the-badge">
  </a>
  <a href="https://paypal.me/YOURUSER" target="_blank">
    <img alt="PayPal" src="https://img.shields.io/badge/Support-PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white">
  </a>
  <a href="https://discord.gg/YOURINVITE" target="_blank">
    <img alt="Discord" src="https://img.shields.io/badge/Community-Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white">
  </a>
</p>

> Replace the placeholder links with your real URLs.

---

## Contributing

Contributions are welcome if they align with the Lite philosophy.

Good contribution areas:
- UI improvements
- report readability
- passive checks
- validators
- documentation
- tests
- translations
- bug fixes

---

## Legal & Responsible Use

HexForge Security Lite is provided for educational, defensive and authorized assessment contexts.

You are responsible for how you use this software.  
Do not use it against targets without permission.

---

## Final Message

HexForge Security Lite is not trying to be the loudest tool.  
It is trying to be the **clearest**.

It is built for users who value:
- cleaner reporting
- safer defaults
- visible evidence
- practical results
- and a better bridge between raw signals and real understanding

---

<div align="center">

### HexForge Security Lite — Built for signal, not noise.

<p>
  <a href="https://hexforge-security-lite.onrender.com">Live Demo</a> •
  <a href="https://github.com/BP202302/hexforge-security-lite">Repository</a> •
  <a href="https://hexforgeai.dev">Official Site</a>
</p>

</div>
