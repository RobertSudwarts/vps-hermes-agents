# Register decisions and preservation

Use the existing schema and literal opportunity key, never a guessed replacement
ID. `sources.json` is a watchlist, not a market census; `opportunities.json` is
mutable working state, not the historical application archive or career record.

| Decision | Meaning |
|---|---|
| `unreviewed` | No substantive assessment recorded; may be old backlog |
| `shortlisted` | Positive research judgement, not Rob's selection |
| `reviewed` | Conditional lead worth reconsidering |
| `excluded` | Concrete disqualifier, unsupported role-defining requirement, or explicit user rejection; record which |
| `deferred` | Parked role or temporary pause with scope and resumption condition |
| `applied_reported` | Rob reports submission; not verified delivery |

Retain first/last observations, meaningful changes, reasons, evidence and
application links. Machine refreshes must not overwrite manual decisions.
A changed excluded role merits reconsideration, not silent promotion. Record
user choice separately from fit: selecting an excluded role does not erase its
assessment or justify a veto. Link the application and hand off to truthful
application preparation; do not rewrite frozen scan reports.

For reported submission, read the exact application record, preserve associated
artifact/archive evidence via `cv-writing`'s application-records route, and
reconcile that exact opportunity to `applied_reported` with its canonical link.
Do not infer receipt, sending time/bytes or final pasted answers. Do not invent a
posting for an open application lacking a matching register row. Archive checks
and tracker-schema checks are distinct; complete both applicable checks.

For “park” use `deferred`; for an explicit decline use `excluded` and record user
preference, not invented closure or inability. Resolve the exact preceding list,
including named secondary alternatives. Suppress repeated recommendations even
if the feed still lists the role. Revisit only on Rob's request or substantive
change; a role rejection is not an employer-wide ban.

For a temporary employer pause, retain scope/resumption condition in the brief,
defer relevant opportunities and exclude the employer from active scans. Preserve
prior fit and relationship evidence. Do not infer an automatic restart date from
an imprecise waiting period or resume paused accounts.

Prefer `discovery.py review` for supported manual fields; it changes decision/
reason and optional evidence/application references only. Preserve the prior
assessment in dated evidence before replacing a summary reason. For other manual
edits, run `discovery.py report --workspace /vault/eric/Research/job-search` and
inspect its exit/diagnostic before declaring success. Correct only affected
records; never weaken validation or alter frozen evidence to accommodate errors.
See [the contract](../scripts/README.md) for fields and write/concurrency limits.

Keep employer evaluation separate from vacancy state: append dated evaluation
evidence and maintain the existing compact latest-by-FMA-ID index with
`last_evaluated_at_utc`, classification, careers route and recheck trigger.
Evaluated employers are not automatically active sources, openings or recommendations.
