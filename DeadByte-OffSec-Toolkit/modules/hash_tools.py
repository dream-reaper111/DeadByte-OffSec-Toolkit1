#!/usr/bin/env python3

import argparse
import hashlib
from pathlib import Path

CHUNK = 1024 * 1024

def sha256_file(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        while True:
            chunk = f.read(CHUNK)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()

def interactive_hash_tools():
    print("[1] Hash file")
    print("[2] Verify SHA-256")
    choice = input("> ").strip()

    path = input("File path: ").strip()

    if choice == "1":
        print(sha256_file(path))
    elif choice == "2":
        expected = input("Expected SHA-256: ").strip().lower()
        actual = sha256_file(path).lower()
        print(f"Actual:   {actual}")
        print(f"Expected: {expected}")
        print("MATCH" if actual == expected else "MISMATCH")

def main():
    ap = argparse.ArgumentParser(description="Hash and verify files")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_hash = sub.add_parser("hash")
    p_hash.add_argument("file")

    p_verify = sub.add_parser("verify")
    p_verify.add_argument("file")
    p_verify.add_argument("sha256")

    args = ap.parse_args()

    actual = sha256_file(args.file)

    if args.cmd == "hash":
        print(actual)
    else:
        print("MATCH" if actual.lower() == args.sha256.lower() else "MISMATCH")

if __name__ == "__main__":
    main()
