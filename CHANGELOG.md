# Changelog

## v1.8.5-community

- Fixed a false positive where static font/assets such as `/v18/*.woff2` could be classified as API-like routes.
- Added static asset filtering before API-like endpoint classification.
- Separated static assets from route/API findings in the internal surface map.
- Increased same-origin JavaScript read size safely for better passive endpoint discovery.
- Added a passive `security.txt` module for disclosure-channel discovery, informational only.
- Added API scan rate limiting and request body size guardrails.
- Added tests for rate limiting, fetch size, security.txt and route filtering.
- Kept the v1.8.3 visual interface unchanged.

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
