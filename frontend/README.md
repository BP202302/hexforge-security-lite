# Frontend notes

The community UI is served from `website/` with plain HTML, CSS and JavaScript to keep Lite easy to run on small servers and free hosting.

## Current pages

- `website/index.html` — landing/product page
- `website/scanner.html` — scan form
- `website/results.html` — report shell
- `website/results.js` — API calls, translated report rendering and endpoint map rendering
- `website/i18n.js` — UI translations
- `website/static.css` — visual system

## Live demo

```text
https://hexforge-security-lite.onrender.com
```

## Design rule

The frontend should stay lightweight:

- no build step required
- no bundled framework
- no tracking scripts
- no hidden external dependencies
- no feature that changes the Lite safety boundary

## Future frontend upgrades

Good future additions:

- downloadable JSON report button
- copy-to-clipboard finding evidence
- endpoint map filtering
- module enable/disable toggles for local runs
- visual distinction between API-like routes, pages, scripts and static assets

Keep advanced dashboards, authentication, teams, projects and historical scans for Pro editions.
