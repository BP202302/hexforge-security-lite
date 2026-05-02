# Architecture

HexForge Security Lite is organized around a small passive analysis pipeline.

```text
URL -> fetcher -> modules -> validators -> dedup -> scoring -> output
```

## Core components

- `hexforge_lite/engine/` orchestrates module execution and validation.
- `hexforge_lite/modules/` contains the 16 Lite checks.
- `hexforge_lite/validators/` normalizes findings and reduces false positives.
- `hexforge_lite/scoring/` produces conservative risk scores.
- `website/` contains the product-style Lite interface.

## Design rules

1. Passive by default.
2. No severity inflation without direct evidence.
3. Informational observations must not be presented as confirmed vulnerabilities.
4. Every finding should include evidence and remediation guidance.
