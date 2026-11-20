# Incremental search of validated sources

1. Read the active brief and compact register/application state. Apply exact
   posting exclusions and employer pauses before collecting; reconcile reported
   applications under [register rules](register-rules.md) to prevent duplicates.
2. Select already validated public sources. Consult [the contract](../scripts/README.md)
   when needed and check actual CLI help for unfamiliar commands. Manual boards
   remain manual work. A refresh without `--apply` still writes evidence/reports;
   only `report` is read-only. Observe the documented Workday empty-feed caveat.
3. Refresh selected sources using the existing helper. Keep output in files;
   inspect per-source status, completeness, counts/errors, events, review queue
   and unresolved backlog using [compact commands](token-lean-commands.md).
   Exit 1 may include useful positive observations plus partial/failure results;
   exit 2 is a command/schema/concurrency error, not a valid collection result.
4. Treat failures, truncation, malformed/partial responses and unvalidated empty
   feeds as unknown, never closure. Absence from a complete feed establishes only
   `not_listed`, not filled. Unchanged runs preserve backlog; filling a missing
   fingerprint baseline is not observed change. Preserve source IDs, exact
   location/language variants and explicit requisition families.
5. Screen new/changed records cheaply by real geography, language, status,
   grade and work. Read exact primary specifications only for plausible roles;
   do not infer Austrian eligibility from remote labels. If a bounded substantive
   pass is requested or needed, load [bounded assessment](bounded-assessment.md),
   declare a cap, and label backlog separately from new observations.
6. Keep discovery broad over time; the watchlist is not a market census.
   Deliberate bounded employer expansion is appropriate when warranted, but do
   not launch a broad search after every unchanged refresh. Review noisy-source
   priority without silently changing the brief or source contract.
7. Preserve observations, decisions, evidence and application links. Validate
   manual edits with the read-only tracker `report`; no schema loosening to make
   malformed records pass. Deliver relevant changes, pending review and source
   limitations, not a raw feed. Distinguish source collection from role assessment.

Anonymous-client agency adverts may be cross-postings. Compare client/project
clues, responsibilities, location, work pattern, start date and duration; retain
uncertain related sources without calling them confirmed duplicates or counting
independently new roles from agency IDs alone.

Keep mechanical timings and source/new/changed/suppressed/backlog counts separate
from model input/output/cache usage. Neither fewer calls nor faster collection
establishes cost savings, recall or useful recommendations.
