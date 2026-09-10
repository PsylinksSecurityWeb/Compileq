"""Branding constants and watermark helpers.

Single source of truth for product/maker attribution so it can never drift
out of sync between the CLI banner, report output, MCP tool descriptions,
and JSON output. Every user-facing surface should pull from here rather
than hardcoding the name/maker string locally.
"""

PRODUCT_NAME = "Compileq"
MAKER_NAME = "Psylinks Security Private Limited"
MAKER_URL = "https://psylinkssecurity.com"
TAGLINE = "Compliance triage scanning, built by Psylinks Security Private Limited"


def watermark_line() -> str:
    """Full attribution line — used in report headers/footers and CLI banners."""
    return f"{PRODUCT_NAME} — proprietary compliance triage software by {MAKER_NAME} ({MAKER_URL})"


def short_watermark() -> str:
    """Compact attribution — used inline / in JSON payloads."""
    return f"{PRODUCT_NAME} by {MAKER_NAME}"


def cli_banner() -> str:
    return (
        f"{PRODUCT_NAME}\n"
        f"{TAGLINE}\n"
        f"{MAKER_URL}\n"
        f"(c) {MAKER_NAME}. Proprietary software — not for redistribution. "
        f"See LICENSE.\n"
    )
