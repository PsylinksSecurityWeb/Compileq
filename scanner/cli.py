"""Command-line entry point: python -m scanner.cli scan <path> [options]"""
from __future__ import annotations
import argparse
import json
import os
import sys

from . import kb_loader, engine, report, fallback, web_lookup
from .branding import cli_banner, PRODUCT_NAME, MAKER_NAME, MAKER_URL

RULES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rules")


def main(argv=None):
    print(cli_banner())
    parser = argparse.ArgumentParser(prog="compileq")
    sub = parser.add_subparsers(dest="command", required=True)

    scan_p = sub.add_parser("scan", help="Scan a repo for compliance findings")
    scan_p.add_argument("path", nargs="?", default=".")
    scan_p.add_argument("--markets", default="", help="Comma-separated target markets, e.g. EU,US-CA,US")
    scan_p.add_argument("--regulations", default="", help="Comma-separated subset, e.g. GDPR,WCAG (default: all)")
    scan_p.add_argument("--out", default="report.md")
    scan_p.add_argument("--json-out", default="report.json")

    lookup_p = sub.add_parser("lookup", help="Check if a regulation is in the KB / get a fallback request")
    lookup_p.add_argument("regulation_name")

    sub.add_parser("sources", help="List the full official-source registry")

    check_p = sub.add_parser("check-source", help="Validate a URL as an official source before citing it")
    check_p.add_argument("url")
    check_p.add_argument("--regulation", default="")

    args = parser.parse_args(argv)

    if args.command == "scan":
        if not os.path.isdir(args.path):
            print(f"ERROR: '{args.path}' is not a directory or does not exist. "
                  f"Refusing to write a report — a 100/100 readiness score here "
                  f"would be misleading, not a real clean scan.", file=sys.stderr)
            return 2

        rules = kb_loader.load_rules(RULES_DIR)
        if args.regulations:
            wanted = {r.strip().upper() for r in args.regulations.split(",")}
            rules = [r for r in rules if r["regulation"].upper() in wanted]
        markets = [m.strip() for m in args.markets.split(",") if m.strip()]

        result = engine.scan_repo(args.path, rules, markets)

        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        md = report.to_markdown(result)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(md)

        print(f"Scanned {result['files_scanned']} files with {result['rules_evaluated']} rules.")
        print(f"Overall readiness: {result['overall_readiness']}/100")
        print(f"Findings: {len(result['findings'])}")
        print(f"Reports written to {args.out} and {args.json_out}")
        print(f"\n{PRODUCT_NAME} by {MAKER_NAME} — {MAKER_URL}")

    elif args.command == "lookup":
        print(json.dumps(fallback.build_lookup_request(args.regulation_name), indent=2))

    elif args.command == "sources":
        print(json.dumps(web_lookup.list_registry(), indent=2))

    elif args.command == "check-source":
        print(json.dumps(fallback.check_source(args.url, args.regulation), indent=2))


if __name__ == "__main__":
    sys.exit(main())
