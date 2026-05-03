# Architecture

HexForge Security Lite is structured as a small product-style scanner rather than a single script.

## Runtime flow

```text
request → api/routes.py → ScanEngine → modules/plugins → validators → scorer → report
```

## Layers

- `server.py` serves the UI and delegates API work to `api/`.
- `api/routes.py` exposes `/health`, `/api/meta` and `/api/scan`.
- `hexforge_lite/engine/scanner.py` orchestrates scanning.
- `hexforge_lite/modules/` contains built-in Lite checks.
- `hexforge_lite/plugins.py` loads opt-in safe plugins.
- `hexforge_lite/datasets.py` loads bundled JSON profiles.
- `hexforge_lite/validators/` reduces noise and prevents severity inflation.
- `hexforge_lite/scoring/` converts validated findings into a conservative score.
- `website/` renders the product UI without requiring a frontend build step.

## Safety model

Lite avoids destructive behavior. The only semi-active check is one `OPTIONS` request used to map advertised HTTP methods. It does not execute state-changing methods or exploit payloads.

## Extension model

New checks can be added as built-in modules or Lite plugins. Built-in modules are preferred for core features. Plugins are preferred for optional passive observations.
