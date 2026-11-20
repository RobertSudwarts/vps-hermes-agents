# Saved pipeline reporting

For “what is left?”, “what next?” or ranking existing propositions, report saved
state rather than refreshing every employer.

1. Select relevant register rows in code: key, employer/title, decision,
   availability, last_checked, reason, evidence and application_record. Do not
   print descriptions, raw feeds or the whole register.
2. Read linked application state only as needed. Reconcile newly reported
   submissions using [register rules](register-rules.md); exclude applied roles
   from next-application recommendations. Preserve employer pauses, parked work,
   prior judgements and exact posting/location distinctions.
3. Rank against the active brief and recorded evidence/caveats; do not reload
   unchanged career history. Separate actionable roles, conditional leads,
   submitted applications and deferred work. Label a selected shortlist versus
   the complete reviewed pipeline.
4. Separate strongest role fit from sequencing or employer diversification.
   Explain any weaker-fit next choice; do not invent a diversification preference
   or pause an employer merely because one application was sent there.
5. State observation dates and that this is saved state, not live verification.
   Verify the chosen role before application work, or a bounded set if Rob asks
   for current availability. A new/reassessed current recommendation requires
   substantive primary verification, not a fresh timestamp on old evidence.
6. Count/deduplicate the final selected set in code. Return a compact in-chat
   view with the important caveat per role; no dashboard or duplicate persistence
   unless separately requested.

Do not silently drop unresolved leads or infer closure from a failed fetch.
For a requested new scan, load the relevant search route instead.
