#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from hexforge_lite.engine import ScanEngine


def main() -> int:
    parser = argparse.ArgumentParser(description="HexForge Security Lite CLI")
    parser.add_argument("url", help="Authorized target URL to analyze")
    parser.add_argument("--pretty", action="store_true", help="Pretty print JSON output")
    args = parser.parse_args()
    result = ScanEngine().scan(args.url)
    print(json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
