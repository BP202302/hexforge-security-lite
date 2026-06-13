# PyZX unitaryHACK #455 Patch Package

Prepared patch for:

- Issue: https://github.com/zxcalc/pyzx/issues/455
- Bounty: $100 via unitaryHACK 2026
- Bounty board: https://unitaryhack.dev/bounties/

## Change Summary

This patch documents PyZX support for measurements, resets, ancilla-style initialisation, and `elide_initial_resets`.

Files changed:

- `doc/representations.rst`
- `demos/AllFeatures.ipynb`

## Verification

Executed locally in `work/pyzx`:

```text
python -m pytest tests/test_qasm.py -q
78 passed, 12 skipped

python -m pytest tests/test_init_postselect.py::TestReset::test_to_graph tests/test_circuit.py::TestCircuit::test_measurement_gate -q
2 passed
```

The notebook example was also executed manually as a Python snippet and produced the expected outcome tags for measurements and reset elision.

## Submission Blocker

The patch is committed locally on branch `codex/pyzx-measurement-reset-docs`, commit `f764ea35`.

PR submission is blocked because:

- GitHub connector cannot create a branch on `zxcalc/pyzx`: `403 Resource not accessible by integration`.
- The browser cannot access `github.com` due enterprise network policy.
- There is no `gh` CLI installed and no existing `BP202302/pyzx` fork.

Patch file:

- `0001-document-measurements-and-resets.patch`

