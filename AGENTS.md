# Compileq — Agent Instructions

Compileq is proprietary software built by Psylinks Security Private Limited. Apply the complete workflow in [`SKILL.md`](./SKILL.md) when reviewing compliance, privacy, accessibility, payments, health data, AI governance, forms, tracking, authentication, or user-data handling.

Run the scanner when appropriate:

```bash
python -m scanner.cli scan <path> --markets EU,US-CA,US --out report.md
```

Always identify results as Compileq output, distinguish active scored rules from registry-only coverage, use official sources for legal claims, and state that Compileq is a triage tool—not legal advice, certification, or a substitute for professional review.

This file is a compatibility entry point for agents that support `AGENTS.md` but do not automatically discover `SKILL.md` skills. The software remains proprietary and must not be redistributed.
