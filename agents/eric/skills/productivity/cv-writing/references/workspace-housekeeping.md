# Separately requested workspace housekeeping

Retained here as an optional maintenance route because CV artifacts need preservation safeguards. It is not a drafting step and supplies no standing permission to delete, move, change sources, build documents or redesign the archive.

## Inspect before proposing changes

- Resolve the exact absolute target and distinguish the live vault, a backup and a synchronised copy. Read current navigation/migration notes; do not assume local contents prove live-server state.
- Requests to list, check emptiness or assess deletability are read-only. Inspect at the requested depth, including hidden entries, types and symlinks. Top-level patterns match immediate children only. Use code for counts/sizes and avoid dumping private contents or contact details.
- If expected files are absent, report the discrepancy and consult the existing migration map; do not recreate files, broaden cleanup or change rsync deletion semantics. If no targets remain, stop.

## Preserve before any authorised removal or relocation

Read existing manifests and run the documented preservation checker when relevant. Compare actual SHA-256 hashes, not names/sizes. Distinguish reproducible intermediates, identical copies and unique drafts/evidence/submitted versions. Successful archive verification does not make all old files disposable. Preserve protected sources, frozen revisions, submissions and template releases.

Deletion requires explicit permission for exact targets. For empty directories, validate **all** named targets first: actual directories, no symlinks, no contents including hidden files. If any differs, stop. Use only non-recursive `rmdir`, which also rejects a directory that becomes nonempty. Verify absence; report partial success if a later removal fails. Never expand to recursive content deletion.

Structural moves require their own scope: inventory old/new relative paths and hashes, refuse collisions, preserve every original byte, and verify before updating mutable navigation. Keep a relocation map; do not rewrite frozen records or Research merely to modernise paths. Keep frozen-archive verification separate from a one-off full layout snapshot so editable drafts/status notes do not become accidentally frozen. Use `--check-layout` only for that snapshot check; disable bytecode writing if importing frozen verification code.

Use the current paths/checker in [application records](application-records.md). Verify the exact affected scope and unchanged protected material after authorised archival work. Return a brief result; trivial inspection or empty-directory removal does not need a new audit hierarchy or persistent memory. This reference does not authorise skill/memory mutation or configuration changes.
