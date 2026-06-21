# kickama issue #15 patch package

Upstream issue: https://github.com/thanhle74/kickama/issues/15

Patch source: local branch `codex/health-check-retry-circuit`, commit `f9b31a96b22b95020f054d6baedaeb78ede61660`.

## What changed

- Added configurable HTTP probe retry support with `--max-retries`.
- Added exponential backoff via `--backoff-factor`.
- Added an in-memory circuit breaker via `--circuit-threshold`.
- Added warning logs for degraded and critical probes.
- Added aggregate health summary stats.
- Added five unit tests covering retry, backoff, warning behavior, circuit-open behavior, reset-on-success behavior, and summary aggregation.

## Validation

Passed:

```text
python -m pytest tests/test_health_check.py -q
5 passed in 0.06s
```

CLI smoke:

```text
python tools/health_check.py --json --service backend --max-retries 1 --backoff-factor 2 --circuit-threshold 2
```

The smoke command exercised the new flags and summary output. It returned degraded status on this Windows workstation because the repo services were not running locally and Linux `/proc`/`statvfs` checks are unavailable.

Build note:

`python build.py` first failed under Windows `cp1252` console encoding while printing a Unicode warning symbol. Retrying with `PYTHONUTF8=1` and the modular `python build.py -m market` path did not produce output and had to be stopped after waiting, so no valid diagnostic `.logd` was generated in this environment.

## Patch

Apply with:

```text
git am 0001-Add-retry-and-circuit-breaker-health-probes.patch
```
