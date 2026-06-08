# Hive Receipt Scout Agent

Minimal public CrewAI-style agent demo for the Hive Embed Bounty.

The agent produces a deterministic research-style result and mints a Hive receipt with the official `crewai-hive` SDK. It does not require a paid LLM API key, wallet connection, deposit, or Hive login.

## One-command run

```bash
python -m pip install -r requirements.txt && python src/receipt_scout_agent.py
```

Successful output includes:

```text
receipt_id=<receipt id>
verify_url=https://thehiveryiq.com/verify/?id=<receipt id>
```

## What is sent to Hive

The runner sends only receipt metadata:

- framework: `crewai`
- event: `task_complete`
- SHA-256 hashes for task/output
- timestamp
- bounty tag
- SDK name/version

The full local agent output is printed locally and is not sent in cleartext.

## Bounty Fit

- Public repo with MIT license.
- Uses the official `crewai-hive` SDK.
- One command mints at least one verifiable Hive receipt.
- No payment, KYC, wallet connection, or phone number is required to run.

## Latest Verification

Latest local run:

- receipt_id: `59df591d044b494bb4606a56f2a6a019`
- verify_url: https://thehiveryiq.com/verify/?id=59df591d044b494bb4606a56f2a6a019
- raw API confirmed: https://hivemorph.onrender.com/v1/receipt/59df591d044b494bb4606a56f2a6a019

Run the one-command demo to mint a fresh receipt, then open the printed `verify_url`.

### Local SSL Fallback

On machines where Python cannot validate the local certificate chain, the runner includes an explicit fallback for local testing:

```bash
python src/receipt_scout_agent.py --insecure-local-cert-workaround
```

The standard command remains the recommended path.
