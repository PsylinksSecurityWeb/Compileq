"""Loads and validates the rule knowledge base from rules/*.yaml."""
from __future__ import annotations
import os
import glob
import datetime
import yaml

REQUIRED_FIELDS = [
    "id", "title", "clause", "description", "file_types", "pattern",
    "severity", "likelihood", "confidence_base", "fine_range",
    "remediation", "last_verified",
]

STALE_DAYS = 180


def load_rules(rules_dir: str) -> list[dict]:
    """Load every YAML file in rules_dir into a flat list of rule dicts,
    each annotated with its parent regulation, jurisdiction, and staleness."""
    rules = []
    today = datetime.date.today()
    for path in sorted(glob.glob(os.path.join(rules_dir, "*.yaml"))):
        with open(path, "r", encoding="utf-8") as f:
            doc = yaml.safe_load(f)
        regulation = doc.get("regulation", "UNKNOWN")
        jurisdiction = doc.get("jurisdiction", [])
        for rule in doc.get("rules", []):
            missing = [k for k in REQUIRED_FIELDS if k not in rule]
            if missing:
                raise ValueError(
                    f"Rule in {path} missing required fields: {missing} "
                    f"(rule id={rule.get('id', '?')})"
                )
            rule["regulation"] = regulation
            rule["jurisdiction"] = jurisdiction
            last_verified = datetime.date.fromisoformat(str(rule["last_verified"]))
            rule["stale"] = (today - last_verified).days > STALE_DAYS
            rules.append(rule)
    return rules


def list_known_regulations(rules_dir: str) -> list[str]:
    regs = []
    for path in sorted(glob.glob(os.path.join(rules_dir, "*.yaml"))):
        with open(path, "r", encoding="utf-8") as f:
            doc = yaml.safe_load(f)
        regs.append(doc.get("regulation", "UNKNOWN"))
    return regs
