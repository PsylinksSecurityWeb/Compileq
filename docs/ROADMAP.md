# Roadmap

## v0.1 (this release)
- Regex-based rule engine, 6 regulations, ~20 starter rules
- CLI + MCP server, both backed by the same engine
- Risk/confidence/fine-exposure scoring
- Out-of-knowledge fallback protocol
- Rule staleness flagging (180-day threshold)

## v0.2 (near-term)
- AST-based rules for JS/TS and Python for the highest-precision checks
  (fewer false positives than regex for things like "is this value actually
  written to a database" vs. "does this line contain the word card_number")
- `--diff` mode: scan only files changed in the current git diff / PR, for
  CI use
- GitHub Action wrapping the CLI for automatic PR comments
- A `severity_override` config file so teams can tune false-positive-prone
  rules down without editing the shared rule files

## v0.3+
- Business-context-weighted overall readiness (e.g. if no payment code is
  detected at all, PCI-DSS readiness shouldn't drag down the average the
  same way GDPR does for a consumer app)
- Additional regulations via community PRs: LGPD (Brazil), PIPEDA (Canada),
  POPIA (South Africa), India's DPDP Act, additional US state laws
  (Virginia VCDPA, Colorado CPA)
- Optional "apply fix" mode that generates an actual diff per finding
  (currently the skill instructs the AI host to do this conversationally —
  formalizing it as a tool would let it work non-interactively in CI)
- A signed/reviewed-rules tier: distinguish community-contributed rules from
  rules that have had a compliance professional review the citation

## Explicitly out of scope
- Legal certification of any kind. This tool triages; it does not certify.
- Auto-fixing without human review by default (WCAG auto-remediation
  specifically is a known source of accessibility overlay controversy —
  see the market research this project started from).
