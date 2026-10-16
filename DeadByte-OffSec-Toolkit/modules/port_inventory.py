#!/usr/bin/env python3

import argparse
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

DEFAULT_PORTS = [22, 53, 80, 110, 143, 443, 445, 993, 995, 3389, 8080]

def parse_ports(spec: str):
    ports = set()

    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue

        if "-" in part:
            start, end = part.split("-", 1)
            for p in range(int(start), int(end) + 1):
                if 1 <= p <= 65535:
                    ports.add(p)
        else:
            p = int(part)
            if 1 <= p <= 65535:
                ports.add(p)

    return sorted(ports)

def check_port(host, port, timeout=0.5):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            try:
                service = socket.getservbyport(port)
            except OSError:
                service = "unknown"
            return port, True, service
    except OSError:
        return port, False, None

def scan(host, ports, workers=32, timeout=0.5):
    results = []

    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futs = [pool.submit(check_port, host, p, timeout) for p in ports]

        for fut in as_completed(futs):
            port, is_open, service = fut.result()
            if is_open:
                results.append({
                    "port": port,
                    "service": service
                })

    return sorted(results, key=lambda x: x["port"])

def interactive_port_inventory():
    host = input("Host/IP: ").strip()
    spec = input("Ports [22,80,443]: ").strip() or "22,80,443"
    ports = parse_ports(spec)

    print(f"\nScanning {host} ...")
    results = scan(host, ports)

    if not results:
        print("No requested ports were reachable.")
        return

    for item in results:
        print(f"[OPEN] {item['port']:5d}/tcp  {item['service']}")

def main():
    ap = argparse.ArgumentParser(description="Authorized TCP port inventory")
    ap.add_argument("host")
    ap.add_argument("--ports", default=",".join(map(str, DEFAULT_PORTS)))
    ap.add_argument("--timeout", type=float, default=0.5)
    ap.add_argument("--workers", type=int, default=32)
    args = ap.parse_args()

    results = scan(args.host, parse_ports(args.ports), args.workers, args.timeout)

    for item in results:
        print(f"{item['port']}/tcp open {item['service']}")

if __name__ == "__main__":
    main()
