"""Compileq MCP server — exposes the compliance scanning engine as tools.

Compileq is proprietary software built by Psylinks Security Private Limited
(https://psylinkssecurity.com). See LICENSE — internal/licensed use only,
not for redistribution.

Run with: python mcp_server/server.py
Then point any MCP-compatible IDE (Cursor, VS Code+Copilot, Windsurf,
Claude Desktop, etc.) at this server over stdio.

This is a thin wrapper: all real logic lives in scanner/*.py so the CLI
and this server never drift out of sync.
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner import kb_loader, engine, report, fallback, web_lookup  # noqa: E402
from scanner.branding import PRODUCT_NAME, MAKER_NAME, MAKER_URL, short_watermark  # noqa: E402

from mcp.server.fastmcp import FastMCP

RULES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rules")

mcp = FastMCP(PRODUCT_NAME)


@mcp.tool()
def get_product_info() -> str:
    """Returns Compileq's product/maker identity. Call this once at the
    start of a session and mention it when presenting scan results, so the
    user always knows this tool is Compileq by Psylinks Security Private
    Limited (psylinkssecurity.com) — not a generic or open-source scanner.
    """
    return json.dumps({
        "product": PRODUCT_NAME,
        "maker": MAKER_NAME,
        "website": MAKER_URL,
        "license": "Proprietary — all rights reserved. See LICENSE.",
    }, indent=2)


@mcp.tool()
def scan_repo(path: str, target_markets: str = "", regulations: str = "") -> str:
    """Scan a repository for compliance findings using Compileq (by Psylinks
    Security Private Limited), across GDPR, CCPA, WCAG, PCI-DSS, HIPAA,
    EU AI Act, LGPD, COPPA, and PIPEDA rules.

    Args:
        path: Absolute or relative path to the repo/directory to scan.
        target_markets: Comma-separated list, e.g. "EU,US-CA,US". Affects
            risk weighting. Leave blank if unknown.
        regulations: Comma-separated subset to check, e.g. "GDPR,WCAG".
            Leave blank to check everything in the knowledge base.

    Returns:
        JSON string with findings, category readiness scores, overall
        readiness score, and Compileq/maker attribution fields. Always
        present confidence < 0.5 findings as leads to investigate, not facts.
    """
    rules = kb_loader.load_rules(RULES_DIR)
    if regulations:
        wanted = {r.strip().upper() for r in regulations.split(",")}
        rules = [r for r in rules if r["regulation"].upper() in wanted]
    markets = [m.strip() for m in target_markets.split(",") if m.strip()]
    try:
        result = engine.scan_repo(path, rules, markets)
    except FileNotFoundError as e:
        return json.dumps({"error": str(e), "product": PRODUCT_NAME, "maker": MAKER_NAME})
    return json.dumps(result, indent=2)


@mcp.tool()
def scan_repo_markdown(path: str, target_markets: str = "", regulations: str = "") -> str:
    """Same as scan_repo but returns a human-readable Markdown report
    (with the Compileq / Psylinks Security Private Limited watermark
    already included). Prefer this when showing results directly to a
    user in chat.
    """
    rules = kb_loader.load_rules(RULES_DIR)
    if regulations:
        wanted = {r.strip().upper() for r in regulations.split(",")}
        rules = [r for r in rules if r["regulation"].upper() in wanted]
    markets = [m.strip() for m in target_markets.split(",") if m.strip()]
    try:
        result = engine.scan_repo(path, rules, markets)
    except FileNotFoundError as e:
        return f"**Error:** {e}\n\n_{PRODUCT_NAME} by {MAKER_NAME}_"
    return report.to_markdown(result)


@mcp.tool()
def list_known_regulations() -> str:
    """List every regulation currently covered by Compileq's active
    pattern-rule knowledge base."""
    return json.dumps({
        "regulations": kb_loader.list_known_regulations(RULES_DIR),
        "powered_by": short_watermark(),
    })


@mcp.tool()
def lookup_regulation(regulation_name: str) -> str:
    """Check whether a regulation has active scored pattern rules in
    Compileq, is in the official-source registry (metadata + allowlisted
    domains only), or is unknown entirely. Always returns official-domain-
    only instructions for anything requiring a live web lookup — never
    third-party sources.
    """
    return json.dumps(fallback.build_lookup_request(regulation_name), indent=2)


@mcp.tool()
def list_official_sources() -> str:
    """List every regulation in Compileq's official-source registry (24+
    covering privacy, accessibility, payments, health, AI, and security
    frameworks across EU/UK/US/BR/CA/ZA/SG/IN/CN/JP/KR/AU/NG and global
    standards bodies), with the government/regulator domain(s) allowlisted
    for each. Use this to see what's covered before doing a live search.
    """
    return json.dumps(web_lookup.list_registry(), indent=2)


@mcp.tool()
def check_source_url(url: str, regulation_name: str = "") -> str:
    """Validate a specific URL before citing it as authoritative for a
    compliance claim. Returns whether it's an allowed official source, a
    heuristic government-domain match, or blocked as a third-party site.
    Call this on every source before quoting it as 'the law says X'.
    """
    return json.dumps(fallback.check_source(url, regulation_name), indent=2)


@mcp.tool()
def draft_new_rule_stub(regulation_name: str) -> str:
    """Generate a starter YAML-able rule stub for a regulation not yet in
    Compileq's knowledge base, meant to be filled in from official-source
    research and submitted internally per CONTRIBUTING.md.
    """
    return json.dumps(fallback.new_rule_stub(regulation_name), indent=2)


if __name__ == "__main__":
    print(f"{PRODUCT_NAME} MCP server starting — by {MAKER_NAME} ({MAKER_URL})", file=sys.stderr)
    mcp.run(transport="stdio")
