# Risk scoring — the exact math

Every number in a report traces back to one of these four calculations,
implemented in `scanner/scoring.py`. Nothing here is a legal calculation —
it's a triage heuristic to help you prioritize what to look at first.

## 1. Jurisdiction weight

How relevant a rule is given the markets you actually operate in.

| Condition | Weight |
|---|---|
| Rule applies globally (e.g. WCAG, PCI-DSS) | 1.1 |
| Rule's jurisdiction matches one of your target markets | 1.3 |
| You didn't specify target markets | 1.0 |
| Rule's jurisdiction does NOT match your target markets | 0.7 |

Example: a GDPR rule when you said `--markets US` only (no EU) gets
downweighted to 0.7 — still shown, just deprioritized, because you might
still get EU users or might be wrong about your own market.

## 2. Risk score (0–100)

```
raw        = severity(1-5) × likelihood(1-5)      # max 25
normalized = (raw / 25) × 100                       # 0-100
risk_score = min(normalized × jurisdiction_weight, 100)
```

`severity` and `likelihood` are set per-rule in the YAML by the rule author,
based on (a) how bad the outcome is if the gap is real, and (b) how often
this pattern tends to be a genuine issue vs. a false positive in practice.

## 3. Confidence (0.0–1.0)

```
confidence = confidence_base × (0.5 if a "negative pattern" was found nearby else 1.0)
```

The `negative_pattern` in a rule is something that, if present in the same
file, suggests the issue is already handled (e.g. a `hasConsent()` check
near a tracking script call). Finding it doesn't clear the finding — it
just means treat it as a weaker signal, because the negative pattern could
be unrelated code.

**Anything below 0.5 confidence should be presented to the user as "worth
checking" language, never as a fact.** This is enforced in `SKILL.md`'s
presentation instructions, not just in the number itself.

## 4. Fine exposure estimate

```
low_estimate  = fine_range[0] × confidence
high_estimate = fine_range[1] × confidence
```

`fine_range` is the statutory min/max for that violation type, sourced from
public regulatory text at the time the rule was written (see each rule's
`last_verified` date). Scaling by confidence keeps a low-confidence, wide
statutory range (like GDPR's up to €20M/4% of global revenue) from
dominating a report with scary numbers that aren't actually likely.

**This is explicitly not a legal or actuarial calculation** — it exists to
help a founder triage "which finding do I look at first," not to predict an
actual fine.

## 5. Category readiness (0–100 per regulation)

```
category_readiness = 100 − mean(risk_score of findings in that category)
```

100 if zero findings in that category — meaning "nothing in our current
rule set flagged anything," not "certified compliant."

## 6. Overall readiness

Simple mean across all category readiness scores that were evaluated.
Deliberately unweighted in v1 (a GDPR gap and a missing-alt-text gap count
equally toward the average) — see `docs/ROADMAP.md` for planned
business-context weighting (e.g. weight PCI higher if the scan detects
payment code at all).
