#!/usr/bin/env python3

from modules.port_inventory import interactive_port_inventory
from modules.http_audit import interactive_http_audit
from modules.tls_inspect import interactive_tls_inspect
from modules.dns_tools import interactive_dns_tools
from modules.hash_tools import interactive_hash_tools
from modules.file_integrity import interactive_file_integrity
from modules.ioc_extract import interactive_ioc_extract
from modules.report_builder import interactive_report_builder

BANNER = r"""
╔══════════════════════════════════════════╗
║        DEADBYTE OFFSEC TOOLKIT          ║
╚══════════════════════════════════════════╝

AUTHORIZED SYSTEMS ONLY
"""

MENU = """
[1] Port / Service Inventory
[2] HTTP Security Audit
[3] TLS Certificate Inspector
[4] DNS Utilities
[5] Hash Utilities
[6] File Integrity Checker
[7] IOC Extractor
[8] Generate Report
[0] Exit
"""

def main():
    print(BANNER)

    while True:
        print(MENU)
        choice = input("deadbyte> ").strip()

        try:
            if choice == "1":
                interactive_port_inventory()
            elif choice == "2":
                interactive_http_audit()
            elif choice == "3":
                interactive_tls_inspect()
            elif choice == "4":
                interactive_dns_tools()
            elif choice == "5":
                interactive_hash_tools()
            elif choice == "6":
                interactive_file_integrity()
            elif choice == "7":
                interactive_ioc_extract()
            elif choice == "8":
                interactive_report_builder()
            elif choice == "0":
                print("Exiting.")
                break
            else:
                print("Unknown option.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as exc:
            print(f"[!] Error: {exc}")

if __name__ == "__main__":
    main()
