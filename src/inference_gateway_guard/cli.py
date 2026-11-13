"""CLI for the inference gateway guard."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

import yaml

from .guard import evaluate


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate an AI inference gateway contract")
    parser.add_argument("contract", type=Path)
    parser.add_argument("--policy", type=Path, default=Path("policy/gateway-policy.yaml"))
    parser.add_argument("--as-of", type=date.fromisoformat)
    parser.add_argument("--output", choices=("text", "json"), default="text")
    args = parser.parse_args()
    result = evaluate(yaml.safe_load(args.contract.read_text()), yaml.safe_load(args.policy.read_text()), args.as_of)
    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"{result['decision']} {result['score']}% ({result['passed']}/{result['total']})")
        for item in result["rules"]:
            print(f"{'PASS' if item['passed'] else item['severity']} {item['rule']}: {item['message']}")
    raise SystemExit(2 if result["decision"] == "BLOCK" else 0)


if __name__ == "__main__":
    main()
