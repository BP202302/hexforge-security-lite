# Changelog

## v1.9.0-stable

- Added Lite-safe JavaScript Surface Analyzer (`HF-LITE-040`, `HF-LITE-041`, `HF-LITE-042`) for endpoint, identifier and browser-storage review hints.
- Added optional hosted-demo waitlist endpoint (`/api/waitlist`) for Pro/Specter notifications with explicit consent.
- Added demo-only homepage waitlist UI that remains hidden outside the hosted demo/local preview.
- Kept Lite boundaries intact: no fuzzing, no brute force, no payload spraying, no auth bypass and no destructive requests.
- Updated versioning to mark this as a Stable Lite release.

## v1.8.7-community

- Added `Dockerfile` for containerized local execution.
- Added `.dockerignore` to keep Docker builds small and clean.
- Ensured `plugins/examples/passive_module_example.py` is a working Lite-safe plugin returning `HF-PLUGIN-001` for public generator metadata.
- Added a GitHub Actions CI badge to the README.
- Added a severity donut chart to the results page using only vanilla HTML/CSS/JS.
- Added one-click JSON report copy in the results page.
- Added animated scan progress feedback to the scanner page.
- Added a homepage "How it works" section with three visual steps.
- Added a subtle animated hacker/gamer background scene to the homepage only.
- Updated Lite feature wording so basic API access reflects `/api/scan` and `/api/meta`.
- Kept the existing dark hacker visual design intact.

## v1.8.6-community

- Connected `datasets/` to runtime logic through `hexforge_lite/datasets.py`.
- Security headers, CORS policy and risk scoring now consume bundled JSON datasets.
- Added safe Lite plugin loader in `hexforge_lite/plugins.py`.
- Reworked `api/routes.py` and `api/handlers.py` so the server uses them directly.
- Added `/api/meta` for runtime visibility into modules, plugins and datasets.
- Added low-impact `OPTIONS` method review module.
- Added low-confidence POST form anti-CSRF marker review without claiming exploitability.
- Expanded `frontend/README.md` and plugin documentation.
- Rebuilt README with live demo, architecture, safety boundaries and API usage.
- Added live demo URL: `https://hexforge-security-lite.onrender.com`.

## v1.8.5-community

- Fixed static asset false positives in API-like route classification.
- Added static asset filtering before endpoint classification.
- Added passive `security.txt` module for disclosure-channel discovery, informational only.
- Added API scan rate limiting and request body size guardrails.
- Added tests for rate limiting, fetch size, security.txt and route filtering.

## v1.8.3-community

- Corrected the PayPal donation URL and wired it consistently across the website.
- Reworked the homepage brand layout so the subtle large emblem stays centered and the solid logo sits cleanly in the side panel.
- Improved multilingual rendering so translated findings are shown more consistently in the selected language.
- Added a read-only same-origin crawler expansion for Lite surface discovery.
- Added passive parameter discovery from visible URLs and forms.
- Added passive form surface mapping with action, method and field-name summaries.
- Added a visual endpoint map to the results page.
- Restructured the README to match the product-oriented Lite presentation.
- Kept Lite boundaries intact: no brute force, no exploit automation and no intrusive testing.

## v1.8.2-community

- Added multi-language Lite interface: Spanish, English, Portuguese, Japanese, Chinese, Arabic and Hindi.
- Added language-aware results rendering so report labels and known findings follow the selected language.
- Added passive client-surface mapping for same-origin routes and API-like references without fuzzing or exploitation.
- Improved UI layout with stronger navigation, official website button, richer visual sections and subtle HexForge logo watermark.
- Kept Lite boundaries: no brute force, no exploit automation, no payload fuzzing and no intrusive testing.
- Expanded controlled self-check coverage to 11 local lab profiles.

## v1.8.1-community

- Reworked Lite UI into a cleaner product-style experience.
- Replaced confusing PayPal support copy with clearer project-support wording.
- Formatted HTML, CSS and JavaScript so the repository is readable.
- Added stricter mixed-content filtering for W3C namespace/schema URLs.
- Reduced cache-policy false positives on public pages.
- Made clickjacking findings more conservative and manual-validation oriented.
- Improved cookie severity logic to avoid inflating non-session cookies.

## v1.8.0-community

- Added product-style repository structure.
- Added risk scoring, confidence, precision notes and controlled self-checks.
- Improved validators for CORS, discovery files and duplicated findings.
