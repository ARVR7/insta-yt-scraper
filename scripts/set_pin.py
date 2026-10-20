#!/usr/bin/env python3
"""Validate a PIN request (env BODY) and write or remove docs/pin.json. Run by .github/workflows/set-pin.yml.

BODY is {"salt": <32 hex>, "iter": <int>, "hash": <64 hex>} or {"remove": true}. The PIN itself never
leaves the phone: only its salted PBKDF2-SHA256 hash is stored.
"""
import json
import os
import re
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "docs" / "pin.json"

try:
    d = json.loads(os.environ.get("BODY", ""))
except ValueError:
    sys.exit("body is not JSON")
if d.get("remove") is True and len(d) == 1:
    OUT.unlink(missing_ok=True)
    print("PIN removed")
    sys.exit(0)
ok = (set(d) == {"salt", "iter", "hash"} and re.fullmatch(r"[0-9a-f]{32}", str(d["salt"])) and re.fullmatch(r"[0-9a-f]{64}", str(d["hash"]))
      and isinstance(d["iter"], int) and 100000 <= d["iter"] <= 2000000)
if not ok:
    sys.exit("body is not a valid PIN record")
OUT.write_text(json.dumps(d) + "\n")
print("PIN written")
