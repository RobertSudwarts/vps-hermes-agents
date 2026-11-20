# Source and adapter onboarding

Load only for adding/changing/validating a source or collection contract, not
routine snapshots or validated refreshes. Use [the CLI/API contract](../scripts/README.md)
and existing tests; no package installation is needed. Preserve deterministic
helpers and schema unless a replacement is deliberately scoped and tested.

1. Confirm a public source's relevance to the current brief. Save observed careers
   entrypoint, platform, request URL/method/payload, retrieval date, pagination,
   small real response sample and hashes in the existing research workspace.
   Keep secrets/private career material out of requests and evidence.
2. Establish stable IDs, exact posting URLs, fields, completeness and failure
   semantics before changing `sources.json` or the register. Classify automatic-ready,
   automatic-candidate, partial, manual or parked in onboarding evidence, not as
   invented watchlist `mode` values (the schema permits automatic/manual only).
3. Reconcile unique records with displayed totals on every page/category,
   including the final card. An undocumented export/plugin endpoint is not a
   stable automation contract. Group-wide boards need verified geography/entity
   filters; authoritative no-openings pages may be parked without frequent polling.
4. Test changes first using synthetic edge cases and preserved real observations:
   repeat stability, existing decisions/applications, literal IDs/location families,
   explicit closure versus absence, partial/failure/empty feeds, evidence redaction
   and concurrent-write protection. Run applicable existing tests. Validate live
   public behaviour only within authorised scope; historical fixtures are not
   current vacancy verification.
5. Prove completeness/failure handling before active monitoring. Verify protected
   sources, historical applications/research, configuration and schedules unchanged.
   Do not add schedules, install software, access authenticated/paused accounts or
   change collection contracts without separately scoped permission.

## Platform-specific acceptance

- **Recruitee:** validate full bodies and canonical careers URLs; existing helper
  accepts only observed open state codes `published` and `9`.
- **SuccessFactors HTML:** enumerate `searchresults` pages using `startrow`;
  accept displayed ranges such as “1 to 25 of 69”, reconcile unique listing total
  before details, then extract the enclosing `jobdescription` span including
  nested divs. One transient detail retry is reasonable; another failure remains
  incomplete and cannot establish absence.
- **SuccessFactors Recruiting JSON:** separate adapter variant; preserve public
  POST payload, reconcile `totalJobs`/`jobSearchResult` before exact details.
- **Workday:** obtain the public board token afresh, use it only in memory/request
  headers, redact it from saved evidence/configuration. Reconcile against the
  first nonzero total; later zero totals with rows are not empty feeds. Match
  stable listing requisitions to detail `jobReqId`, retain `externalUrl` and full
  location evidence. Inspect the existing contract caveat: the helper currently
  accepts an initially empty complete Workday feed, contrary to the desired
  conservative empty-feed rule. This needs deliberate review before unattended use.
- **Other ATS/structured pages:** use `grounded-citations`' selective public-ATS
  recovery reference. Successful one-off retrieval does not validate an adapter.

Fetch details selectively for in-scope or already tracked postings. Report
candidate platforms separately from validated adapters; do not turn a plausible
response into a claim of full coverage.
