# Lite plugins

HexForge Security Lite includes a small **safe plugin loader** so the repository is not just visually extensible; plugins can run inside the scan pipeline.

## Rules for Lite plugins

A plugin must:

- inherit `hexforge_lite.modules.base.BaseModule`
- set `lite_safe = True`
- return a list of `Finding` objects
- use passive evidence only
- avoid network requests, brute force, payload spraying, exploitation, mutation, authentication bypass, or destructive behavior

## Example

`passive_module_example.py` maps public `meta name="generator"` HTML metadata when present. It is intentionally informational and demonstrates the plugin flow without inventing vulnerabilities.

## Loading

Plugins in this directory are loaded by `hexforge_lite.plugins.load_lite_plugins()` and appended to the normal module pipeline. Plugin module names appear in the report as `plugin:<plugin_name>`.

Disable plugin loading with:

```bash
HEXFORGE_ENABLE_PLUGINS=0 python3 server.py
```
