# Hermes Hub Operations

## Purpose

This workspace documents Rob’s self-hosted Nous Hermes Agent Deployment
on the VPS. It runs two persistent Discord-accessible agents:

- `bramble` — personal coach and Obsidian-vault assistant.
- `eric` — career research and CV-writing assistant.

Rob executes VPS commands himself. Propose commands clearly, explain
consequential changes, and do not assume access to the VPS.

## Deployment

- VPS Compose project: `/home/rob/hermes-hub`
- Persistent host data: `/srv/hermes-hub`
- One container: `hermes-hub-agent-1`
- Container mounts:
  - `/srv/hermes-hub/state` → `/opt/data`
  - `/srv/hermes-hub/vault` → `/vault`
- No host ports are published for Hermes.
- Hermes must not join public Docker networks or receive the Docker socket.
- The container is built from the Nous Hermes image with LaTeX support for
  Eric’s CV workflow.

## Profiles and vaults

### Bramble

- profile: /srv/hermes-hub/state/profiles/bramble
- vault: /srv/hermes-hub/vault/bramble

### Eric

- profile: /srv/hermes-hub/state/profiles/eric
- vault: /srv/hermes-hub/vault/eric

## Agent personalities

Read `agents/bramble/SOUL.md` or `agents/eric/SOUL.md` when the relevant
agent’s personality or intended role matters. These are read-only symlinks to
the latest local backup; do not edit them from this workspace.

Hermes uses one default-profile gateway multiplexer. Do not start separate 
gateways for `bramble` or `eric`.

## Important safety rules

- Never expose Discord tokens, Codex authentication, `.env` contents, or private keys.
- Do not mount the Docker socket.
- Do not add Hermes to publicly reachable networks or publish ports.
- Do not run destructive Docker, filesystem, or profile-migration actions without Rob’s explicit approval.
- Do not treat agent-generated claims of completed actions as proof; verify where practical.

## Eric’s career material

- Eric’s vault root is `/vault/eric`.
- His protected factual source record is `/vault/eric/CV/reference/CV/source/`.
- `/vault/eric/CV/workflow-design.md` records the current career-support workflow.
- Tailoring must not alter protected source material.
- Eric may produce fresh, truthful role-specific CV prose, but must not invent qualifications, responsibilities, results, or proficiency.
- Rob’s German is not sufficient for professional German-language work. Exclude roles where German is explicitly mandatory; flag uncertainty when it is merely preferred or unspecified.

## Backups

The local backup destination is `/data/vps-agent-backups/`.

Back up only:

- each agent’s `SOUL.md`;
- each agent’s `skills/`;
- both vaults.

Do not back up Hermes databases, caches, locks, sessions, logs, sockets, or credentials through the routine content-backup script.

The vault rsync operation uses `--delete-delay`, so deleted VPS vault files are removed from the local mirror after transfer.

## Further documentation

Keep detailed architecture, backup instructions, restore notes, and operational commands in `docs/`. Keep this file concise and current.

