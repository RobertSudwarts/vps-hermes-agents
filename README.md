# Hermes Agent Hub

Operations notes and a local backup script for Rob's self-hosted Nous Hermes
deployment on a VPS. One Docker Compose container serves two persistent agents
through Discord: **Bramble**, a personal coach and Obsidian-vault assistant, and
**Eric**, a career research and CV-writing assistant.

The VPS Compose project is at `/home/rob/hermes-hub`; persistent data is under
`/srv/hermes-hub`. This repository documents the deployment but is not the
live Compose project. Rob runs VPS commands himself.

## Start here

- [Architecture](docs/architecture.md) — container, profiles, storage and network design.
- [Runbook](docs/runbook.md) — operational checks and maintenance commands.
- [Backup](docs/backup.md) — backup scope, access model and restore principles.
- [Image updates](docs/image-updates.md) — update cadence, preparation and verification.
- [Agent instructions](AGENTS.md) — workspace rules and safety boundaries.

## Local content backup

Run from this repository on Rob's development machine:

```bash
./scripts/backup.sh
```

It copies the agents' SOUL files, selected memories and skills, plus both vaults,
to `/data/vps-agent-backups/`. Only the message
`Backup completed for bramble and eric.` means every transfer succeeded. The
backup excludes credentials and runtime state; see the [backup guide](docs/backup.md)
before relying on it for recovery.

Do not place tokens, `.env` contents or private keys in this repository.
