#!/usr/bin/env python3

import argparse
import json
import re
from pathlib import Path

IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
DOMAIN_RE = re.compile(
    r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,63}\b"
)
SHA256_RE = re.compile(r"\b[a-fA-F0-9]{64}\b")
SHA1_RE = re.compile(r"\b[a-fA-F0-9]{40}\b")
MD5_RE = re.compile(r"\b[a-fA-F0-9]{32}\b")
URL_RE = re.compile(r"https?://[^\s'\"<>]+")

def valid_ip(ip):
    try:
        return all(0 <= int(x) <= 255 for x in ip.split("."))
    except Exception:
        return False

def extract(text):
    return {
        "ips": sorted({ip for ip in IP_RE.findall(text) if valid_ip(ip)}),
        "domains": sorted(set(DOMAIN_RE.findall(text))),
        "urls": sorted(set(URL_RE.findall(text))),
        "sha256": sorted(set(SHA256_RE.findall(text))),
        "sha1": sorted(set(SHA1_RE.findall(text))),
        "md5": sorted(set(MD5_RE.findall(text))),
    }

def interactive_ioc_extract():
    path = input("Text/log file: ").strip()
    data = extract(Path(path).read_text(errors="replace"))
    print(json.dumps(data, indent=2))

def main():
    ap = argparse.ArgumentParser(description="Extract common IOCs from text")
    ap.add_argument("file")
    ap.add_argument("-o", "--output")
    args = ap.parse_args()

    data = extract(Path(args.file).read_text(errors="replace"))
    rendered = json.dumps(data, indent=2)

    if args.output:
        Path(args.output).write_text(rendered)

    print(rendered)

if __name__ == "__main__":
    main()
