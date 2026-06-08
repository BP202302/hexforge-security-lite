from __future__ import annotations

import argparse
import hashlib
import json
import time

import httpx
from crewai_hive import mint_receipt


DEFAULT_TAG = "bounty_brandon_hive_receipt_scout"


def build_agent_output(topic: str) -> dict:
    """Deterministic agent result, intentionally no paid LLM dependency."""
    observations = [
        "Hive receipts provide verifiable provenance for agent actions.",
        "The demo uses the official crewai-hive SDK and the free receipt endpoint.",
        "Only hashes and metadata are sent; the full local task text is kept local.",
    ]
    digest = hashlib.sha256((topic + "|" + "|".join(observations)).encode("utf-8")).hexdigest()
    return {
        "agent": "Receipt Scout",
        "framework": "crewai",
        "topic": topic,
        "summary": "A small CrewAI-style agent report with Hive receipt provenance.",
        "observations": observations,
        "local_digest": digest,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Mint a Hive receipt for a CrewAI-style agent run.")
    parser.add_argument("--topic", default="Hive receipt provenance for AI agents")
    parser.add_argument("--tag", default=DEFAULT_TAG)
    parser.add_argument(
        "--insecure-local-cert-workaround",
        action="store_true",
        help="Use only when local Python cannot validate the Hive endpoint certificate.",
    )
    args = parser.parse_args()

    result = build_agent_output(args.topic)
    output_text = json.dumps(result, sort_keys=True, separators=(",", ":"))

    metadata = {
        "framework": "crewai",
        "event": "task_complete",
        "agent_role": result["agent"],
        "task_hash": hashlib.sha256(args.topic.encode("utf-8")).hexdigest(),
        "output_hash": hashlib.sha256(output_text[:4096].encode("utf-8")).hexdigest(),
        "ts": int(time.time()),
        "tag": args.tag,
        "sdk": "crewai-hive",
        "sdk_version": "0.1.0",
        "repo_purpose": "Hive Embed Bounty public verification demo",
    }

    if args.insecure_local_cert_workaround:
        body = {"payload": json.dumps(metadata, separators=(",", ":"))}
        response = httpx.post(
            "https://hivemorph.onrender.com/v1/receipt/free",
            json=body,
            headers={"Content-Type": "application/json"},
            timeout=15,
            verify=False,
        )
        response.raise_for_status()
        receipt_json = response.json()
        receipt_id = receipt_json.get("receipt_id") or receipt_json.get("id")
    else:
        receipt_id = mint_receipt(metadata, verbose=True)
    if not receipt_id:
        print("receipt_id=")
        print("verify_url=")
        return 1

    print("agent_output=" + json.dumps(result, sort_keys=True))
    print(f"receipt_id={receipt_id}")
    print(f"verify_url=https://thehiveryiq.com/verify/?id={receipt_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
