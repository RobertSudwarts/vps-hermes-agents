# Hermes Hub content backup

## Purpose

This backup preserves the material that gives Bramble and Eric their useful long-term identity and working knowledge:

- each agent’s `SOUL.md`;
- each agent’s learned `skills/`;
- each agent’s vault.

It intentionally does **not** back up Hermes credentials, authentication state, sessions, databases, caches, logs, locks, sockets, gateway state, or other runtime artefacts.

This is a content-and-capability backup, not a complete bare-metal restoration of the Hermes container.

## Backup source and destination

The backup runs from Rob’s development machine and pulls data from the VPS over SSH.

| Item | Location |
|---|---|
| Local backup script | `scripts/vps-hermes-agent-backup.sh` |
| VPS SSH host alias | `netcup` |
| VPS Hub state | `/srv/hermes-hub/state/profiles/` |
| VPS vaults | `/srv/hermes-hub/vault/` |
| Local backup root | `/data/vps-agent-backups/` |

The local result is:

```text
/data/vps-agent-backups/
├── bramble/
│   ├── profile/
│   │   ├── SOUL.md
│   │   └── skills/
│   └── vault/
└── eric/
    ├── profile/
    │   ├── SOUL.md
    │   └── skills/
    └── vault/
```

## Running a backup

From the local operations workspace:

```bash
./scripts/vps-hermes-agent-backup.sh
```

The script uses `rsync` over SSH. It should complete without `sudo`, passwords in scripts, or remote write access.

The script stops at the first failed step and reports which copy failed. Only
`Backup completed for bramble and eric.` means all six transfers succeeded.
After a failure, earlier copies may have updated locally while later ones did
not; rerun the script after resolving the error.

## Vault mirroring behaviour

The vault transfers use `rsync --delete-delay`.

This means the local vaults are mirrors of the VPS vaults:

- new or changed VPS files are copied locally;
- files deleted from a VPS vault are deleted from the corresponding local vault after a successful transfer;
- deletions happen at the end of the transfer rather than during it.

This is intentional, but it means the local backup is not historical version retention. An accidental deletion on the VPS will be reflected locally during the next successful backup.

The profile `SOUL.md` and `skills/` copies do not use deletion mirroring. They are retained locally unless deliberately removed.

## Access model

The VPS user `rob` has narrowly scoped ACL-based read access to the required Hermes profile and vault material.

The backup does not use remote `sudo`. Do not add `sudo -S`, store VPS passwords in the script, or use an unrestricted passwordless root credential to make the backup work.

If a backup fails with a permission error, inspect the relevant ACL on the VPS
rather than weakening the backup authentication design. Use `namei -l` to find
the blocked path and `getfacl -p` on that directory or file. A named `rob` ACL
entry may still grant no effective access if its ACL mask is `---`; check the
effective permissions before making a narrow correction. Avoid recursive or
world-readable permission changes.

## What is intentionally excluded

The routine backup excludes or omits:

- SQLite databases and write-ahead-log files;
- active session and gateway state;
- logs, caches, scratch files and browser runtime artefacts;
- lock, PID and socket files;
- Codex/Hermes authentication and Discord credentials.

Hermes recreates this runtime material after a restart. Keeping it out makes the backup smaller, more stable and safer to retain locally.

## Restore principles

A vault restoration should be treated as a deliberate recovery operation:

1. Stop the Hermes Hub container first.
2. Preserve or rename the current target directory before overwriting it.
3. Restore only the required agent’s vault, SOUL file or skills.
4. Restore ownership to the `hermes` user where necessary.
5. Start the container and verify the relevant agent can read its vault and retains the expected identity.

Do not restore arbitrary database, cache, gateway or session files from this backup.

## Future improvement

The current backup is a mirror, not an archive. If the Hub becomes important enough that accidental deletion protection is needed, add occasional dated snapshots of `/data/vps-agent-backups/` to separate local storage or encrypted off-device storage.
