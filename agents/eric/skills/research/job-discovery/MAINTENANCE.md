# Job-discovery replacement map

Maintenance record for the proposed package, 2026-11-20. Not routine skill
context. Original paths below are relative to the read-only backup package at
`/data/vps-agent-backups/eric/profile/skills/research/job-discovery/`.
“Retired” means not carried into the proposed runtime package; nothing was deleted
from the backup. No live search, register/watchlist edit or deployment occurred.

## Original package disposition

| Original file | Disposition and destination |
|---|---|
| `SKILL.md` | Replaced by [compact router](SKILL.md). Detailed incremental procedure moved to [incremental-search](references/incremental-search.md); state/decision rules to [register-rules](references/register-rules.md). Finance-first priorities, brief authority, German rules and access boundaries remain in the root. |
| `references/pipeline-reporting.md` | Retained, condensed [at the same path](references/pipeline-reporting.md): saved versus current state, submission reconciliation, fit versus sequencing, pauses and compact counts. |
| `references/bounded-role-assessment.md` | Old filename retired; substance consolidated into the existing proposed [bounded-assessment.md](references/bounded-assessment.md), with state semantics in [register-rules](references/register-rules.md) and refresh semantics in [incremental-search](references/incremental-search.md). Preserves caps, broader employer universe, regulator categories, board comparison, open routes, exact IDs, primary checks and outcome reporting. |
| `references/source-onboarding.md` | Retained, condensed [at the same path](references/source-onboarding.md). Preserves samples, completeness, failure safety, tokens, public-source validation and test-first changes. Platform-specific recovery stays with grounded-citations, not a second adapter implementation. |
| `references/human-outreach-research.md` | Retained, condensed [at the same path](references/human-outreach-research.md). Optional requested research/draft route; relationship history, current remit, verified channels, screenshot limits and no sending preserved. |
| `references/token-lean-commands.md` | Retained [byte-for-byte](references/token-lean-commands.md). Existing helper paths, JSON fields, exit-code inspection and compact-output recipe unchanged. Use subject to the Workday caveat in the contract. |
| `scripts/discovery.py` | Retained [byte-for-byte](scripts/discovery.py); no replacement, schema or executable behaviour change. |
| `scripts/README.md` | Retained [with corrections to documentation](scripts/README.md), not the implementation: Workday adapter/fields, header-aware injected transports, actual fetch signature, redacted evidence hashes, bounded SuccessFactors detail retry and empty-Workday caveat. CLI commands, decision set, schema v1 and write semantics preserved. |
| `tests/test_discovery.py` | Retained [byte-for-byte](tests/test_discovery.py), including synthetic cases and historical-evidence tests. |
| `tests/run_tdd.py` | Retained [byte-for-byte](tests/run_tdd.py). Optional maintenance runner appends a transcript; not used for this validation. |
| `tests/tdd-results.md` | Intentionally not carried forward: historical RED/GREEN transcripts stay in the backup, avoiding stale results presented as replacement-package validation. Fresh results are below. Running the retained test runner can create a new local transcript. |

## Existing proposed package disposition

All three existing files were revised in place: `SKILL.md`,
`references/bounded-assessment.md` and `references/source-onboarding.md`.
No existing proposed file was deleted. Added files are all destinations above,
plus `references/incremental-search.md`, `references/register-rules.md` and this
maintenance map. The two new references split recurring collection from conditional
assessment/state maintenance, avoiding full methodology loads for snapshots.

## Preserved contracts and deliberate exclusions

- Active brief remains `/vault/eric/Research/job-search/README.md`; watchlist and
  register remain its `sources.json` and `opportunities.json`. No data/schema migration.
- Retained CLI `refresh`, `report`, `review`; API signatures, exact keys, decision
  vocabulary, evidence/report outputs and exits 0/1/2 remain unchanged. A dry
  refresh writes evidence/reports even without `--apply`; `report` is read-only.
- German rules apply per vacancy: explicit mandatory professional German excludes;
  preferred/unspecified remains uncertain. Remote/office/English labels do not
  establish eligibility or working language.
- Retained exact user decisions, prior fit, application links, employer pauses,
  agency-identity uncertainty, new/change/backlog distinctions and manual-source limits.
- Repetitive prose is consolidated; automatic fan-out is excluded. Parallel work,
  if explicitly authorised, shares one deduplicated cap. No new installation,
  scheduler, external outreach or autonomous skill maintenance is introduced.

## Validation and unresolved implementation issue

All 31 existing discovery tests passed across two runs: 30 passed in the sandbox;
the loopback HTTP test was initially blocked by socket permissions, then passed
alone with the required execution permission. The three historical-fixture tests
used a process-local read-only mapping from `/vault/eric/Research/` to the local
backup; test files and fixtures were not edited. Temporary state was isolated.
No live feed was queried; these results are not current ATS acceptance checks.

SHA-256 comparisons confirm identical script/test bytes:

- `scripts/discovery.py`: `6966da5de8c181b51a404226dec318bf1d15083f6ad726330482f8a1a215fbda`
- `tests/test_discovery.py`: `efb70514867715784035afdc613a8b52f8ef25706b2a8c1df6bf5e20b3ac770e`
- `tests/run_tdd.py`: `0422200501e84c5e0eec08ab000f529dce9754092b8a12be542e4766885dbfad`

**Existing Workday policy/implementation mismatch:** a first response with
`total: 0` and an empty postings list is treated as complete and may mark tracked
roles `not_listed` under `--apply`, despite the conservative empty-feed policy.
This was reproduced with synthetic offline data in temporary state. The helper
was deliberately left unchanged; onboarding and contract notes flag the limitation.
A nonempty dry run cannot guarantee a later mutating fetch stays nonempty.
Unattended Workday use needs a separately scoped, tested correction or explicit
acceptance of the completeness semantics. No role is thereby proven filled.

Package sanity checks passed: local Markdown links, whitespace, Python syntax,
YAML parsing, original-file mapping coverage and two-package-only edit scope.
The generic Codex skill validator rejects the existing Hermes-specific `author`,
`platforms` and `version` frontmatter fields; these were deliberately preserved
and checked as YAML rather than removed to satisfy a different metadata schema.
