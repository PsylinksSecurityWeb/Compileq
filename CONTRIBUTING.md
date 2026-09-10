# Internal Development Guide

Compileq is proprietary software owned by Psylinks Security Private Limited
(psylinkssecurity.com). This guide is for authorized internal contributors
and licensed partners working on the rule base — it is not an open
invitation for public pull requests, and this repository must not be made
public. See `LICENSE`.

## Code changes
Run `python -m unittest discover -s tests -v` before submitting for review
— CI runs this too. Route changes through your internal review process
rather than a public PR.

## Rule changes (most contributions will be this)
Rules are legal-adjacent content, so hold them to a higher bar than code:

1. Follow the schema in `docs/RULES_SCHEMA.md` exactly.
2. Cite the actual article/section — no rule without a real citation.
3. Add a fixture in `tests/fixtures/` that triggers it, and a test in
   `tests/test_engine.py`.
4. Set `last_verified` to the date you actually checked the citation.
5. In your change description, link the source you verified against
   (official regulation text preferred over a blog summary).
6. New-regulation changes (a whole new `rules/<name>.yaml`) should start
   small — 2-3 well-cited rules beat 20 speculative ones, and get reviewed
   by at least one other qualified reviewer before merge given the subject
   matter.
7. Do not remove or alter the `scanner/branding.py` watermark constants, or
   any code path that renders them into output, without sign-off from
   Psylinks Security Private Limited.

## Reporting a bad rule (false positive / wrong citation)
File an internal ticket with: the rule id, the file/line that triggered it,
and why it's wrong. If it's a citation error, please also propose the
correction.

## Adding to the official-source registry
`rules/official_sources.yaml` is the allowlist of domains the scanner (and
the AI host, per `SKILL.md`'s out-of-knowledge protocol) will treat as
authoritative for a given regulation — see `docs/COVERAGE.md` for what's
covered today. This is a lower bar than a full pattern-rule change, and
very welcome on its own:

1. Confirm the domain is genuinely the government/regulator/standards
   body's own site — not a private "data protection guide" site with a
   similar name, and not a law firm's summary page.
2. Add an entry following the existing schema (code, name, jurisdiction,
   regulator, official_domains, has_active_rules: false, verified_date).
3. If you also want to add pattern rules for it, flip `has_active_rules` to
   `true` in the same change and follow the rule-changes checklist above.

## What will not be accepted
- Rules with no cited clause
- Rules that auto-modify code without the CLI/MCP caller explicitly asking
  for a fix to be applied
- Anything that presents itself as a legal certification rather than a
  triage signal
- Any change that strips, hides, or genericizes the Compileq / Psylinks
  Security Private Limited attribution from output
