# Hermes Agent Hub architecture

## Purpose

The VPS runs a single self-hosted Nous Hermes Agent container serving two persistent, Discord-accessible agent profiles:

| Profile | Agent | Purpose |
|---|---|---|
| `bramble` | Bramble | Personal coach and Obsidian-vault assistant |
| `eric` | Eric | Career research, job discovery, and CV-writing assistant |

The shared-container design avoids duplicating the Hermes runtime, bundled skills, gateway services, browser tooling and baseline memory footprint.

## High-level topology

```text
Discord
  │
  │  Separate bot identity and token for each agent
  ▼
hermes-hub-agent-1 container
  │
  ├── default-profile gateway multiplexer
  │     ├── routes Bramble’s Discord bot
  │     └── routes Eric’s Discord bot
  │
  ├── profile: bramble
  │     └── /vault/bramble
  │
  └── profile: eric
        └── /vault/eric
```

The gateway multiplexer runs inside hermes-hub-agent-1 as a Hermes process associated with the neutral default profile. “Host gateway” refers to its role as the one gateway serving all profiles within that Hermes installation; it is not a VPS-level system service or a separate container.

There is exactly one Hermes host gateway. It is managed from the neutral `default` profile and multiplexes incoming messages to the named `bramble` and `eric` profiles.

Do not start separate per-profile gateways, use `gateway.standalone`, or use forced gateway installation for either named profile.

## VPS deployment

| Item | Location / setting |
|---|---|
| Compose project | `/home/rob/hermes-hub` |
| Container | `hermes-hub-agent-1` |
| Persistent state on host | `/srv/hermes-hub/state` |
| Persistent vaults on host | `/srv/hermes-hub/vault` |
| State mount in container | `/opt/data` |
| Vault mount in container | `/vault` |
| Runtime Unix identity | `hermes` — UID/GID `988` |
| CPU limit | 2 CPUs |
| Memory limit | 3 GiB |
| PID limit | 512 |
| Restart policy | `unless-stopped` |

The container runs with `no-new-privileges` and does not receive the Docker socket.

## Container image and LaTeX support

The Hub uses a locally built image derived from `nousresearch/hermes-agent:latest`.

The derived image includes the minimum useful LaTeX toolchain for Eric’s CV workflow, including `latexmk`, `texlive-latex-extra` and recommended fonts, plus `rsync` for the content-backup source. This allows Eric to compile and inspect role-specific PDF CVs within the container while the backup runs as the unprivileged container user.

The image build definition belongs in the Compose-project directory. The image should be rebuilt after intentional changes to the Dockerfile or after reviewing upstream Hermes updates.

## Networking and exposure

Hermes has no published host ports and is not attached to the VPS’s public-facing Docker networks.

Discord connectivity is outbound. Caddy remains the only public HTTP/HTTPS ingress for the VPS’s web applications.

This arrangement means the agents are reachable through Discord but do not expose a web service directly to the internet.

## Profile storage

```text
/srv/hermes-hub/
├── state/
│   └── profiles/
│       ├── bramble/
│       └── eric/
└── vault/
    ├── bramble/
    └── eric/
```

Each named profile has its own persisted configuration, SOUL file, memories, skills, cron configuration and other Hermes state.

Each agent has its own intended vault root:

| Agent | Container vault path | Host vault path |
|---|---|---|
| Bramble | `/vault/bramble` | `/srv/hermes-hub/vault/bramble` |
| Eric | `/vault/eric` | `/srv/hermes-hub/vault/eric` |

The two profiles share a container and can technically see the same mounted `/vault` tree. The `bramble` and `eric` directories are therefore an organisational boundary, not a hard security boundary.

## Current model defaults

| Agent | Current model |
|---|---|
| Bramble | `gpt-6-sol` |
| Eric | `gpt-6.1-sol` |

Model selection is profile-specific. Changes should be made deliberately and recorded in the relevant agent’s persistent configuration.

## Discord

Bramble and Eric each have their own Discord bot identity and token.

Never run a second copy of either agent using the same bot token: Discord bot tokens represent a single bot identity and concurrent gateways would conflict.

Each agent has a Discord home channel for scheduled-job results and cross-platform messages.

## Eric’s career-workspace boundary

Eric’s factual career source is:

```text
/vault/eric/CV/reference/CV/source/
```

That material is protected during CV tailoring. Eric may use it to write fresh, truthful, role-specific application material, but must not alter the factual source record.

The current workflow principles are recorded in:

```text
/vault/eric/CV/workflow-design.md
```

## Operational principles

- Keep credentials, Discord tokens, authentication files and private keys out of documentation and source control.
- Do not expose Hermes through public ports or attach it to public Docker networks.
- Do not mount the Docker socket into Hermes.
- Treat agent claims about completed actions as claims to verify, particularly for file changes and external communication.
- Keep routine agent-content backups separate from disposable runtime state.
- See `backup.md` for the local backup design and `runbook.md` for safe operational commands.
