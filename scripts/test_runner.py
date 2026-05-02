#!/usr/bin/env python3
from __future__ import annotations

# Stable project validation runner. It executes the controlled 10-profile
# fixture suite three times to verify precision, deduplication and scoring.

import subprocess
import sys

subprocess.run([sys.executable, "scripts/self_check.py"], check=True)
