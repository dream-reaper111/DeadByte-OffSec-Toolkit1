#!/usr/bin/env python3

import argparse
import json
from pathlib import Path
from .hash_tools import sha256_file

def build_baseline(root):
    root = Path(root)
    baseline = {}

    for path in sorted(root.rglob("*")):
        if path.is_file():
            rel = str(path.relative_to(root))
            try:
                baseline[rel] = sha256_file(path)
            except OSError:
                pass

    return baseline

def compare(root, baseline):
    root = Path(root)
    current = build_baseline(root)

    baseline_keys = set(baseline)
    current_keys = set(current)

    added = sorted(current_keys - baseline_keys)
    removed = sorted(baseline_keys - current_keys)
    modified = sorted(
        k for k in current_keys & baseline_keys
        if current[k] != baseline[k]
    )

    return {
        "added": added,
        "removed": removed,
        "modified": modified,
    }

def interactive_file_integrity():
    print("[1] Create baseline")
    print("[2] Check baseline")
    choice = input("> ").strip()

    root = input("Directory: ").strip()
    baseline_file = input("Baseline JSON [baseline.json]: ").strip() or "baseline.json"

    if choice == "1":
        data = build_baseline(root)
        Path(baseline_file).write_text(json.dumps(data, indent=2))
        print(f"Baseline saved to {baseline_file}")
    elif choice == "2":
        baseline = json.loads(Path(baseline_file).read_text())
        result = compare(root, baseline)
        print(json.dumps(result, indent=2))

def main():
    ap = argparse.ArgumentParser(description="File-integrity baseline utility")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_base = sub.add_parser("baseline")
    p_base.add_argument("directory")
    p_base.add_argument("output")

    p_check = sub.add_parser("check")
    p_check.add_argument("directory")
    p_check.add_argument("baseline")

    args = ap.parse_args()

    if args.cmd == "baseline":
        data = build_baseline(args.directory)
        Path(args.output).write_text(json.dumps(data, indent=2))
    else:
        baseline = json.loads(Path(args.baseline).read_text())
        print(json.dumps(compare(args.directory, baseline), indent=2))

if __name__ == "__main__":
    main()
