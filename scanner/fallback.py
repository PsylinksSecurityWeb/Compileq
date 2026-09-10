"""Out-of-knowledge protocol helpers.

The scanner itself has no internet access — it's a pure static-analysis
engine so it stays fast, offline-capable, and auditable. When a user asks
about a regulation that isn't covered by active pattern rules in
rules/*.yaml, this module produces the structured request that the *host
AI* (Claude, or whatever LLM is running the skill/MCP tool) is instructed
to act on — see SKILL.md.

As of v0.2, this routes through scanner/web_lookup.py's official-source
registry (rules/official_sources.yaml) FIRST, so lookups are constrained to
government/regulator/standards-body domains only — never third-party blogs,
"compliance platform" marketing pages, or aggregators — before ever falling
back to an unconstrained search.
"""
from __future__ import annotations
from . import kb_loader, web_lookup


def is_known_regulation(rules_dir: str, name: str) -> bool:
    """True only if there are active PATTERN rules for this regulation
    (i.e. it can produce scored findings, not just registry metadata)."""
    known = {r.lower() for r in kb_loader.list_known_regulations(rules_dir)}
    return name.strip().lower().replace(" ", "_") in known or name.strip().lower() in known


def build_lookup_request(regulation_name: str) -> dict:
    """Structured object the host LLM should use to research a regulation
    and present the result as an advisory (non-scored) finding, using only
    official sources. This is now backed by the official-source registry —
    see web_lookup.lookup_instructions for the allowlist logic.
    """
    result = web_lookup.lookup_instructions(regulation_name)
    result["suggested_new_rule_path_pattern"] = "rules/{slug}.yaml"
    return result


def check_source(url: str, regulation_name: str = "") -> dict:
    """Validate a specific URL before it's cited as an authoritative source
    for a compliance finding. Use this on every URL before quoting it as
    'the law says X' — not just at the start of a lookup.
    """
    entry = web_lookup.find_registry_entry(regulation_name) if regulation_name else None
    return web_lookup.is_allowed_domain(url, entry)


def new_rule_stub(regulation_name: str) -> dict:
    """A starter YAML-able dict for a brand-new regulation file, meant to be
    filled in by the host LLM from official-source research and written out
    with a PR for maintainer review.
    """
    return {
        "regulation": regulation_name.upper().replace(" ", "_"),
        "jurisdiction": ["UNKNOWN - fill in"],
        "rules": [
            {
                "id": "REPLACE-001",
                "title": "REPLACE - short description of the pattern",
                "clause": "REPLACE - specific article/section citation",
                "description": "REPLACE",
                "file_types": [".py", ".js"],
                "pattern": "REPLACE - regex",
                "negative_pattern": None,
                "severity": 3,
                "likelihood": 3,
                "confidence_base": 0.3,
                "fine_range": [0, 0],
                "remediation": "REPLACE",
                "last_verified": "REPLACE - YYYY-MM-DD",
            }
        ],
    }
