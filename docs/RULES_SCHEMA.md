# Rule schema — how to add a regulation or a rule

Each file in `rules/` is one regulation:

```yaml
regulation: GDPR              # short code, used everywhere in reports
jurisdiction: [EU]             # or [Global], [US-CA], [US], etc.
rules:
  - id: gdpr-005                              # unique, kebab-case, prefixed by regulation
    title: Short human title
    clause: "Art. X - Official section name"   # exact legal citation
    description: >
      One or two sentences a non-lawyer can understand, explaining what
      pattern this looks for and why it matters.
    file_types: [".py", ".js"]                 # extensions this rule scans
    pattern: "regex here"                       # Python re syntax
    negative_pattern: "regex or null"            # mitigating signal, optional
    severity: 1-5                                # how bad if real
    likelihood: 1-5                              # how often this pattern is a real issue
    confidence_base: 0.0-1.0                      # starting confidence before negative_pattern applied
    fine_range: [min_usd, max_usd]                 # statutory range, source it
    remediation: >
      Concrete, actionable fix instructions.
    last_verified: "YYYY-MM-DD"                     # when you checked this against current law
```

## Guidelines for good rules

- **Prefer high precision over high recall.** A rule that fires constantly
  on non-issues trains users to ignore the tool. Set `confidence_base` low
  (0.2–0.4) for anything pattern-matched rather than structurally certain.
- **Always cite a real clause.** If you can't point to the actual article/
  section, don't add the rule yet — flag it as a question in your change description
  instead.
- **`last_verified` is not optional.** Rules older than 180 days are flagged
  `stale` in every report automatically (see `scanner/kb_loader.py`). Update
  this date whenever you re-check the rule against current law.
- **Test fixtures required.** Any new rule needs at least one fixture file
  in `tests/fixtures/` that should trigger it, added to `tests/test_engine.py`.
- **New regulation = new file.** Don't mix regulations in one YAML file —
  the report generator groups by `regulation`.

## Adding a whole new regulation (e.g. LGPD, PIPEDA, DPDP)

1. Create `rules/<name>.yaml` following the schema above.
2. Start with 2–3 high-confidence, well-cited rules rather than a huge
   speculative list.
3. Add fixtures + tests.
4. Submit for internal review. Since this is legal-adjacent content,
   changes adding or altering rules should get a second pair of eyes
   before merge — see `CONTRIBUTING.md`.

This is also exactly the format the AI host produces when using the
out-of-knowledge fallback protocol (`scanner/fallback.py` →
`new_rule_stub()`), so a user hitting an uncovered regulation in normal use
can generate a first draft of this file automatically.
