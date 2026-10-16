#!/usr/bin/env python3

import argparse
import json
from datetime import datetime
from pathlib import Path

def build_markdown(title, findings):
    lines = [
        f"# {title}",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Summary",
        "",
        "DeadByte OffSec Toolkit assessment report.",
        "",
        "## Findings",
        "",
    ]

    if not findings:
        lines.append("No findings supplied.")
        return "\n".join(lines)

    for key, value in findings.items():
        lines.append(f"### {key}")
        lines.append("")
        if isinstance(value, (dict, list)):
            lines.append("```json")
            lines.append(json.dumps(value, indent=2))
            lines.append("```")
        else:
            lines.append(str(value))
        lines.append("")

    return "\n".join(lines)

def interactive_report_builder():
    title = input("Report title: ").strip() or "Security Assessment"
    json_file = input("Input JSON file: ").strip()
    output = input("Output Markdown [reports/report.md]: ").strip() or "reports/report.md"

    findings = json.loads(Path(json_file).read_text())
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text(build_markdown(title, findings))
    print(f"Report written to {output}")

def main():
    ap = argparse.ArgumentParser(description="Build a Markdown report from JSON")
    ap.add_argument("json_file")
    ap.add_argument("--title", default="Security Assessment")
    ap.add_argument("-o", "--output", default="report.md")
    args = ap.parse_args()

    findings = json.loads(Path(args.json_file).read_text())
    Path(args.output).write_text(build_markdown(args.title, findings))
    print(args.output)

if __name__ == "__main__":
    main()
