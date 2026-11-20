# Grounded-citations replacement map

Maintenance record for the proposed package, 2026-11-20. Not routine skill
context. Original paths below are relative to the read-only backup package at
`/data/vps-agent-backups/eric/profile/skills/research/grounded-citations/`.
“Retired” means omitted from the proposed runtime package, not deleted from backup.

## Original package disposition

| Original file | Disposition and destination |
|---|---|
| `SKILL.md` | Replaced by [compact router](SKILL.md). Ledger/evidence procedures move to [ledger-workflow](references/ledger-workflow.md), career vacancy safeguards to [vacancy-verification](references/vacancy-verification.md), employer framing to [employer-research](references/employer-research.md), and recovery pitfalls to [public-ats-recovery](references/public-ats-recovery.md). |
| `scripts/sources.py` | Retained [byte-for-byte](scripts/sources.py); all commands, render styles, JSON schema, normalized URL identities, quotes, verification and exit behaviour preserved. |
| `scripts/_hermes_home.py` | Retained [byte-for-byte](scripts/_hermes_home.py); Hermes resolver and standalone fallback unchanged. |
| `references/citation-formats.md` | Retained, condensed [at the same path](references/citation-formats.md). All implemented styles remain available. Removes stale named dependencies and erroneous self-handoff for academic papers; accurately distinguishes Markdown reference checks from target-format validation. No new document-building authority. |
| `references/employer-research.md` | Retained, split selectively: [employer-research](references/employer-research.md) for landscape/expansion/diligence, [vacancy-verification](references/vacancy-verification.md) for exact role/language/geography/compensation/status, [public-ats-recovery](references/public-ats-recovery.md) for observed retrieval patterns. Preserves entity scope, independent disclosures, attributed employee accounts, mutual value, uncertainty, access and dossier-preservation boundaries. |
| `references/grounding-rationale.md` | Intentionally retired from runtime instructions. Research-paper, leaked-prompt and implementation-history discussion is not needed to operate the ledger and is not newly verified here. Its actionable principles—register after retrieval, cite while composing, render mappings, stable IDs and checked quotations—live in [ledger-workflow](references/ledger-workflow.md). Claims of impossible wrong URLs or product-level guarantees are not retained: storing a URL does not prove retrieval or entailment. |

## Existing proposed package disposition

The existing `SKILL.md` is revised in place. Added files are the two original
scripts, five selective references linked above and this maintenance map.
No existing proposed file was deleted. The proposed root's broad primary-source
principles remain, but the original stable ledger/evidence contract is restored
instead of replacing it with manually assembled links.

## Preserved contracts and deliberate exclusions

- Ledger path precedence, v1 schema, source IDs and normalization unchanged.
  Recommended explicit task paths avoid overwriting another task's default ledger;
  this changes operating guidance, not the script's default.
- All CLI actions retained: `reset`, `add`, `ingest`, `quote`, `list`, `render`,
  `verify`; render styles markdown/plain/footnotes/bibtex/evidence remain intact.
- Quotes are checked against supplied text; evidence/coverage gates do not prove
  authenticity, every-claim support or current facts. `[unverified]` still counts
  as declared provenance, not verification. Unused-source warnings are explained,
  not “fixed” by irrelevant citations. Sources replacement is limited to mutable
  drafts with Sources last. Serial writes are preferred over relying on the
  existing best-effort lock as a concurrency guarantee.
- German and geographic rules remain in exact-vacancy verification. Employer
  evidence stays separate from protected career facts and opportunity decisions.
- Generic automatic multi-platform sweeps and optional-plugin catalogues are
  omitted; requested research may use available appropriate sources, attribute
  reports versus measurement and disclose coverage gaps without installing tools.
- PDF/Word/slides citation placement remains guidance only; obsolete tool names
  and build recipes are excluded. Employer-facing application text is not modified
  to add research citations. Research ledgers/evidence stay separate.

## Validation

21 isolated CLI checks passed using synthetic data and an explicit temporary
ledger: help, normalized/idempotent registration, listing, accepted/rejected
quotes, idempotent rendering, unknown-ID/URL-mismatch/missing-evidence rejection,
strict/coverage verification, all five render styles and JSON ingestion. No network,
profile-default ledger, backup or live profile was written. This is a bounded
contract smoke check, not a new exhaustive test suite.

SHA-256 matches to the original:

- `scripts/sources.py`: `0c216e29e092faedcaa1ebae129db15dfc100465169490704b3628446db96788`
- `scripts/_hermes_home.py`: `e2fba7b30ee22afdb21e8411b6a18431da6efc9ec3ef55e2223481bf906f4376`

Known retained limitations: the lock is best-effort, the verifier uses rough
sentence/URL parsing and literal parentheses can truncate a URL. Guidance exposes
these limits rather than silently changing code or overstating verification.

Package sanity checks passed: local Markdown links, whitespace, Python syntax,
YAML parsing, original-file mapping coverage and two-package-only edit scope.
The generic Codex skill validator rejects the existing Hermes-specific `author`,
`platforms` and `version` frontmatter fields; these were deliberately preserved
and checked as YAML rather than removed to satisfy a different metadata schema.
