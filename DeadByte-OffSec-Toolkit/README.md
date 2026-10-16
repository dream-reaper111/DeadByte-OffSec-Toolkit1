# DeadByte OffSec Toolkit

> Modular Python utilities for authorized security testing, lab reconnaissance, defensive validation, and incident-response support.

DeadByte OffSec Toolkit is a small collection of cybersecurity utilities built for:

- Home labs
- CTF environments
- Internal security validation
- Defensive assessments
- Incident-response support
- Security coursework
- Portfolio demonstrations

The toolkit intentionally focuses on inspection, inventory, validation, and reporting rather than exploitation.

## Included Modules

- Port and service inventory
- HTTP security-header auditing
- TLS certificate inspection
- DNS lookup utilities
- Hashing and verification
- File-integrity checks
- IOC extraction
- Markdown / JSON reporting

## Project Structure

```text
DeadByte-OffSec-Toolkit/
├── README.md
├── requirements.txt
├── deadbyte.py
├── modules/
│   ├── __init__.py
│   ├── port_inventory.py
│   ├── http_audit.py
│   ├── tls_inspect.py
│   ├── dns_tools.py
│   ├── hash_tools.py
│   ├── file_integrity.py
│   ├── ioc_extract.py
│   └── report_builder.py
├── examples/
│   └── targets.txt
└── reports/
```

## Installation

```bash
git clone <your-repo-url>
cd DeadByte-OffSec-Toolkit

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Launch

```bash
python3 deadbyte.py
```

You will get a terminal menu similar to:

```text
╔══════════════════════════════════════════╗
║        DEADBYTE OFFSEC TOOLKIT          ║
╚══════════════════════════════════════════╝

[1] Port / Service Inventory
[2] HTTP Security Audit
[3] TLS Certificate Inspector
[4] DNS Utilities
[5] Hash Utilities
[6] File Integrity Checker
[7] IOC Extractor
[8] Generate Report
[0] Exit
```

## Scope

Use this toolkit only on:

- Systems you own
- Systems you administer
- Environments where you have explicit permission to test
- Legal training environments and CTFs

Do not use it for unauthorized access or disruption.

## Examples

### Port Inventory

```bash
python3 -m modules.port_inventory 127.0.0.1 --ports 22,80,443,8000-8010
```

### HTTP Audit

```bash
python3 -m modules.http_audit https://example.com
```

### TLS Inspection

```bash
python3 -m modules.tls_inspect example.com --port 443
```

### DNS Lookup

```bash
python3 -m modules.dns_tools example.com
```

### Hash a File

```bash
python3 -m modules.hash_tools hash README.md
```

### Verify a File

```bash
python3 -m modules.hash_tools verify README.md <sha256>
```

### Create a File-Integrity Baseline

```bash
python3 -m modules.file_integrity baseline ./some-folder baseline.json
```

### Compare Against the Baseline

```bash
python3 -m modules.file_integrity check ./some-folder baseline.json
```

### Extract IOCs

```bash
python3 -m modules.ioc_extract suspicious_log.txt
```

## Roadmap

Potential future additions:

- Nmap XML import
- PCAP metadata summaries
- Sigma rule helpers
- STIX/TAXII export
- CVE lookup using public vulnerability APIs
- Certificate-chain analysis
- Local service inventory
- JSONL output
- Better Markdown reporting
- Plugin architecture
- TUI interface
- Unit tests
- GitHub Actions
- Docker support

## Disclaimer

This project is for authorized security testing, defensive research, education, and lab use only.

## License

MIT is recommended.
