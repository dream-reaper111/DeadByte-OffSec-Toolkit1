#!/usr/bin/env python3

import argparse
import requests
from urllib.parse import urlparse

SECURITY_HEADERS = {
    "content-security-policy": "Content Security Policy",
    "strict-transport-security": "HTTP Strict Transport Security",
    "x-content-type-options": "MIME sniffing protection",
    "x-frame-options": "Clickjacking protection",
    "referrer-policy": "Referrer Policy",
    "permissions-policy": "Permissions Policy",
}

def normalize_url(url):
    if "://" not in url:
        url = "https://" + url
    return url

def audit(url, timeout=10):
    url = normalize_url(url)

    r = requests.get(
        url,
        timeout=timeout,
        allow_redirects=True,
        headers={"User-Agent": "DeadByte-OffSec-Toolkit/1.0"}
    )

    headers = {k.lower(): v for k, v in r.headers.items()}
    missing = [name for name in SECURITY_HEADERS if name not in headers]
    present = {
        name: headers[name]
        for name in SECURITY_HEADERS
        if name in headers
    }

    parsed = urlparse(r.url)

    return {
        "requested_url": url,
        "final_url": r.url,
        "status_code": r.status_code,
        "server": r.headers.get("Server"),
        "https": parsed.scheme == "https",
        "present_security_headers": present,
        "missing_security_headers": missing,
    }

def interactive_http_audit():
    url = input("URL: ").strip()
    result = audit(url)

    print(f"\nStatus: {result['status_code']}")
    print(f"Final URL: {result['final_url']}")
    print(f"HTTPS: {result['https']}")
    print(f"Server header: {result['server']}")

    print("\nPresent security headers:")
    if result["present_security_headers"]:
        for k, v in result["present_security_headers"].items():
            print(f"  [+] {k}: {v}")
    else:
        print("  none detected")

    print("\nMissing security headers:")
    for k in result["missing_security_headers"]:
        print(f"  [-] {k} - {SECURITY_HEADERS[k]}")

def main():
    ap = argparse.ArgumentParser(description="HTTP security-header audit")
    ap.add_argument("url")
    args = ap.parse_args()
    interactive = audit(args.url)

    for k, v in interactive.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
