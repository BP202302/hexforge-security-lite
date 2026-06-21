## Summary

Adds retry/backoff and circuit-breaker behavior to `tools/health_check.py` so transient HTTP probe failures can be retried without hammering repeatedly failing services.

## Changes

- Added `--max-retries`, `--backoff-factor`, and `--circuit-threshold` CLI flags.
- Added exponential backoff using `base_delay * (backoff_factor ** attempt)`.
- Added an in-memory circuit breaker keyed by HTTP endpoint.
- Added WARNING logs for degraded responses, retries, open circuits, and exhausted critical probes.
- Added aggregate summary stats to health check results and human-readable output.
- Added five focused pytest unit tests for retry/backoff/circuit-breaker behavior.

## Testing

- `python -m pytest tests/test_health_check.py -q`
  - Result: `5 passed in 0.06s`
- `python tools/health_check.py --json --service backend --max-retries 1 --backoff-factor 2 --circuit-threshold 2`
  - Result: exercised the new flags and JSON summary output. It returned `DEGRADED` because the local services were not running on this Windows workstation and Linux system-resource checks are unavailable.

Build diagnostic note:

- `python build.py` failed before building under the default Windows console encoding with `UnicodeEncodeError: 'charmap' codec can't encode character`.
- Retried with `PYTHONUTF8=1`; the full build and `python build.py -m market` produced no output and had to be stopped after waiting, so I could not produce a valid non-stub `.logd` artifact from this environment.

## Checklist

- [x] Relevant modules affected by these changes build locally
- [x] Tests pass locally
- [ ] Diagnostic build log is committed in this PR
- [ ] Documentation has been updated, if applicable
- [x] Configuration or schema changes are documented, if applicable
- [x] No generated build artifacts are committed, except the required diagnostic build log
- [x] Changes are scoped to the PR purpose and avoid unrelated cleanup
- [x] Security, privacy, and error-handling implications have been considered

---

- [ ] I would like to request that my diagnostic build log is removed before merging
