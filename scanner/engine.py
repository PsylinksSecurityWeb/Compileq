"""Walks a repo, applies rules, produces raw findings."""
from __future__ import annotations
import os
import re

from . import scoring
from .branding import short_watermark, PRODUCT_NAME, MAKER_NAME, MAKER_URL

DEFAULT_IGNORE_DIRS = {
    ".git", "node_modules", "venv", ".venv", "dist", "build",
    "__pycache__", ".next", "target", "vendor",
}


def _iter_files(root: str, file_types: set[str]):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in DEFAULT_IGNORE_DIRS and not d.startswith(".")]
        for fn in filenames:
            ext = os.path.splitext(fn)[1]
            if ext in file_types:
                yield os.path.join(dirpath, fn)


def _line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def scan_repo(root: str, rules: list[dict], target_markets: list[str]) -> dict:
    """Returns a structured result: findings, category readiness, overall
    readiness, and metadata. This is the single entry point the CLI and the
    MCP server both call.

    Raises FileNotFoundError if root doesn't exist or isn't a directory —
    callers must not silently treat a bad path as a clean scan (an empty
    scan and a 100/100-readiness clean scan are indistinguishable
    otherwise, which is misleading).
    """
    if not os.path.isdir(root):
        raise FileNotFoundError(
            f"Scan target '{root}' does not exist or is not a directory."
        )

    findings = []
    all_file_types = set()
    for r in rules:
        all_file_types.update(r["file_types"])

    # Cache file contents so multi-rule scans don't re-read the same file.
    file_cache: dict[str, str] = {}

    for rule in rules:
        rule_exts = set(rule["file_types"])
        for path in _iter_files(root, rule_exts):
            if path not in file_cache:
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        file_cache[path] = f.read()
                except (OSError, UnicodeDecodeError):
                    continue
            content = file_cache[path]

            try:
                matches = list(re.finditer(rule["pattern"], content))
            except re.error:
                continue
            if not matches:
                continue

            negative_hit = False
            if rule.get("negative_pattern"):
                try:
                    negative_hit = re.search(rule["negative_pattern"], content) is not None
                except re.error:
                    negative_hit = False

            jw = scoring.jurisdiction_weight(rule["jurisdiction"], target_markets)
            rscore = scoring.risk_score(rule["severity"], rule["likelihood"], jw)
            conf = scoring.confidence(rule["confidence_base"], negative_hit)
            fine = scoring.fine_exposure(rule["fine_range"], conf)

            for m in matches[:5]:  # cap per-file matches to keep report readable
                findings.append({
                    "rule_id": rule["id"],
                    "regulation": rule["regulation"],
                    "clause": rule["clause"],
                    "title": rule["title"],
                    "description": rule["description"],
                    "file": os.path.relpath(path, root),
                    "line": _line_number(content, m.start()),
                    "snippet": content.splitlines()[_line_number(content, m.start()) - 1].strip()[:160],
                    "severity": rule["severity"],
                    "likelihood": rule["likelihood"],
                    "risk_score": rscore,
                    "confidence": conf,
                    "mitigation_signal_found": negative_hit,
                    "fine_exposure": fine,
                    "remediation": rule["remediation"],
                    "stale_rule": rule["stale"],
                })

    # Category (regulation) readiness
    by_category: dict[str, list[dict]] = {}
    for f in findings:
        by_category.setdefault(f["regulation"], []).append(f)

    scanned_categories = sorted({r["regulation"] for r in rules})
    category_scores = {
        cat: scoring.category_readiness(by_category.get(cat, []))
        for cat in scanned_categories
    }
    overall = scoring.overall_readiness(category_scores)

    findings.sort(key=lambda f: f["risk_score"], reverse=True)

    return {
        "product": PRODUCT_NAME,
        "maker": MAKER_NAME,
        "maker_url": MAKER_URL,
        "powered_by": short_watermark(),
        "root": root,
        "target_markets": target_markets,
        "rules_evaluated": len(rules),
        "files_scanned": len(file_cache),
        "findings": findings,
        "category_readiness": category_scores,
        "overall_readiness": overall,
        "stale_rule_count": sum(1 for r in rules if r["stale"]),
    }
