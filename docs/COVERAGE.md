# Coverage — what's actively scanned vs. registry-only

This is the honest map of what the scanner can do today, generated from
`rules/official_sources.yaml`. **"Active pattern rules"** means the scanner
produces scored findings (risk score, confidence, fine estimate) for that
regulation right now. **"Registry only"** means the regulation is known —
its regulator and official domain(s) are on file so a lookup is instant and
constrained — but nobody has written pattern rules for it yet. That's a
`CONTRIBUTING.md`-shaped opportunity, not a dead end: the out-of-knowledge
protocol (see `SKILL.md`) still gets you accurate, officially-sourced
answers about it, just not automated pattern detection.

| Regulation | Jurisdiction | Regulator | Official domain(s) | Status |
|---|---|---|---|---|
| General Data Protection Regulation (GDPR) | EU, EEA | European Data Protection Board / national DPAs | eur-lex.europa.eu, edpb.europa.eu | Active pattern rules |
| UK GDPR / Data Protection Act 2018 | UK | Information Commissioner's Office (ICO) | ico.org.uk, legislation.gov.uk | Registry only |
| California Consumer Privacy Act / CPRA (CCPA) | US-CA | California Privacy Protection Agency / California AG | cppa.ca.gov, oag.ca.gov | Active pattern rules |
| HIPAA | US | US Department of Health and Human Services (HHS) | hhs.gov | Active pattern rules |
| COPPA | US | Federal Trade Commission (FTC) | ftc.gov | Active pattern rules |
| Gramm-Leach-Bliley Act (GLBA) | US | Federal Trade Commission (FTC) | ftc.gov | Registry only |
| FERPA | US | US Department of Education | studentprivacy.ed.gov, ed.gov | Registry only |
| Sarbanes-Oxley Act (SOX) | US | Securities and Exchange Commission (SEC) | sec.gov | Registry only |
| PCI-DSS | Global | PCI Security Standards Council | pcisecuritystandards.org | Active pattern rules |
| WCAG | Global | W3C / Web Accessibility Initiative | w3.org | Active pattern rules |
| ADA (Title III, web application) | US | US Department of Justice | ada.gov | Registry only |
| EU AI Act | EU | European Commission / AI Office | eur-lex.europa.eu, digital-strategy.ec.europa.eu | Active pattern rules |
| LGPD | BR | Autoridade Nacional de Proteção de Dados (ANPD) | gov.br | Active pattern rules |
| PIPEDA | CA | Office of the Privacy Commissioner of Canada | priv.gc.ca | Active pattern rules |
| POPIA | ZA | Information Regulator (South Africa) | inforegulator.org.za | Registry only |
| PDPA (Singapore) | SG | Personal Data Protection Commission (PDPC) | pdpc.gov.sg | Registry only |
| DPDP Act, 2023 | IN | Ministry of Electronics and IT (MeitY) | meity.gov.in | Registry only |
| PIPL | CN | Cyberspace Administration of China (CAC) | cac.gov.cn | Registry only |
| APPI | JP | Personal Information Protection Commission (PPC) | ppc.go.jp | Registry only |
| PIPA (South Korea) | KR | Personal Information Protection Commission (PIPC) | pipc.go.kr | Registry only |
| Privacy Act 1988 | AU | Office of the Australian Information Commissioner (OAIC) | oaic.gov.au | Registry only |
| Nigeria Data Protection Act | NG | Nigeria Data Protection Commission (NDPC) | ndpc.gov.ng | Registry only |
| SOC 2 | Global | AICPA | aicpa-cima.com, aicpa.org | Registry only |
| ISO/IEC 27001 | Global | ISO | iso.org | Registry only |

**9 of 23 regulations have active scored pattern rules; all 23 have a
verified official-source domain on file.** New rules should target the
"Registry only" rows first — the regulator relationship is already
established, so a contributor just needs to translate specific clauses into
patterns (see `docs/RULES_SCHEMA.md`).

## How this list is meant to grow

This is deliberately not trying to be exhaustive on day one — there are
100+ jurisdictions with some form of data protection law. The registry
structure is what scales: adding a new regulation the scanner can *talk
about accurately* is a one-entry YAML change (`rules/official_sources.yaml`);
adding one it can *actively scan for* is a slightly bigger change
(`rules/<code>.yaml` + fixtures + tests, per `docs/RULES_SCHEMA.md`). Both
are welcome, and the registry-only tier is what makes the out-of-knowledge
protocol (`SKILL.md`) safe at scale — the tool never has to choose between
"refuse to answer" and "guess," because it either has a rule, has an
allowlisted official domain, or explicitly says it found neither.
