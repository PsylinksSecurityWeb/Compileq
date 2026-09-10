"""All the numeric estimation/calculation logic lives here, in one place,
so the formulas are auditable rather than scattered through the engine.
See docs/RISK_SCORING.md for the human-readable explanation of each one.
"""
from __future__ import annotations

JURISDICTION_MATCH_WEIGHT = 1.3
JURISDICTION_PARTIAL_WEIGHT = 1.0
JURISDICTION_NO_MATCH_WEIGHT = 0.7
GLOBAL_JURISDICTION_WEIGHT = 1.1


def jurisdiction_weight(rule_jurisdictions: list[str], target_markets: list[str]) -> float:
    """How relevant is this rule given the markets the product targets."""
    rule_set = set(rule_jurisdictions)
    target_set = set(target_markets)
    if "Global" in rule_set:
        return GLOBAL_JURISDICTION_WEIGHT
    if rule_set & target_set:
        return JURISDICTION_MATCH_WEIGHT
    if not target_set:
        return JURISDICTION_PARTIAL_WEIGHT
    return JURISDICTION_NO_MATCH_WEIGHT


def risk_score(severity: int, likelihood: int, jw: float) -> float:
    """0-100 risk score. raw = severity(1-5) * likelihood(1-5), max 25.
    Normalized to 100, then adjusted by jurisdiction relevance, capped 0-100.
    """
    raw = severity * likelihood
    normalized = (raw / 25.0) * 100.0
    adjusted = normalized * jw
    return round(min(adjusted, 100.0), 1)


def confidence(confidence_base: float, negative_pattern_hit: bool) -> float:
    """Confidence that a raw pattern match is a genuine finding.
    Halved (roughly) if a mitigating/negative pattern was also found nearby,
    since that usually means the issue is already handled and this is a
    weaker signal, but not necessarily a false positive.
    """
    c = confidence_base
    if negative_pattern_hit:
        c = c * 0.5
    return round(max(0.0, min(c, 1.0)), 2)


def fine_exposure(fine_range: list[float], conf: float) -> dict:
    """Rough fine exposure estimate. Always a range, always confidence-
    scaled, always explicitly a non-legal estimate for triage purposes.
    """
    low, high = fine_range[0], fine_range[1]
    return {
        "low_estimate": round(low * conf, 2),
        "high_estimate": round(high * conf, 2),
        "raw_range": [low, high],
        "note": "Rough triage estimate, not a legal or actuarial calculation.",
    }


def category_readiness(findings_for_category: list[dict]) -> float:
    """100 if no findings in this regulation category. Otherwise
    100 minus the mean risk score of findings in that category, floored at 0.
    """
    if not findings_for_category:
        return 100.0
    mean_risk = sum(f["risk_score"] for f in findings_for_category) / len(findings_for_category)
    return round(max(0.0, 100.0 - mean_risk), 1)


def overall_readiness(category_scores: dict[str, float]) -> float:
    """Simple mean across all scanned categories that had at least one rule
    evaluated. Not weighted by category importance on purpose (v1) — see
    docs/ROADMAP.md for planned business-context weighting.
    """
    if not category_scores:
        return 100.0
    return round(sum(category_scores.values()) / len(category_scores), 1)
