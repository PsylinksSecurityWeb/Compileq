# Architecture

```
                     ┌─────────────────────┐
                     │   rules/*.yaml       │  versioned knowledge base
                     │   (GDPR, CCPA, WCAG, │  (data, not code — editable
                     │   PCI-DSS, HIPAA,    │   internally, see CONTRIBUTING)
                     │   EU_AI_Act, ...)    │
                     └──────────┬───────────┘
                                │ kb_loader.py
                                ▼
                     ┌─────────────────────┐
                     │   scanner/engine.py │  walks repo, regex-matches,
                     │                      │  builds raw findings
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │  scanner/scoring.py  │  risk score, confidence,
                     │                      │  fine exposure, readiness
                     └──────────┬───────────┘
                                │
              ┌─────────────────┴─────────────────┐
              ▼                                     ▼
   ┌─────────────────────┐              ┌─────────────────────────┐
   │  scanner/cli.py       │              │  mcp_server/server.py    │
   │  (Claude Skill path — │              │  (MCP path — Cursor,     │
   │  invoked via bash by  │              │  VS Code+Copilot, any    │
   │  Claude Code/Cowork)  │              │  MCP host)                │
   └─────────────────────┘              └─────────────────────────┘
```

Both entry points call the *same* `scanner/engine.py` and
`scanner/scoring.py` — there is exactly one implementation of "what counts
as a finding" and "how risky is it," so the CLI and the MCP server can never
silently disagree.

## Out-of-knowledge protocol

The engine is intentionally offline and rule-based — no LLM call happens
inside `scanner/`. This is a deliberate tradeoff: it makes the core scan
fast, deterministic, testable, and auditable (you can read every rule that
could possibly fire). The cost is that it only knows what's in `rules/`.

To handle things outside that knowledge without breaking the "deterministic
core" property, and without ever citing a third-party source as if it were
authoritative, the protocol is split across three layers:

1. **`rules/official_sources.yaml`** — a curated registry of 24+
   regulations/frameworks, each mapped to its actual government/regulator/
   standards-body domain(s). See `docs/COVERAGE.md`. This is the fast path:
   most "what does regulation X require" questions resolve here instantly
   without any network call at all, just a lookup.
2. **`scanner/web_lookup.py`** — pure, offline policy logic. Given a
   regulation name, it checks the registry first; if there's no entry, it
   returns instructions requiring any cited source to match a
   government-domain pattern (`.gov`, `.gov.xx`, `.go.xx`, `europa.eu`,
   recognized standards bodies) and explicitly rejecting law-firm blogs,
   marketing pages, Wikipedia, and aggregators. It also exposes
   `is_allowed_domain()` so any specific URL can be checked before it's
   cited, not just at the start of a lookup. `scanner/fallback.py` is the
   thin entry point both the CLI and MCP server call into this from.
3. **The host AI (Claude, or whatever LLM runs the MCP tools)** — performs
   the actual web search/fetch using its own tools, but only within the
   domain constraints layer 2 hands it, and labels anything sourced this
   way as **advisory**, distinct from the KB-backed, scored findings.

This means: the scored numbers in a report are always traceable to a
specific, versioned, human-reviewed pattern rule. The registry-backed
material is always traceable to a named government/regulator domain, even
without a pattern rule behind it. And anything found via open web search is
always clearly separated, domain-checked, and labeled lower-trust. Nothing
in the report can silently blend "the KB said so," "the registry pointed
here," and "the LLM guessed" into one undifferentiated claim.

## Staleness handling

`kb_loader.load_rules()` computes `stale = (today - last_verified) > 180 days`
per rule at load time — not baked into the YAML — so it's always evaluated
against the actual current date, and every report surfaces a stale-rule
count without needing a separate maintenance script.

## Why regex instead of AST parsing (for now)

Regex is faster to write rules for, works identically across every
language/file type without a parser dependency per language, and is
transparent enough that a non-engineer can read a rule and understand what
it looks for. The tradeoff is more false positives on structurally complex
code. See `docs/ROADMAP.md` for planned AST-based rules for the
highest-value languages (JS/TS, Python) once the pattern-based rule set has
proven out which checks are worth the extra precision.
