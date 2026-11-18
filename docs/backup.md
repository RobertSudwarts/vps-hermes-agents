# Hermes Hub content backup

## Purpose

This backup preserves the material that gives Bramble and Eric their useful long-term identity and working knowledge:

- each agent’s `SOUL.md`;
- each agent’s `memories/MEMORY.md` and `memories/USER.md`;
- each agent’s learned `skills/`;
- each agent’s vault.

It intentionally does **not** back up Hermes credentials, authentication state, sessions, databases, caches, logs, locks, sockets, gateway state, or other runtime artefacts.

This is a content-and-capability backup, not a complete bare-metal restoration of the Hermes container.

## Backup source and destination

The backup runs from Rob’s development machine and pulls data from the VPS over
SSH. Its remote `rsync` process runs inside the existing Hub container as the
unprivileged `hermes` user. This lets it read Hermes-owned files regardless of
their creation mode, without granting the host SSH user broad access.

| Item | Location |
|---|---|
| Local backup script | `scripts/backup.sh` |
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
│   │   ├── memories/
│   │   │   ├── MEMORY.md
│   │   │   └── USER.md
│   │   └── skills/
│   └── vault/
└── eric/
    ├── profile/
    │   ├── SOUL.md
    │   ├── memories/
    │   │   ├── MEMORY.md
    │   │   └── USER.md
    │   └── skills/
    └── vault/
```

## Running a backup

From the local operations workspace:

```bash
./scripts/backup.sh
```

The script uses `rsync` over SSH, with the remote process executed as UID/GID
`988` in `hermes-hub-agent-1`. The derived Hub image must include `rsync`.
It should complete without `sudo`, passwords in scripts, or remote write access.

The script stops at the first failed step and reports which copy failed. Only
`Backup completed for bramble and eric.` means all eight transfers succeeded.
After a failure, earlier copies may have updated locally while later ones did
not; rerun the script after resolving the error.

## Vault mirroring behaviour

The vault transfers use `rsync --delete-delay`.

This means the local vaults are mirrors of the VPS vaults:

- new or changed VPS files are copied locally;
- files deleted from a VPS vault are deleted from the corresponding local vault after a successful transfer;
- deletions happen at the end of the transfer rather than during it.

This is intentional, but it means the local backup is not historical version retention. An accidental deletion on the VPS will be reflected locally during the next successful backup.

The profile `SOUL.md`, `memories/` and `skills/` copies do not use deletion mirroring. They are retained locally unless deliberately removed. Only `MEMORY.md` and `USER.md` are copied from each `memories/` directory; other files there are excluded.

## Access model

SSH authenticates as VPS user `rob`; the source-side `rsync` is then executed
as the container's `hermes` user (UID/GID `988`) through the existing container
manager access. It has only the access Hermes itself has to the two mounted
content locations. This avoids depending on host ACL inheritance, which can be
defeated when Hermes atomically creates a file with mode `0600`.

The backup does not use remote `sudo`, store VPS passwords in the script, or
make vault content world-readable. Do not add unrestricted passwordless root
access to make backups work.

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
3. Restore only the required agent’s vault, SOUL file, memory files or skills.
4. Restore ownership to the `hermes` user where necessary.
5. Start the container and verify the relevant agent can read its vault and retains the expected identity.

Do not restore arbitrary database, cache, gateway or session files from this backup.

## Future improvement

The current backup is a mirror, not an archive. If the Hub becomes important enough that accidental deletion protection is needed, add occasional dated snapshots of `/data/vps-agent-backups/` to separate local storage or encrypted off-device storage.
