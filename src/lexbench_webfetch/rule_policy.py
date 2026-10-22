"""Versioned extraction policy data, included in the scorer fingerprint."""
import json
from pathlib import Path

POLICY_PATH = Path(__file__).with_name("definitions") / "evaluation" / "scorer-policy-v1.json"
SCORER_POLICY = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
if SCORER_POLICY.get("version") != 1:
    raise ValueError("Unsupported scorer policy version")
