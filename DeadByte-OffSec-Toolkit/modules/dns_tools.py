#!/usr/bin/env python3

import argparse
import socket
import dns.resolver

RECORD_TYPES = ["A", "AAAA", "MX", "NS", "TXT"]

def query(domain, record_type):
    try:
        answers = dns.resolver.resolve(domain, record_type)
        return [str(r) for r in answers]
    except Exception as exc:
        return [f"<error: {exc}>"]

def all_records(domain):
    return {rtype: query(domain, rtype) for rtype in RECORD_TYPES}

def reverse_lookup(ip):
    try:
        return socket.gethostbyaddr(ip)
    except Exception as exc:
        return (f"<error: {exc}>", [], [])

def interactive_dns_tools():
    domain = input("Domain: ").strip()

    for rtype, values in all_records(domain).items():
        print(f"\n{rtype}:")
        for value in values:
            print(f"  {value}")

def main():
    ap = argparse.ArgumentParser(description="DNS lookup helper")
    ap.add_argument("domain")
    ap.add_argument("--type", choices=RECORD_TYPES)
    args = ap.parse_args()

    if args.type:
        for value in query(args.domain, args.type):
            print(value)
    else:
        for rtype, values in all_records(args.domain).items():
            print(f"[{rtype}]")
            for value in values:
                print(f"  {value}")

if __name__ == "__main__":
    main()
