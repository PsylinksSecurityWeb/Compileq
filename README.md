# Compileq

**Built by [Psylinks Security Private Limited](https://psylinkssecurity.com)**

Compileq scans a codebase for likely compliance gaps — GDPR, CCPA/CPRA,
WCAG, PCI-DSS, HIPAA, EU AI Act, LGPD, COPPA, PIPEDA, and more via an
official-source registry covering 24+ regulations worldwide — scores the
risk, estimates fine exposure, and proposes concrete fixes. It runs as a
Claude Skill or as an MCP server, so it works inside Claude Code, Claude
Cowork, Cursor, VS Code + Copilot, Windsurf, or any other MCP-compatible
IDE.

> ⚠️ **This repository is proprietary software, not open source.** It is distributed through a private GitHub repository and licensed channels only.
> Copyright © Psylinks Security Private Limited. All rights reserved. Do
> not fork, redistribute, or publish this code publicly. See [`LICENSE`](./LICENSE)
> for the full terms. If you found this repository without authorization,
> please contact us at [psylinkssecurity.com](https://psylinkssecurity.com).

---

## What it does

- Runs a static, rule-based scan of your repository for patterns that
  commonly correlate with compliance gaps (missing consent gates before
  tracking scripts, unencrypted PII/PHI fields, raw card numbers touching
  your own storage, missing alt text and form labels, automated
  decision-making without human oversight, and more).
- Scores every finding: a **risk score (0–100)**, a **confidence score
  (0–1)**, and a rough **fine-exposure estimate** — see
  [`docs/RISK_SCORING.md`](./docs/RISK_SCORING.md) for the exact formulas.
- Produces a **category readiness score** per regulation and an overall
  readiness score, in both Markdown (for humans) and JSON (for tooling).
- When it doesn't know something, it doesn't guess: it routes through an
  **official-source registry** (`rules/official_sources.yaml`) that maps
  each regulation to its actual government/regulator/standards-body
  domain, and explicitly refuses to treat law-firm blogs, marketing pages,
  or aggregators as authoritative — see
  [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md).
- **This is a triage tool, not legal advice or a certification.** Every
  report says so, and confidence scores exist precisely so low-certainty
  findings are never presented as fact.

## Quick start

```bash
pip install -r scanner/requirements.txt
python -m scanner.cli scan /path/to/your/repo --markets EU,US-CA --out report.md
```

### As a Claude Skill (Claude Code / Claude Cowork)

```bash
cp -r compileq ~/.claude/skills/compileq
pip install -r ~/.claude/skills/compileq/scanner/requirements.txt
```

Claude will pick up `SKILL.md` automatically — just ask it to scan a repo
for compliance issues.

### Codex, Cursor, Antigravity, and other AI IDEs

For OpenAI Codex or any Agent Skills-compatible tool, copy the package into its
documented skill directory. For example:

```bash
mkdir -p ~/.codex/skills/compileq
cp -R . ~/.codex/skills/compileq/
```

Cursor can discover the `SKILL.md` package through a compatible skills folder,
or use the included [`.cursor/rules/compileq.mdc`](./.cursor/rules/compileq.mdc)
project-rule bridge. For Antigravity and tools that do not auto-discover
Agent Skills, copy [`AGENTS.md`](./AGENTS.md) into the project root or paste
its instructions into the IDE's project rules. The scanner and MCP server work
independently of the host AI tool.

### As an MCP server (Cursor, VS Code + Copilot, Windsurf, Claude Desktop)

```bash
pip install -r mcp_server/requirements.txt
```

Add to your MCP host's config:

```json
{
  "mcpServers": {
    "compileq": {
      "command": "python",
      "args": ["/absolute/path/to/compileq/mcp_server/server.py"]
    }
  }
}
```

Full install instructions: [`docs/INSTALL.md`](./docs/INSTALL.md).

## Coverage

| | |
|---|---|
| Regulations with active, scored pattern rules | GDPR, CCPA/CPRA, WCAG, PCI-DSS, HIPAA, EU AI Act, LGPD, COPPA, PIPEDA |
| Regulations in the official-source registry | 24+, spanning EU/UK/US/Brazil/Canada/South Africa/Singapore/India/China/Japan/South Korea/Australia/Nigeria plus global standards (SOC 2, ISO 27001) |

Full matrix: [`docs/COVERAGE.md`](./docs/COVERAGE.md).

## Repository layout

```
SKILL.md                   Claude Skill definition
scanner/                    the engine (offline, deterministic, testable)
  engine.py                 repo walker + rule matcher
  scoring.py                risk / confidence / fine-exposure formulas
  report.py                 Markdown report generator
  web_lookup.py              official-source allowlist enforcement
  fallback.py                out-of-knowledge lookup protocol
  branding.py                 product/maker attribution (single source of truth)
  cli.py                     command-line entry point
rules/*.yaml                 pattern rules, one file per regulation
rules/official_sources.yaml   the 24-regulation official-domain registry
mcp_server/server.py         MCP server wrapper for non-Claude IDEs
docs/                        architecture, scoring formulas, coverage, install
tests/                       27 tests, all fixtures included
```

## Documentation

- [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md) — how the pieces fit together, including the out-of-knowledge protocol
- [`docs/RISK_SCORING.md`](./docs/RISK_SCORING.md) — every formula behind every number in a report
- [`docs/RULES_SCHEMA.md`](./docs/RULES_SCHEMA.md) — how to add a new rule or regulation
- [`docs/COVERAGE.md`](./docs/COVERAGE.md) — active vs. registry-only regulation coverage
- [`docs/INSTALL.md`](./docs/INSTALL.md) — detailed install steps for every IDE
- [`docs/ROADMAP.md`](./docs/ROADMAP.md) — what's next
- [`CONTRIBUTING.md`](./CONTRIBUTING.md) — internal contribution guide (authorized contributors only)

## Testing

```bash
python -m unittest discover -s tests -v
```

27 tests covering the rule loader, scoring math, engine detection against
real fixture files, and the official-source allowlist logic.

## License

Proprietary — All rights reserved, Psylinks Security Private Limited. See
[`LICENSE`](./LICENSE). This software is not licensed under MIT, Apache,
or any open-source license; redistribution and derivative works are
prohibited without written permission.

---

**Compileq** is a product of **Psylinks Security Private Limited**
— [psylinkssecurity.com](https://psylinkssecurity.com)
