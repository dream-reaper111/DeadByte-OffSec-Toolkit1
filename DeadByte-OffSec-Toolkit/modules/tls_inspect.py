#!/usr/bin/env python3

import argparse
import socket
import ssl
from datetime import datetime, timezone

def inspect_tls(host, port=443, timeout=5):
    context = ssl.create_default_context()

    with socket.create_connection((host, port), timeout=timeout) as sock:
        with context.wrap_socket(sock, server_hostname=host) as tls:
            cert = tls.getpeercert()

            subject = dict(x[0] for x in cert.get("subject", []))
            issuer = dict(x[0] for x in cert.get("issuer", []))
            sans = [
                value for kind, value in cert.get("subjectAltName", [])
                if kind == "DNS"
            ]

            not_after = cert.get("notAfter")
            expiry = None
            days_left = None

            if not_after:
                expiry = datetime.strptime(
                    not_after, "%b %d %H:%M:%S %Y %Z"
                ).replace(tzinfo=timezone.utc)
                days_left = (expiry - datetime.now(timezone.utc)).days

            return {
                "host": host,
                "port": port,
                "protocol": tls.version(),
                "cipher": tls.cipher(),
                "subject_common_name": subject.get("commonName"),
                "issuer_common_name": issuer.get("commonName"),
                "subject_alt_names": sans,
                "expires": expiry.isoformat() if expiry else None,
                "days_until_expiry": days_left,
            }

def interactive_tls_inspect():
    host = input("TLS host: ").strip()
    port_raw = input("Port [443]: ").strip()
    port = int(port_raw) if port_raw else 443

    result = inspect_tls(host, port)

    for k, v in result.items():
        print(f"{k}: {v}")

def main():
    ap = argparse.ArgumentParser(description="Inspect a TLS certificate")
    ap.add_argument("host")
    ap.add_argument("--port", type=int, default=443)
    args = ap.parse_args()

    for k, v in inspect_tls(args.host, args.port).items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
