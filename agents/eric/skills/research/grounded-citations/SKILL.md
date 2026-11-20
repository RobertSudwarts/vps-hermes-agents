---
name: grounded-citations
description: Ground external research claims in retrieved sources, a stable citation ledger and checked evidence. Verify exact vacancies and employer facts without taking over job discovery or application writing.
version: 2.0.0
author: Eric
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [research, citations, sources, web, evidence]
    related_skills: [job-discovery, cv-writing, cover-letter-writing, pdf]
---

# Grounded citations

Use for research answers and saved documents relying on external facts. Skip
formal citation machinery for incidental lookups, casual or creative work.
`/vault/eric/workflow-design.md` governs career boundaries: `job-discovery` owns
search/fit/register decisions; application skills own drafting. External evidence
never establishes an invented career claim or authorises protected-source edits.

## Evidence first

Retrieve and inspect substantive content before registering its actual URL or
writing findings. A plausible URL, ledger entry, search snippet, HTTP 200 or saved
shell is not proof of the expected facts. Separate retrieved bodies, excerpt-only
leads, failed fetches, attributed reports and hypotheses. Preserve URL, retrieval
and publication dates where known, evidence path and source-to-file mapping.

Use stable numbered ledger IDs inline and mechanically rendered Sources blocks
for research; do not invent IDs/URLs or reset a ledger used by existing drafts.
Run citation checks and independently assess claim support and currency: a green
check is reference integrity, not truth. Keep private provenance in research notes
rather than inserting research apparatus into employer-facing CVs/letters.

## Load selectively

- Citation operation or evidence-backed fact-checking: [ledger workflow](references/ledger-workflow.md), using unchanged `scripts/sources.py` and `scripts/_hermes_home.py`.
- Exact vacancy facts, language/geography or status uncertainty: [vacancy verification](references/vacancy-verification.md).
- Company landscape, mutual-value analysis, expansion or requested diligence: [employer research](references/employer-research.md).
- JavaScript shell, conflicting ATS fields or extraction failure: relevant section of [public ATS recovery](references/public-ats-recovery.md).
- Nonstandard output target: [citation formats](references/citation-formats.md).

Store dated dossiers, evidence and ledgers under `/vault/eric/Research/<topic>/`,
with concise navigation; reuse existing files, not the protected CV workspace.
Keep bulk pages/logs on disk. Do not automatically refresh an unchanged report.

No submission, outreach, external sharing of private material, account-access
resumption, software installation, configuration changes or autonomous skill
mutation. Respect public-source access limits and preserve historical research.
