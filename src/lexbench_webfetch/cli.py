"""Small command interface for portable benchmark inputs."""
import argparse
import json
from pathlib import Path

from .benchmark import export, registry, validate, verify_inputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect and verify LexBench Web Fetch inputs")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="List the versioned suites")
    check = sub.add_parser("validate", help="Check all public definitions and bindings")
    check.add_argument("--suite")
    for name in ("verify-inputs", "export"):
        command = sub.add_parser(name)
        command.add_argument("--suite", required=True)
        command.add_argument("--source", type=Path, required=True)
        if name == "export":
            command.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "list":
            result = [{k: row[k] for k in ("id", "dataset_id", "case_count")} for row in registry()["suites"]]
        elif args.command == "validate":
            result = [validate(row["id"]) for row in registry()["suites"]
                      if args.suite is None or row["id"] == args.suite]
            if not result:
                raise ValueError(f"Unknown suite: {args.suite}")
        elif args.command == "verify-inputs":
            result = verify_inputs(args.suite, args.source)
        else:
            result = {"dataset": str(export(args.suite, args.source, args.output).resolve())}
    except (ValueError, KeyError, OSError) as error:
        parser.exit(1, f"{error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
