"""Official-source registry + domain allowlist enforcement.

This module is the core of "the scanner can look things up on the internet
when it doesn't know, but only from official sites, never third parties."

It does NOT make network calls itself — the scanner engine stays offline
and deterministic (see docs/ARCHITECTURE.md). Instead, this module is the
policy layer: given a regulation name, it tells the calling AI host (a) what
it already knows, (b) which domains are the ONLY acceptable sources if it
needs to search or fetch, and (c) rejects/flags any URL that isn't on the
allowlist so a citation from a law-firm blog or "compliance platform"
marketing page never gets treated as authoritative.
"""
from __future__ import annotations
import os
import re
import yaml

RULES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rules")

# Generic patterns that indicate a domain is *plausibly* an official
# government/standards-body source even if it's not in our curated
# registry yet — used only as a last-resort heuristic gate, and always
# surfaced to the user as "unverified, heuristic match" rather than trusted
# outright the way a registry hit is.
OFFICIAL_DOMAIN_HEURISTICS = [
    r"\.gov$", r"\.gov\.[a-z]{2}$", r"\.go\.[a-z]{2}$",   # .gov, .gov.uk, .go.jp etc
    r"\.europa\.eu$",                                       # EU institutions
    r"^eur-lex\.europa\.eu$",
    r"\.gob\.[a-z]{2}$",                                   # Spanish-speaking govts
    r"\.gouv\.fr$",
    r"^iso\.org$", r"^w3\.org$", r"^ietf\.org$",            # standards bodies
]

KNOWN_THIRD_PARTY_BLOCKLIST_HINTS = [
    "medium.com", "substack.com", "wordpress.com", "blogspot.com",
    "reddit.com", "quora.com",
]


def _load_registry() -> list[dict]:
    path = os.path.join(RULES_DIR, "official_sources.yaml")
    with open(path, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    return doc.get("sources", [])


def find_registry_entry(regulation_query: str) -> dict | None:
    """Fuzzy match a regulation name/code against the registry."""
    q = regulation_query.strip().lower().replace(" ", "_").replace("-", "_")
    for entry in _load_registry():
        code = entry["code"].lower().replace("-", "_")
        name = entry["name"].lower()
        if q == code or q in name.replace(" ", "_") or entry["code"].lower() in q:
            return entry
    return None


def list_registry() -> list[dict]:
    return _load_registry()


def is_allowed_domain(url: str, registry_entry: dict | None = None) -> dict:
    """Check whether a URL is acceptable to cite/fetch as authoritative.

    Returns a dict: {"allowed": bool, "reason": str, "tier": "registry"|"heuristic"|"blocked"}
    tier="registry" means it matched a curated official_domains entry (highest trust).
    tier="heuristic" means it matched a generic .gov-style pattern but isn't
      in the curated list yet — usable, but the host AI should say so.
    tier="blocked" means it's a known third-party content platform or
      simply didn't match anything official — must not be cited as
      authoritative; treat as background context at most, with the source
      named explicitly.
    """
    try:
        domain = re.sub(r"^https?://", "", url).split("/")[0].lower()
        domain = re.sub(r"^www\.", "", domain)
    except Exception:
        return {"allowed": False, "reason": "could not parse URL", "tier": "blocked"}

    for hint in KNOWN_THIRD_PARTY_BLOCKLIST_HINTS:
        if hint in domain:
            return {"allowed": False, "reason": f"{domain} is a third-party content platform, not an official source", "tier": "blocked"}

    if registry_entry:
        for official in registry_entry.get("official_domains", []):
            if domain == official.lower() or domain.endswith("." + official.lower()):
                return {"allowed": True, "reason": f"matches registered official domain for {registry_entry['code']}", "tier": "registry"}

    for pattern in OFFICIAL_DOMAIN_HEURISTICS:
        if re.search(pattern, domain):
            return {"allowed": True, "reason": f"{domain} matches a government/standards-body domain pattern", "tier": "heuristic"}

    return {"allowed": False, "reason": f"{domain} is not a recognized official source", "tier": "blocked"}


def lookup_instructions(regulation_query: str) -> dict:
    """The main entry point used by scanner/fallback.py and the MCP tool.

    Given any regulation name (known or not), returns exactly what the
    host AI should do: use the registry entry if one exists (fastest,
    highest trust), or fall back to a constrained web search with an
    explicit domain allowlist and instructions to reject anything else.
    """
    entry = find_registry_entry(regulation_query)

    if entry:
        return {
            "status": "in_registry",
            "regulation": entry["name"],
            "code": entry["code"],
            "jurisdiction": entry["jurisdiction"],
            "regulator": entry["regulator"],
            "official_domains": entry["official_domains"],
            "has_active_pattern_rules": entry["has_active_rules"],
            "instructions": (
                f"Fetch/cite ONLY these domains for {entry['name']}: "
                f"{', '.join(entry['official_domains'])}. "
                f"Regulator: {entry['regulator']}. "
                + ("Pattern rules already exist in rules/ for scored findings; "
                   "use this registry entry only if you need to verify a specific "
                   "clause's current wording."
                   if entry["has_active_rules"] else
                   "No pattern rules exist yet for this regulation — after "
                   "researching from the official domain(s) above, present "
                   "findings as an ADVISORY (unscored) section, and offer to "
                   "draft a new rules/<code>.yaml file per docs/RULES_SCHEMA.md.")
            ),
        }

    return {
        "status": "not_in_registry",
        "regulation_requested": regulation_query,
        "instructions": (
            f"'{regulation_query}' is not in rules/official_sources.yaml. "
            "Search for the OFFICIAL government regulator or standards body "
            "for this law (queries like "
            f"'{regulation_query} official regulator site' or "
            f"'{regulation_query} government data protection authority'). "
            "Before citing ANY result, check its domain: it must be a "
            "government domain (.gov, .gov.xx, .go.xx), an official "
            "intergovernmental body (e.g. europa.eu), or a recognized "
            "standards body (w3.org, iso.org, ietf.org). "
            "REJECT law-firm blogs, 'compliance platform' marketing pages, "
            "Wikipedia, and news aggregators as sources for the legal "
            "citation itself — they're fine for orientation but the clause "
            "citation and remediation text must trace back to the official "
            "source. Once found, propose adding it to "
            "rules/official_sources.yaml (see CONTRIBUTING.md) so the next "
            "lookup is instant instead of a fresh search."
        ),
    }
