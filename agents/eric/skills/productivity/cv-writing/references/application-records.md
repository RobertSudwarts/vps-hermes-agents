# Application records and reported submissions

Use only for a record request or Rob's report that he submitted an application. This records his report; it does not submit anything or establish employer receipt.

## Preserve the existing structure

Paths are relative to `/vault/eric/`. Read `Applications/README.md` and the target application's current pointers as needed. Reuse `Applications/YYYYMMDD/<application>/working/`, frozen `revisions/rNNN/` and separate `submissions/sNNN/`; never overwrite an existing frozen revision or submission. Directory dates identify work/archive batches, not sending times. A neutral recipient filename such as `robert_sudwarts_cv.pdf` is separate from revision identity.

Keep original artifact bytes, available input snapshots, provenance and recorded unknowns. Do not regenerate a historical submission, substitute a newer draft or silently repair frozen records. The November 11 audit at `Applications/20261111/audit/` stays frozen. Use `archive/layout-migration-20261112.json` to interpret historical paths without rewriting ledgers or Research.

## Bounded submission-record update

1. Identify the exact application, associated delivered revision/documents and opportunity entry. If multiple artifacts could be intended, clarify that link rather than guessing sent bytes. Read the existing submission schema and tracker contract; reuse them without inventing another archive format.
2. Create the next `submissions/sNNN/` note and machine-readable manifest. Preserve associated delivered PDFs and any delivered form-answer text. Mark answers as drafts unless Rob confirms the final pasted wording; label submission time, outgoing filename/bytes and receipt unknown unless evidence establishes them. Record the provenance of any confirmation.
3. Identify the CV as the primary PDF and letters separately. Include each copied document in `associated_delivered_documents` with `filename`, application-relative `linked_artifact` and checksum, following the existing schema. Verify actual SHA-256 copy/link hashes; names and sizes are insufficient. A matching associated copy does not prove it was sent.
4. Update application status and navigation index, and reconcile the exact existing opportunity entry to `applied_reported`, preserving prior fit judgements. Validate against the tracker contract; do not use unsupported shorthand `applied`, invent a posting for an open application or defer reconciliation to the next search. If no matching entry exists, report that limitation.
5. After the complete update, run `python3 /vault/eric/Applications/verify_archive.py` once. On failure investigate the affected records, make only authorised mutable-record corrections and rerun the relevant checks. Do not rewrite frozen material to pass. Report partial completion or unresolved checks honestly; do not claim an atomic transaction.

Use deterministic checks with concise results. No new research, PDF rebuild or external action belongs in this transition. Archive checks establish preservation within their checked scope, not delivery, external attestation or tamper-proof storage.
