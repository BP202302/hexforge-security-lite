# Modules

HexForge Lite includes focused modules that favor evidence quality over volume.

## Core modules

1. Security headers
2. Clickjacking
3. CORS policy
4. Cookie flags
5. Cache policy
6. Redirect policy
7. Content type
8. Metadata exposure
9. HTML comments
10. Email/token exposure
11. External resources
12. Mixed content
13. Forms basics
14. Client surface mapping
15. Robots/sitemap
16. security.txt
17. HTTP methods safe probe
18. TLS basics
19. Safe Lite plugins

## Dataset-backed modules

These modules use `datasets/` at runtime:

- `security_headers` reads `datasets/headers.json`
- `cors_policy` reads `datasets/cors_patterns.json`
- `RiskScorer` reads `datasets/severity_profiles.json`

## Lite semi-active module

`http_methods` performs a single safe `OPTIONS` request and never sends state-changing methods. It only maps advertised methods and flags sensitive advertised methods as manual review signals.

## Plugins

Plugins are loaded through `hexforge_lite.plugins.load_lite_plugins()`.

A Lite plugin must:

- inherit `BaseModule`
- set `lite_safe = True`
- return structured findings
- use passive evidence only

The example plugin maps public generator metadata when present.

## Validation

All module output goes through validators, deduplication and conservative scoring before reaching the report.
